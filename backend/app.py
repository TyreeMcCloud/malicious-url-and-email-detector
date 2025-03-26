from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
from fastapi.middleware.cors import CORSMiddleware




# Initialize the FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Load pre-trained Hugging Face models for phishing and URL malware detection
phishing_detector = pipeline("text-classification", model="cybersectony/phishing-email-detection-distilbert_v2.4.1")  # Use a relevant BERT-based model for phishing
url_detector = pipeline("text-classification", model="elftsdmr/malware-url-detect")  # Example URL malware detection model

# Define the input structure for the email text
class EmailText(BaseModel):
    email_text: str

# Define the input structure for the URL
class URL(BaseModel):
    url: str

# Endpoint to detect phishing in an email
@app.post("/detect-phishing")
async def detect_phishing(data: EmailText):
    # Use the phishing model to classify the email text
    result = phishing_detector(data.email_text)
    label = result[0]['label']
    # Mapping model labels to user-friendly labels
    if label == "LABEL_1":
        label = "MALICIOUS"
    elif label == "LABEL_0":
        label = "SAFE"
    confidence = result[0]['score']
    
    return {"classification": label, "confidence": confidence}

# Endpoint to detect malware in a URL
@app.post("/detect-malware")
async def detect_malware(data: URL):
    # Use the URL malware model to classify the URL
    result = url_detector(data.url)
    label = result[0]['label']
    # Replace "benign" with "safe"
    if label == "BENIGN":
        label = "SAFE"
    confidence = result[0]['score']
    
    return {"classification": label, "confidence": confidence}

if __name__ == "__main__":
    import uvicorn
    # Run the FastAPI app
    uvicorn.run(app, host="0.0.0.0", port=8000)
