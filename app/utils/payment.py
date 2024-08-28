import requests

from app.config.config import settings


def accept_payments(email: str, amount: str):
    url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }
    data = {
        "email": email,
        "amount": amount,  # amount should be multiplied by 100  if currency is in GHS
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        return response.json()["data"]["authorization_url"]
    except requests.exceptions.HTTPError as e:
        return None
