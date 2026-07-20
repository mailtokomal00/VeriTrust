# verify_model.py
from model import FakeNewsClassifier

def run_tests():
    print("Initializing classifier...")
    clf = FakeNewsClassifier()
    
    print("Training model...")
    clf.train()
    
    print("\n--- Model Metrics ---")
    print(f"Total training samples: {clf.total_samples}")
    print(f"Training Accuracy: {clf.train_accuracy:.4f}")
    
    # Define test samples
    test_cases = [
        {
            "name": "Factual Health News",
            "text": "A new research study from Oxford University shows that regular daily walks can reduce blood pressure by 10% in adult patients.",
            "expected": "Real"
        },
        {
            "name": "Conspiracy / Fake Claim",
            "text": "SHOCKING TRUTH: Top secret laboratories are hiding a miracle herbal tea that cures diabetes instantly! Big pharma doesn't want you to know!",
            "expected": "Fake"
        },
        {
            "name": "Neutral Science Post",
            "text": "The international space station crew completed a six-hour spacewalk to upgrade the station's solar arrays, according to NASA officials.",
            "expected": "Real"
        },
        {
            "name": "Clickbait / Suspicious Post",
            "text": "ALERT: The moon is hollow and alien bases have been uncovered by satellite cameras! Click this link to see the hidden video!",
            "expected": "Fake"
        }
    ]
    
    print("\n--- Running Test Cases ---")
    passed = 0
    for tc in test_cases:
        res = clf.explain_prediction(tc["text"])
        pred = res["prediction"]
        conf = res["confidence"]
        
        status = "PASSED" if pred == tc["expected"] else "FAILED"
        if status == "PASSED":
            passed += 1
            
        print(f"[{status}] {tc['name']}")
        print(f"  Input: {tc['text'][:60]}...")
        print(f"  Predicted: {pred} (Confidence: {conf:.2%})")
        print("  Key contributions:")
        for contrib in res["contributions"][:3]:
            print(f"    '{contrib['word']}': {contrib['score']:+.4f}")
            
    print(f"\nResults: {passed}/{len(test_cases)} tests passed.")

if __name__ == "__main__":
    run_tests()
