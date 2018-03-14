from . import token
import requests 
import os
import webbrowser as web
from urllib.request import Request, urlopen

class Genius():
    def __init__(self):
        self.base_url = "https://api.genius.com/"
    
    def format_path(self,path):
        request = Request(path)
        request.add_header('Authorization', 'Bearer ' + token)
        request.add_header("user-Agent", "")
        return request
    
    def format_request(self, request):
        false, true, null = False, True, None
        response = urlopen(request)
        raw = response.read().decode('utf-8')
        page = eval(raw)
        return page
    
    def search(self, query):
        path = self.base_url + "search?q={}".format(query.replace(" ","%20"))  
        request = self.format_path(path)
        page = self.format_request(request)
        return page
    
    def get_id(self, query):
        page = self.search(query)
        return page['response']['hits'][0]['id']
    
    def get_artist_info(self, id):
        path = self.base_url + "artists/{}".format(id)
        request = self.format_path(path)
        page = self.format_request(request)
        return page
    
    def get_artist_songs(self, id):
        path = self.base_url + "artists/{}/songs".format(id)
        request = self.format_path(path)
        page = self.format_request(request)
        return page
    
    def get_song(self, id):
        path = self.base_url + "songs/{}".format(id)
        request = self.format_path(path)
        page = self.format_request(request)
        return page
    
    def get_song_info(self, id):
        path = self.base_url + "referents?song_id={}".format(id)
        request = self.format_path(path)
        page = self.format_request(request)
        return page
    
            