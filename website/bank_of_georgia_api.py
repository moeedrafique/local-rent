# tbcbank_integration/utils.py

import requests
from django.conf import settings

TBC_API_BASE_URL = "https://api.tbcbank.ge/v1"


def make_tbcbank_api_request(endpoint, method='GET', data=None):
    url = f"{TBC_API_BASE_URL}/{endpoint}"
    headers = {
        'Authorization': f'Bearer {settings.TBC_API_KEY}',
        'Content-Type': 'application/json',
    }

    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=data)
        else:
            # Handle other HTTP methods as needed
            pass

        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        return response.json() if response.status_code == 200 else None
    except requests.exceptions.RequestException as e:
        # Log the error or handle it appropriately
        print(f"Error making TBC Bank API request: {e}")
        return None