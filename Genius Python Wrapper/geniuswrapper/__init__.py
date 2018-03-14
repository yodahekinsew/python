import requests 
import os
import webbrowser as web
from urllib.request import Request, urlopen

authorize_url = 'https://api.genius.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&state={state}&response_type=code'.format(client_id = os.environ['GENIUS_CLIENT_ID'], redirect_uri = os.environ['GENIUS_REDIRECT_URI'], scope = os.environ['GENIUS_SCOPE'], state = 200)

web.open(authorize_url)

code = input("Copy code from redirect URL here: ")

data = {"code": code, "client_id": os.environ['GENIUS_CLIENT_ID'], "client_secret": os.environ['GENIUS_CLIENT_SECRET'], "redirect_uri": os.environ['GENIUS_REDIRECT_URI'], "response_type": "code", "grant_type": "authorization_code"}

response = requests.post('https://api.genius.com/oauth/token', data)

token = response.json()['access_token']


from .geniuspy import Genius

