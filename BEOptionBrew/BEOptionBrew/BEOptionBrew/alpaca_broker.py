# Broker Utility Classes to sign users up, execute positions, and more... 
import os
import requests
import random
import datetime
import base64
from .models import User
from dotenv import load_dotenv


class AlpacaAPI:
    def __init__(self):
        load_dotenv()
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Basic {encoded_credentials}"
        }
        
    def _send_request(self, method, endpoint, data=None):
        response = requests.request(method, url, json=data, headers=self.headers)
        if response.status_code in [200, 201]:
            return Response({"API Call Success": "_send_request received 200 or 201"}, status=status.HTTP_200__OK )
        else:
            # Log detailed error information
            raise Exception(f"API request failed: {response.status_code} {response.text}")


class Users(AlpacaAPI):
    def registerUser(self, first_name, last_name, email, phone_number):
        response = self._send_request('post', endpoint, data=alpaca_formatted_data)
        
        if response and 'id' in response:
            user = User.objects.get(phone_number=phone_number)
            user.alpaca_account_id = response['id']
            user.save()
            return response['id']  # Return the Alpaca account ID
        else:
            raise Exception("Failed to create Alpaca account or retrieve account ID.")

    def _transform_data_to_alpaca_format(self, user_data):
        alpaca_payload = {
            "contact": {
                "email_address": user_data["email"],
                "phone_number": user_data['phone_number'],
                "street_address": ["123 Fake Street"],
                "unit": "string",
                "city": "Faketown",
                "state": "CA",
                "postal_code": "90210"
            },
            "identity": {
                "tax_id_type": "USA_SSN",
                "given_name": user_data["first_name"],
                "family_name": user_data["last_name"],
                "date_of_birth": "1990-01-01",
                "tax_id": dummy_ssn,
                "country_of_citizenship": "USA",
                "country_of_birth": "USA",
                "country_of_tax_residence": "USA",
                "funding_source": ["employment_income"]
            },
            "disclosures": {
                "is_control_person": False,
                "is_affiliated_exchange_or_finra": False,
                "is_politically_exposed": False,
                "immediate_family_exposed": False
            },
            "trusted_contact": {
                "given_name": "Jane",
                "family_name": "Doe",
                "email_address": "jane.doe@example.com"
            },
            "agreements": [
                {
                    "agreement": "customer_agreement",
                    "signed_at": dummy_date,
                    "ip_address": "192.0.2.1"
                }
            ],
            "documents": [
                {
                    "document_type": "identity_verification",
                    "document_sub_type": "passport",
                    "content": "/9j/Cg==",
                    "mime_type": "image/jpeg"
                }
            ],
            "enabled_assets": ["us_equity"]
        }
        return alpaca_payload

    def create_ach_relationship(self, account_id, first_name): 
        endpoint = f'{self.base_url}/v1/accounts/{account_id}/relationships'
        data = {
                "bank_account_type": "CHECKING", 
                "account_owner_name": first_name,
                "bank_account_number": "123456",
                "bank_routing_number": "123456780",
               }

        request_status = self._send_request('post', endpoint, data=data)

        if response_status.status == status.HTTP_200_OK: 
            return Response(
                            {
                             "ACH Relationship created": "ACH Relationship created successfully",
                             "Data": response_status.data
                            }, 
                            status=status.HTTP_201_CREATED)
            
    def fetch_balance(self, account_id): 
        endpoint = f'{self.base_url}/v1/accounts/{account_id}/transfers'
        data = {
                "transfer_type": "ach",
                "direction": "INCOMING",
                "timing": "immediate"
            }
        self._send_request('post', endpoint, )
        
class Trades(AlpacaAPI):
    def open_position(self, symbol, qty, side, type='market', time_in_force='gtc'):
        alpaca_account_id = 0
        data = {
            "symbol": symbol,
            "qty": qty,
            "side": side,  # "buy" or "sell"
            "type": type,  # "market", "limit", etc.
            "time_in_force": time_in_force  # "day", "gtc", etc.
        }

        response = self._send_request('post', endpoint, data=data)

        if response and 'id' in response:
            return response['id']  # Return the order ID
        else:
            raise Exception("Failed to open position.")

    def close_position(self, symbol, qty, side, type='market', time_in_force='gtc'):
        # For closing a position, you can use similar logic as opening a position
        return self.open_position(symbol, qty, side, type, time_in_force)
