from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
from fastapi.middleware.cors import CORSMiddleware
import logging
import kagglehub
import pandas as pd
import os

logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level to DEBUG to capture all types of log messages
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]  # Log messages will be output to the console
)
logging.getLogger('module_name').setLevel(logging.WARNING)

# Initialize the FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_urls():
    try:
        df = pd.read_csv("urldata.csv")  # Ensure this is the correct path
        return df["url"].tolist()  # Adjust column name based on CSV structure
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/urls")
def get_urls():
    urls = load_urls()
    return {"urls": urls}

# Load pre-trained Hugging Face models for phishing and URL malware detection
phishing_detector = pipeline("text-classification", model="cybersectony/phishing-email-detection-distilbert_v2.4.1")
url_detector = pipeline("text-classification", model="elftsdmr/malware-url-detect")

# Define the input structure for the email text
class EmailText(BaseModel):
    email_text: str

# Define the input structure for the URL
class URL(BaseModel):
    url: str

# Endpoint to detect phishing in an email
@app.post("/detect-phishing")
async def detect_phishing(data: EmailText):
    logging.debug("Received request to /detect-phishing endpoint.")
    logging.debug(f"Email content received: {data.email_text}")

    # Use the phishing model to classify the email text
    result = phishing_detector(data.email_text)
    label = result[0]['label']
    confidence = result[0]['score']

    logging.debug(f"Model raw output - Label: {label}, Confidence: {confidence}")

    # Mapping model labels to user-friendly labels
    if label == "LABEL_1":
        label = "MALICIOUS"
    elif label == "LABEL_0":
        label = "SAFE"
    else:
        label = "UNKNOWN"
    logging.info(f"Email classified as {label} with confidence {confidence:.2f}")

    return {"classification": label, "confidence": confidence}

# Endpoint to detect malware in a URL
@app.post("/detect-malware")
async def detect_malware(data: URL):
    logging.debug("Received request to /detect-malware endpoint.")
    logging.debug(f"URL received: {data.url}")

    # Use the URL malware model to classify the URL
    result = url_detector(data.url)
    label = result[0]['label']
    confidence = result[0]['score']
    logging.debug(f"Model raw output - Label: {label}, Confidence: {confidence}")

    # Replace "benign" with "safe"
    if label == "BENIGN":
        label = "SAFE"
    logging.info(f"URL classified as {label} with confidence {confidence:.2f}")

    return {"classification": label, "confidence": confidence}
if __name__ == "__main__":
    import uvicorn
    # Run the FastAPI app
    uvicorn.run(app, host="0.0.0.0", port=8000)
