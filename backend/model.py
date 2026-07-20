# model.py
import re
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from seed_data import generate_expanded_dataset

# Compact list of common English stopwords for explicit NLP visualization
STOPWORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd",
    'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers',
    'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
    'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
    'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if',
    'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
    'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out',
    'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
    'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
    'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should',
    "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't",
    'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't",
    'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't",
    'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"
}

def simple_stem(word):
    """A lightweight rule-based stemmer to simulate stemming in the NLP visualization."""
    w = word.lower()
    if len(w) <= 3:
        return w
    # Common suffix stripping
    if w.endswith('ingly'): w = w[:-5]
    elif w.endswith('ing'): w = w[:-3]
    elif w.endswith('edly'): w = w[:-4]
    elif w.endswith('ed'): w = w[:-2]
    elif w.endswith('ness'): w = w[:-4]
    elif w.endswith('ment'): w = w[:-4]
    elif w.endswith('s') and not w.endswith('ss') and not w.endswith('us') and not w.endswith('is'): w = w[:-1]
    return w

class FakeNewsClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            token_pattern=r'(?u)\b\w\w+\b|[!?!]'
        )
        self.model = LogisticRegression(C=1.5, max_iter=1000)
        self.is_trained = False
        self.train_accuracy = 0.0
        self.total_samples = 0
        self.additional_data = [] # Stores dynamically collected posts

    def add_collected_data(self, posts):
        """Append newly collected posts to the training dataset."""
        self.additional_data.extend(posts)
        # Force re-train on next prediction/status request
        self.is_trained = False

    def clean_text(self, text):
        """Basic text cleaning before classification."""
        if not text:
            return ""
        text = text.lower().strip()
        text = re.sub(r"[^a-zA-Z0-9\s!?.,]", "", text)
        return text

    def get_nlp_pipeline_steps(self, text):
        """Runs the input text through the NLP stages and returns the intermediate transformations."""
        raw_text = text
        # Step 1: Cleaned
        cleaned = self.clean_text(text)
        
        # Step 2: Tokenized (words + punctuation)
        tokenized = re.findall(r"\b\w+\b|[!?]", cleaned)
        
        # Step 3: Stopwords Filtered
        filtered = [w for w in tokenized if w.lower() not in STOPWORDS]
        
        # Step 4: Stemmed
        stemmed = [simple_stem(w) for w in filtered]
        
        return {
            "raw": raw_text,
            "cleaned": cleaned,
            "tokenized": tokenized,
            "filtered": filtered,
            "stemmed": stemmed
        }

    def train(self):
        """Train the TF-IDF and Logistic Regression model on seed data + additional collected data."""
        data = generate_expanded_dataset()
        # Merge dynamically collected data
        for item in self.additional_data:
            data.append({"text": item["text"], "label": item["label"]})
            
        df = pd.DataFrame(data)
        df['cleaned_text'] = df['text'].apply(self.clean_text)
        
        X = self.vectorizer.fit_transform(df['cleaned_text'])
        y = df['label'].values
        
        self.model.fit(X, y)
        self.train_accuracy = float(self.model.score(X, y))
        self.total_samples = len(df)
        self.is_trained = True
        
        print(f"Model trained successfully. Accuracy: {self.train_accuracy:.4f} on {self.total_samples} samples.")

    def explain_prediction(self, text):
        """Predicts credibility and explains using feature weights + returns NLP pipeline trace."""
        if not self.is_trained:
            self.train()
            
        cleaned = self.clean_text(text)
        x_vector = self.vectorizer.transform([cleaned])
        
        prob = self.model.predict_proba(x_vector)[0]
        classes = list(self.model.classes_)
        fake_idx = classes.index(0) if 0 in classes else 0
        real_idx = classes.index(1) if 1 in classes else 1
        fake_prob = float(prob[fake_idx])
        real_prob = float(prob[real_idx])
        
        prediction = 1 if real_prob >= 0.5 else 0
        confidence = real_prob if prediction == 1 else fake_prob
        
        coo = x_vector.tocoo()
        feature_names = self.vectorizer.get_feature_names_out()
        coefficients = self.model.coef_[0]
        
        contributions = []
        for col, val in zip(coo.col, coo.data):
            word = feature_names[col]
            coef = coefficients[col]
            score = val * coef
            contributions.append({
                "word": word,
                "score": float(score),
                "type": "real_signal" if score > 0 else "fake_signal"
            })
            
        contributions.sort(key=lambda x: abs(x["score"]), reverse=True)
        
        exclamation_count = cleaned.count('!')
        question_count = cleaned.count('?')
        uppercase_words = sum(1 for w in text.split() if w.isupper() and len(w) > 1)
        
        clickbait_markers = ["shocking", "unbelievable", "secret", "exposed", "truth", "warning", "miracle", "won't believe", "furious"]
        clickbait_hits = sum(1 for marker in clickbait_markers if marker in cleaned)
        clickbait_score = min(1.0, (clickbait_hits * 0.25) + (exclamation_count * 0.1) + (uppercase_words * 0.15))
        
        # Get detailed NLP pipeline steps
        nlp_steps = self.get_nlp_pipeline_steps(text)
        
        return {
            "prediction": "Real" if prediction == 1 else "Fake",
            "prediction_label": prediction,
            "confidence": confidence,
            "real_probability": real_prob,
            "fake_probability": fake_prob,
            "contributions": contributions[:15],
            "nlp_steps": nlp_steps,
            "metrics": {
                "clickbait_score": clickbait_score,
                "uppercase_words": uppercase_words,
                "exclamation_marks": exclamation_count,
                "question_marks": question_count,
                "length": len(text)
            }
        }

    def get_top_features(self, n=15):
        if not self.is_trained:
            self.train()
            
        feature_names = self.vectorizer.get_feature_names_out()
        coefficients = self.model.coef_[0]
        
        features = list(zip(feature_names, coefficients))
        features.sort(key=lambda x: x[1])
        
        top_fake = [{"word": f[0], "coefficient": float(f[1])} for f in features[:n]]
        top_real = [{"word": f[0], "coefficient": float(f[1])} for f in features[-n:]][::-1]
        
        return {
            "top_fake": top_fake,
            "top_real": top_real
        }
