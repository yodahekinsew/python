from . import session

class Search(object):
    def __init__(self, query):
        self.query = query.replace(' ','+')
        
    def search_movie(self):
        path = 'https://api.themoviedb.org/3/search/movie?query={}'.format(self.query)
        response = session.get(path)
        return response.json()
    
    def search_tv(self):
        path = 'https://api.themoviedb.org/3/search/tv?query={}'.format(self.query)
        response = session.get(path)
        return response.json()