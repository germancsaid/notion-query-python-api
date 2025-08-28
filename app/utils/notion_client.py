import requests

class NotionClient:
    def __init__(self, notion_token, database_id):
        self.notion_token = notion_token
        self.database_id = database_id
        self.base_url = "https://api.notion.com/v1"

    def get_database(self):
        url = f"{self.base_url}/databases/{self.database_id}/query"
        headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Notion-Version": "2021-05-13"
        }
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_page(self, page_id):
        url = f"{self.base_url}/pages/{page_id}"
        headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Notion-Version": "2021-05-13"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()