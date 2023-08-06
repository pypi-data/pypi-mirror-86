import json
import requests
from .exceptions import MarketmanAuthenticationFailed


class Marketman:
    """Marketman Instance

    An instance of Marketman is a handy way to wrap a Marketman session
    for easy use of the Marketman REST API.
    """

    def __init__(self, api_key, api_password):
        self.token = self.authenticate(api_key, api_password)
        self.guid = self.get_account()

    def authenticate(self, api_key, api_password):
        url = "https://api.marketman.com/v3/buyers/auth/GetToken"
        headers = {'content-type': "application/json"}
        credentials = {
            "APIKey": api_key,
            "APIPassword": api_password
        }
        response = requests.request("POST", url, data=json.dumps(credentials), headers=headers)
        result = response.json()
        if result.get('IsSuccess', False) is False:
            raise MarketmanAuthenticationFailed(response.status_code, result.get('ErrorMessage'))
        return result.get('Token')

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'AUTH_TOKEN': self.token
        }

    def get_token(self):
        return self.token

    def get_account(self):
        url = "https://api.marketman.com/v3/buyers/partneraccounts/GetAuthorisedAccounts"
        response = requests.request("POST", url, headers=self.get_headers())
        response = response.json()
        return response['Buyers'][0]['Guid']

    def get_items(self):
        url = "https://api.marketman.com/v3/buyers/inventory/GetItems"
        payload = {'BuyerGuid': self.guid}
        response = requests.request("POST", url, headers=self.get_headers(), data=json.dumps(payload))
        return response.json()['InventoryItems']

    def get_vendors(self):
        """Get all vendors"""
        url = "https://api.marketman.com/v3/buyers/items/GetVendors"
        payload = {'BuyerGuid': self.guid}
        response = requests.request("POST", url, headers=self.get_headers(), data=json.dumps(payload))
        return response.json()['Vendors']
