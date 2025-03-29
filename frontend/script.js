// 💥 Phishing AI Explanation (w/ GPT Model Selection)
async function getPhishingExplanation() {
    const emailText = document.getElementById("emailText").value;
    const selectedModel = document.getElementById("modelSelect").value;
    const outputDiv = document.getElementById("explanationOutput");

    if (!emailText.trim()) {
        alert("⚠️ Please enter email text first.");
        return;
    }

    outputDiv.classList.remove("hidden");
    outputDiv.innerText = "⏳ Generating explanation...";

    try {
        const response = await fetch("http://127.0.0.1:8000/explain-phishing", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email_text: emailText, model: selectedModel })
        });

        const data = await response.json();
        outputDiv.innerText = data.explanation || "⚠️ No explanation returned.";
    } catch (error) {
        console.error("Error getting explanation:", error);
        outputDiv.innerText = "❌ Failed to generate explanation.";
    }
}
