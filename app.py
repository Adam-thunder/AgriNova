from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# ✅ Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ API Keys (hardcoded for now – move to .env for production!)
GEMINI_API_KEY = "AIzaSyDCH1u8OIhqSYtASdd5zz7iUOePecGZ1_o"
WEATHER_API_KEY = "700807f11c088606d7d40b8ed6402c09"

# ✅ Supported Gemini model
MODEL_NAME = "gemini-2.5-flash"

# -------------------------------
# 🌍 AI Chatbot Endpoint
# -------------------------------
@app.post("/api/ask-ai")
def ask_ai(payload: dict):
    user_query = payload.get("query")
    lang = payload.get("lang", "en")

    if not user_query:
        return {"response": "⚠️ Please enter a question."}

    # Language instructions
    lang_map = {
        "en": "Respond in English.",
        "ta": "Respond in Tamil.",
        "ml": "Respond in Malayalam."
    }
    instruction = lang_map.get(lang, "Respond in English.")

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        body = {
            "contents": [
                {"parts": [{"text": f"{instruction}\n\nUser query: {user_query}"}]}
            ]
        }

        r = requests.post(url, headers=headers, json=body, timeout=20)

        if r.status_code != 200:
            return {"response": f"⚠️ Gemini API error: {r.json().get('error', {}).get('message', 'Unknown error')}."}

        data = r.json()

        # Extract reply safely
        reply = (
            data.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text", None)
        )

        if not reply:
            return {"response": "⚠️ No meaningful reply from Gemini. Try rephrasing your question."}

        return {"response": reply}

    except Exception as e:
        return {"response": f"❌ AI error: {str(e)}"}


# -------------------------------
# 🌦 Weather Endpoint
# -------------------------------
@app.get("/api/weather/{city}")
def get_weather(city: str):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        r = requests.get(url, timeout=10)

        if r.status_code == 404:
            return {"error": f"⚠️ City '{city}' not found."}

        r.raise_for_status()
        data = r.json()

        return {
            "city": data.get("name"),
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"].title(),
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"⚠️ Weather service error: {str(e)}")
    except Exception:
        raise HTTPException(status_code=500, detail="⚠️ Unexpected weather error.")


# -------------------------------
# 🚨 Dam Alerts (Static Example)
# -------------------------------
@app.get("/api/dam-alerts")
def dam_alerts():
    return [
        {"dam": "Idukki", "status": "High inflow, controlled release ongoing"},
        {"dam": "Mullaperiyar", "status": "Water level rising, monitoring closely"},
        {"dam": "Aliyar", "status": "Stable"}
    ]


# -------------------------------
# 🛒 Marketplace (Static Example)
# -------------------------------
@app.get("/api/marketplace")
def marketplace():
    return [
        {"crop": "Tomato", "price": "₹40/kg"},
        {"crop": "Onion", "price": "₹55/kg"},
        {"crop": "Rice", "price": "₹42/kg"}
    ]
