function displayResult(message) {
    let resultBox = document.getElementById("result-box");
    let resultText = document.getElementById("result");

    resultText.innerText = message;
    resultBox.classList.remove("hidden");
}

// Function to escape HTML entities
function escapeHTML(input) {
    const div = document.createElement('div');
    div.innerText = input;
    return div.innerHTML;
}

async function checkPhishing() {
    let emailText = document.getElementById("emailText").value;
    
    if (!emailText.trim()) {
        alert("⚠️ Please enter email text to analyze.");
        return;
    }

    // Escape the input
    let escapedEmailText = escapeHTML(emailText);

    try {
        let response = await fetch("http://127.0.0.1:8000/detect-phishing", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email_text: escapedEmailText })
        });

        if (!response.ok) {
            throw new Error(`Server responded with status: ${response.status}`);
        }

        let data = await response.json();
        displayResult(`📧 Email: ${data.classification} (Confidence: ${data.confidence})`);
    } catch (error) {
        console.error("Error during fetch operation:", error);
        alert("An error occurred while analyzing the email. Please try again.");
    }
}

async function checkMalware() {
    let url = document.getElementById("urlInput").value;

    if (!url.trim()) {
        alert("⚠️ Please enter a URL to analyze.");
        return;
    }

    let response = await fetch("http://127.0.0.1:8000/detect-malware", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: url })
    });

    let data = await response.json();

    if (data.error) {
        displayResult(`⚠️ Error: ${data.error}`);
    } else {
        displayResult(`🌐 URL: ${data.classification} (Confidence: ${data.confidence})`);
    }
}

