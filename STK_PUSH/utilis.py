import requests
from django.conf import settings

def get_pesapal_access_token():
    url = f"{settings.PESAPAL_API_BASE_URL}/Auth/RequestToken"
    headers = {"Content-Type": "application/json"}
    data = {
        "consumer_key": settings.PESAPAL_CONSUMER_KEY,
        "consumer_secret": settings.PESAPAL_CONSUMER_SECRET
    }

    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("token")
    else:
        return None
