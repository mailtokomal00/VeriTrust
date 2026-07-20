# main.py
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from model import FakeNewsClassifier
import data_collector

app = FastAPI(title="VeriTrust API", description="AI-powered fake news analysis API")

# Enable CORS for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize and train the model on startup
classifier = FakeNewsClassifier()

@app.on_event("startup")
def startup_event():
    print("Training model on startup...")
    classifier.train()

class AnalysisRequest(BaseModel):
    text: str

class CollectRequest(BaseModel):
    source: str  # "Twitter", "Reddit", "LocalFiles"

@app.post("/api/analyze")
def analyze_text(payload: AnalysisRequest):
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Text content cannot be empty.")
    try:
        explanation = classifier.explain_prediction(payload.text)
        return explanation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/collect")
def collect_data(payload: CollectRequest):
    valid_sources = ["Twitter", "Reddit", "LocalFiles"]
    if payload.source not in valid_sources:
        raise HTTPException(status_code=400, detail=f"Invalid source. Choose from {valid_sources}")
    try:
        collected = data_collector.collect_from_source(payload.source)
        classifier.add_collected_data(collected)
        # Re-train model with new data
        classifier.train()
        
        return {
            "success": True,
            "collected_count": len(collected),
            "total_samples": classifier.total_samples,
            "train_accuracy": classifier.train_accuracy,
            "items": collected
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/status")
def get_status():
    return {
        "status": "online",
        "model_trained": classifier.is_trained,
        "train_accuracy": classifier.train_accuracy,
        "total_samples": classifier.total_samples
    }

@app.get("/api/top-features")
def get_top_features(limit: int = 15):
    try:
        features = classifier.get_top_features(n=limit)
        return features
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
