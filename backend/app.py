from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
from fastapi.middleware.cors import CORSMiddleware
import logging
import pandas as pd
import os
from dotenv import load_dotenv
from openai import OpenAI

# 📦 Load API Key and initialize OpenAI client
load_dotenv()
client = OpenAI()  # uses OPENAI_API_KEY from env

# 🔧 Logging
logging.basicConfig(level=logging.DEBUG)
app = FastAPI()

# 🔓 CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📄 Input Schemas
class EmailText(BaseModel):
    email_text: str
    model: str = "gpt-3.5-turbo"

class URL(BaseModel):
    url: str

# 🧠 Load ML models
phishing_detector = pipeline(
    "text-classification",
    model="cybersectony/phishing-email-detection-distilbert_v2.4.1"
)

url_detector = pipeline(
    "text-classification",
    model="elftsdmr/malware-url-detect"
)

# 📂 Load URLs for dropdown
def load_urls():
    try:
        df = pd.read_csv("urldata.csv")
        return df["url"].tolist()
    except Exception as e:
        return {"error": str(e)}

# 📡 Routes
@app.get("/")
def home():
    return {"message": "Welcome to the AI Malware + Phishing Detection API!"}

@app.get("/api/urls")
def get_urls():
    return {"urls": load_urls()}

@app.post("/detect-phishing")
async def detect_phishing(data: EmailText):
    result = phishing_detector(data.email_text)
    label = result[0]["label"]
    confidence = result[0]["score"]
    label = "MALICIOUS" if label == "LABEL_1" else "SAFE"
    return {"classification": label, "confidence": confidence}

@app.post("/detect-malware")
async def detect_malware(data: URL):
    result = url_detector(data.url)
    label = result[0]["label"]
    confidence = result[0]["score"]
    if label == "BENIGN":
        label = "SAFE"
    return {"classification": label, "confidence": confidence}

@app.post("/explain-phishing")
async def explain_phishing(data: EmailText):
    prompt = f"""
You are a cybersecurity expert. Analyze the following email
and explain if it is a phishing attempt. Highlight suspicious
elements and provide helpful advice to the user.

EMAIL:
\"\"\"
{data.email_text}
\"\"\"
"""
    try:
        logging.debug(f"Calling OpenAI with model: {data.model}")
        response = client.chat.completions.create(
            model=data.model,
            messages=[
                {"role": "system", "content": "You are a helpful cybersecurity assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        explanation = response.choices[0].message.content
        return {"explanation": explanation}
    except Exception as e:
        logging.error(f"OpenAI API error: {e}")
        return {"error": "Failed to generate explanation."}
