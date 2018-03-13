from __future__ import print_function
from tmdbwrapper import TV, Movie, Search

popular = Movie.popular()

for number, show in enumerate(popular['results'], start = 1):
    print("{num}. {name} - {pop}".format(num = number, name = show['title'], pop = show['popularity']))
    
a = TV(1396)
print(a.info()['name'])

responses = Search("The Big").search_tv()['results']
for number, result in enumerate(responses, start = 1):
    print("{num}. {name}".format(num = number, name = result['name']))
