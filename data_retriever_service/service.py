import os
import pandas as pd
import requests


class RetrieverService():

    def __init__(self) -> None:
        pass

    @staticmethod
    def getCredentials():
        api_key = os.environ['CFBD_DATA_API_KEY']

        return api_key

    @staticmethod
    def checkResponseStatus(response):
        if response.status_code == 200:
            pass
        else:
            error = response.status_code
            print(f"Failed to retrieve endpoint: {error}")

    @staticmethod
    def getConnection(endpoint, parameters):
        base_url = f'https://api.collegefootballdata.com/{endpoint}'
        api_key = RetrieverService.getCredentials()
        headers = {
            "Authorization": f'Bearer {api_key}'
        }

        response = requests.get(base_url, headers=headers, params=parameters)
        RetrieverService.checkResponseStatus(response)

        return response.json()

    @classmethod
    def getPostgresConnection(cls, endpoint, params):
        pass
