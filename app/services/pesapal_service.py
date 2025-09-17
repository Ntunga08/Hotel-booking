from fastapi import HTTPException
import httpx
from typing import Optional

class PesapalService:
    def __init__(self):
        self.consumer_key = "your_pesapal_consumer_key"
        self.consumer_secret = "your_pesapal_consumer_secret"
        self.base_url = "https://pay.pesapal.com/v3"
    
    async def initiate_payment(self, amount: float, description: str, callback_url: str) -> str:
        async with httpx.AsyncClient() as client:
            # Get auth token
            token_response = await client.post(
                f"{self.base_url}/api/Auth/RequestToken",
                json={
                    "consumer_key": self.consumer_key,
                    "consumer_secret": self.consumer_secret
                }
            )
            
            if token_response.status_code != 200:
                raise HTTPException(status_code=400, detail="Failed to authenticate with Pesapal")
            
            token = token_response.json()["token"]
            
            # Submit payment request
            payment_response = await client.post(
                f"{self.base_url}/api/Transactions/SubmitOrderRequest",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "Amount": amount,
                    "Description": description,
                    "CallbackUrl": callback_url,
                    "Currency": "KES"
                }
            )
            
            if payment_response.status_code != 200:
                raise HTTPException(status_code=400, detail="Failed to initiate payment")
            
            return payment_response.json()["redirect_url"]
    
    async def verify_payment(self, merchant_reference: str, tracking_id: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/Transactions/GetTransactionStatus",
                params={
                    "merchantReference": merchant_reference,
                    "pesapalTrackingId": tracking_id
                }
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail="Failed to verify payment")
            
            return response.json()["payment_status"]