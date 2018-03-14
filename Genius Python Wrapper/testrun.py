from __future__ import print_function
from geniuswrapper import Genius

genius = Genius()

kendrick_songs = genius.search('All the Stars')

for i in kendrick_songs['response']['hits']:
    print(i['result']['title'])