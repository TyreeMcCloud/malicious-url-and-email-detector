from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from fastapi.middleware.cors import CORSMiddleware
<<<<<<< Updated upstream
import logging

logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level to DEBUG to capture all types of log messages
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]  # Log messages will be output to the console
)
logging.getLogger('module_name').setLevel(logging.WARNING)
=======
import torch
>>>>>>> Stashed changes

# Initialize the FastAPI app
app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Welcome to your AI Malware + Phishing Detection API!"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load pre-trained Hugging Face models for phishing and URL malware detection
phishing_detector = pipeline(
    "text-classification", 
    model="cybersectony/phishing-email-detection-distilbert_v2.4.1"
)

url_detector = pipeline(
    "text-classification", 
    model="elftsdmr/malware-url-detect"
)

# Load the language model for contextual phishing explanation
assistant_model = "mistralai/Mistral-7B-Instruct-v0.1"
tokenizer = AutoTokenizer.from_pretrained(assistant_model)
model = AutoModelForCausalLM.from_pretrained(
    assistant_model, 
    torch_dtype=torch.float16, 
    device_map="auto"
)

# Define input structures
class EmailText(BaseModel):
    email_text: str

class URL(BaseModel):
    url: str

# Endpoint to detect phishing in an email
@app.post("/detect-phishing")
async def detect_phishing(data: EmailText):
<<<<<<< Updated upstream
    logging.debug("Received request to /detect-phishing endpoint.")
    logging.debug(f"Email content received: {data.email_text}")

    # Use the phishing model to classify the email text
    result = phishing_detector(data.email_text)
    label = result[0]['label']
    confidence = result[0]['score']
    logging.debug(f"Model raw output - Label: {label}, Confidence: {confidence}")

    # Mapping model labels to user-friendly labels
=======
    result = phishing_detector(data.email_text)
    label = result[0]['label']
>>>>>>> Stashed changes
    if label == "LABEL_1":
        label = "MALICIOUS"
    elif label == "LABEL_0":
        label = "SAFE"
<<<<<<< Updated upstream
    else:
        label = "UNKNOWN"
    logging.info(f"Email classified as {label} with confidence {confidence:.2f}")

=======
    confidence = result[0]['score']
>>>>>>> Stashed changes
    return {"classification": label, "confidence": confidence}

# Endpoint to detect malware in a URL
@app.post("/detect-malware")
async def detect_malware(data: URL):
<<<<<<< Updated upstream
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
=======
    result = url_detector(data.url)
    label = result[0]['label']
    if label == "BENIGN":
        label = "SAFE"
    confidence = result[0]['score']
    return {"classification": label, "confidence": confidence}

# NEW: Endpoint to generate contextual phishing explanation
@app.post("/explain-phishing")
async def explain_phishing(data: EmailText):
    prompt = f"""
You are a cybersecurity assistant. Analyze the following email and explain if it is a phishing attempt. Highlight any suspicious elements and give helpful safety advice.

EMAIL:
\"\"\"
{data.email_text}
\"\"\"
"""
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=300, do_sample=False)
    explanation = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return {"explanation": explanation}

# Run the FastAPI app
>>>>>>> Stashed changes
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
