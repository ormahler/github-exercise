import os
import requests


class GithubSearchClient:
    GITHUB_SEARCH_PREFIX = "https://api.github.com/search/"

    def __init__(self):
        self.token = os.getenv('GIT_HUB_TOKEN')

    def execute_search_query(self, url: str):
        response = requests.get(url, headers={'Authorization': f'Bearer {self.token}'})
        return response.json()

    def get_rate_limit(self, retries=3):
        for i in range(3):
            try:
                response = requests.get("https://api.github.com/rate_limit", {'Authorization': f'Bearer {self.token}'})
                return response.json()
            except Exception as e:
                if i >= retries - 1:
                    raise e



