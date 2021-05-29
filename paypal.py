import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
load_dotenv()

PAYPAL_OAUTH_API = 'https://api-m.paypal.com/v1/oauth2/token/';
PAYPAL_ORDER_API = 'https://api-m.paypal.com/v2/checkout/orders/';

def get_token():
    return requests.post(PAYPAL_OAUTH_API, data="grant_type=client_credentials", auth=HTTPBasicAuth(os.getenv('PAYPAL_CLIENT'), os.getenv('PAYPAL_SECRET'))).json()["access_token"]

def build_request_body():
  """Method to create body with a custom PAYEE (receiver)"""
  return \
    {
      "intent": "CAPTURE",
      "purchase_units": [
        {
          "amount": {
            "currency_code": "USD",
            "value": "1.00"
          },
          "payee": {
            "email_address": "petkanicsandra@gmail.com"
          }
        }
      ]
    }

def send_payment():
    headers = {"Authorization": "Bearer "+get_token(), "Accept": "application/json"}
    return requests.post(PAYPAL_ORDER_API, headers=headers, json=build_request_body()).json()
