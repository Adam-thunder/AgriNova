const API_BASE = "http://127.0.0.1:8000";  // backend URL

// -------------------------
// 🌍 AI Chatbot
// -------------------------
async function askAI() {
    const query = document.getElementById("userInput").value.trim();
    const lang = document.getElementById("langSelect").value;
    const chatBox = document.getElementById("chatBox");

    if (!query) {
        chatBox.innerHTML += `<div class="error">⚠️ Please enter a question.</div>`;
        return;
    }

    chatBox.innerHTML += `<div class="user-msg">👤 ${query}</div>`;

    try {
        const res = await fetch(`${API_BASE}/api/ask-ai`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query, lang })
        });

        const data = await res.json();
        chatBox.innerHTML += `<div class="ai-msg">🤖 ${data.response}</div>`;
    } catch (err) {
        chatBox.innerHTML += `<div class="error">❌ AI Error: ${err.message}</div>`;
    }
}

// -------------------------
// 🌦 Weather
// -------------------------
async function getWeather() {
    const city = document.getElementById("cityInput").value.trim();
    const weatherBox = document.getElementById("weatherBox");

    if (!city) {
        weatherBox.innerHTML = "⚠️ Enter a city name.";
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/api/weather/${city}`);
        const data = await res.json();

        if (data.error) {
            weatherBox.innerHTML = data.error;
        } else {
            weatherBox.innerHTML = `
                <h3>${data.city}</h3>
                🌡 Temp: ${data.temperature}°C<br>
                ☁️ Condition: ${data.description}<br>
                💧 Humidity: ${data.humidity}%<br>
                🌬 Wind: ${data.wind_speed} m/s
            `;
        }
    } catch (err) {
        weatherBox.innerHTML = `❌ Weather error: ${err.message}`;
    }
}

// -------------------------
// 🚨 Dam Alerts
// -------------------------
async function loadDamAlerts() {
    const damBox = document.getElementById("damBox");

    try {
        const res = await fetch(`${API_BASE}/api/dam-alerts`);
        const data = await res.json();

        damBox.innerHTML = data.map(
            dam => `<div>🏞 <b>${dam.dam}</b>: ${dam.status}</div>`
        ).join("");
    } catch (err) {
        damBox.innerHTML = `❌ Dam alerts error: ${err.message}`;
    }
}

// -------------------------
// 🛒 Marketplace
// -------------------------
async function loadMarketplace() {
    const marketBox = document.getElementById("marketBox");

    try {
        const res = await fetch(`${API_BASE}/api/marketplace`);
        const data = await res.json();

        marketBox.innerHTML = data.map(
            item => `<div>🌾 <b>${item.crop}</b>: ${item.price}</div>`
        ).join("");
    } catch (err) {
        marketBox.innerHTML = `❌ Marketplace error: ${err.message}`;
    }
}

// -------------------------
// 📌 Load on startup
// -------------------------
window.onload = () => {
    loadDamAlerts();
    loadMarketplace();
};
