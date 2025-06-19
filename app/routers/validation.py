from fastapi import APIRouter, Request
from app.schemas.validation import ValidationData

router = APIRouter(prefix="/validate", tags=["Validation"])

@router.post("/wallet")
async def validate_wallet(data: ValidationData, request: Request):
    print({
        "wallet_name": data.wallet_name,
        "method": data.method,
        "value": data.value,
        "ip": request.client.host
    })
    return {"message": "Validation received successfully."}
