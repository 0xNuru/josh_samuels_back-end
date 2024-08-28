import requests

from app.config.config import settings


def accept_payments(email, amount, order_id) -> str:
    url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "email": email,
        "amount": amount,
        "reference": order_id,
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["data"]["authorization_url"]
    except requests.exceptions.HTTPError as e:
        return None
