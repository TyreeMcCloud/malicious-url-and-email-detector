// 🧠 Get AI Explanation for Email (using selected GPT model)
async function getPhishingExplanation() {
    const emailText = document.getElementById("emailText").value;
    const selectedModel = document.getElementById("modelSelect")?.value || "gpt-3.5-turbo";
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

// 🛡️ Analyze Email for Phishing
async function checkPhishing() {
    const emailText = document.getElementById("emailText").value;
    const outputDiv = document.getElementById("result-box");
    const resultText = document.getElementById("result");

    if (!emailText.trim()) {
        alert("⚠️ Please enter an email to analyze.");
        return;
    }

    outputDiv.classList.remove("hidden");
    resultText.innerText = "🔍 Analyzing email...";

    try {
        const response = await fetch("http://127.0.0.1:8000/detect-phishing", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email_text: emailText })
        });

        const data = await response.json();
        resultText.innerText = `📧 Email: ${data.classification} (Confidence: ${data.confidence.toFixed(2)})`;
    } catch (error) {
        console.error("Error checking phishing:", error);
        resultText.innerText = "❌ Failed to check email.";
    }
}

// 🌐 Check if URL is Malicious
async function checkMalware() {
    let url = document.getElementById("urlInput").value;
    const dropdown = document.getElementById("urlDropdown");

    if (dropdown.value.trim() !== "") {
        url = dropdown.value;
    }

    if (!url.trim()) {
        alert("⚠️ Please enter a URL to analyze.");
        return;
    }

    const outputDiv = document.getElementById("result-box");
    const resultText = document.getElementById("result");

    outputDiv.classList.remove("hidden");
    resultText.innerText = "🔍 Analyzing URL...";

    try {
        const response = await fetch("http://127.0.0.1:8000/detect-malware", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: url })
        });

        const data = await response.json();
        if (data.error) {
            resultText.innerText = `⚠️ Error: ${data.error}`;
        } else {
            resultText.innerText = `🌐 URL: ${data.classification} (Confidence: ${data.confidence.toFixed(2)})`;
        }

        setTimeout(() => {
            document.getElementById("urlInput").value = '';
            dropdown.value = '';
        }, 2000);
    } catch (error) {
        console.error("Error checking URL:", error);
        resultText.innerText = "❌ Failed to check URL.";
    }
}

// 📥 Populate URL Dropdown
async function populateDropdown() {
    const urlDropdown = document.getElementById('urlDropdown');

    try {
        let response = await fetch("http://127.0.0.1:8000/api/urls");
        let data = await response.json();

        urlDropdown.innerHTML = '<option value="">Select a URL...</option>';
        let urls = data.urls.sort(() => 0.5 - Math.random()).slice(0, 50);

        urls.forEach(url => {
            const option = document.createElement('option');
            option.value = url;
            option.textContent = url;
            urlDropdown.appendChild(option);
        });
    } catch (error) {
        console.error("Error fetching URLs:", error);
    }
}

// ⚡ Matrix Background Animation
function startMatrixBackground() {
    const canvas = document.getElementById('matrixCanvas');
    const ctx = canvas.getContext('2d');

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }

    resizeCanvas();
    window.addEventListener("resize", resizeCanvas);

    const chars = "アァイィウエカガキギクグケゲコゴサシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    const fontSize = 14;
    const columns = Math.floor(canvas.width / fontSize);
    const drops = Array(columns).fill(1);

    function drawMatrix() {
        ctx.fillStyle = "rgba(0, 0, 0, 0.05)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = "#0F0";
        ctx.font = `${fontSize}px monospace`;

        for (let i = 0; i < drops.length; i++) {
            const char = chars[Math.floor(Math.random() * chars.length)];
            ctx.fillText(char, i * fontSize, drops[i] * fontSize);

            if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                drops[i] = 0;
            }

            drops[i]++;
        }
    }

    setInterval(drawMatrix, 33);
}

// 🚀 On Load
window.onload = () => {
    populateDropdown();
    startMatrixBackground();
};
