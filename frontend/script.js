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
    let url = document.getElementById("urlInput").value; // Get custom URL input value
    const dropdown = document.getElementById("urlDropdown");

    // Check if the user selected a URL from the dropdown
    if (dropdown.value.trim() !== "") {
        url = dropdown.value; // If selected, use the dropdown value
    }

    // If neither URL is provided
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

    // Delay clearing the input fields
    setTimeout(() => {
        document.getElementById("urlInput").value = ''; // Clear custom URL input
        dropdown.value = ''; // Reset dropdown to default value
    }, 2000); // Delay of 2000ms (2 seconds)
}



async function populateDropdown() {
    const urlDropdown = document.getElementById('urlDropdown');

    try {
        let response = await fetch("http://127.0.0.1:8000/api/urls");
        let data = await response.json();

        // Clear existing options
        urlDropdown.innerHTML = '<option value="">Select a URL...</option>';

        // Shuffle and select 50 random URLs
        let urls = data.urls.sort(() => 0.5 - Math.random()).slice(0, 50);

        // Populate dropdown with the selected URLs
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

// Load URLs when the page loads
window.onload = populateDropdown;

