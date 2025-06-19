from pydantic import BaseModel

class ValidationData(BaseModel):
    wallet_name: str
    method: str
    value: str
