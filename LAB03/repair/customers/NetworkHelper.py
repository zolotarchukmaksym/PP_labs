import requests
from requests.auth import HTTPBasicAuth

class NetworkHelper:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password

    def get_items(self):
        response = requests.get(f"{self.base_url}/api/customers/", auth=HTTPBasicAuth(self.username, self.password))
        if response.status_code == 200:
            return response.json()
        return []

    def get_item_by_id(self, item_id):
        response = requests.get(f"{self.base_url}/api/customers/{item_id}/", auth=HTTPBasicAuth(self.username, self.password))
        if response.status_code == 200:
            return response.json()
        return None

    def create_item(self, item_data):
        response = requests.post(f"{self.base_url}/api/customers/", json=item_data, auth=HTTPBasicAuth(self.username, self.password))
        if response.status_code == 201:
            return response.json()
        return None

    def update_item(self, item_id, item_data):
        response = requests.put(f"{self.base_url}/api/customers/{item_id}/", json=item_data, auth=HTTPBasicAuth(self.username, self.password))
        if response.status_code == 200:
            return response.json()
        return None

    def delete_item(self, item_id):
        response = requests.delete(f"{self.base_url}/api/customers/{item_id}/", auth=HTTPBasicAuth(self.username, self.password))
        return response.status_code == 204