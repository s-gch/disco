"""
Discogs API access class
"""
import requests

from discogs.types import Collection, Artist
from discogs import settings

class Discogs:
    USER_AGENT = 'DiscoDesktopClient/0,1 +https://github.com/s-gch/disco'
    URL_BASE = 'https://api.discogs.com/'
    def __init__(self):
        self.headers = {'user-agent': Discogs.USER_AGENT,
                        'Authorization': 'Discogs token={0}'.format(settings.instance().userToken)}

    def run_query(self, query, parameters=None):
            #print('Querying: {}'.format(Discogs.URL_BASE + query))
        answer = requests.get(Discogs.URL_BASE + query, headers=self.headers, params=parameters)
        remaining = int(answer.headers['X-Discogs-Ratelimit-Remaining'])
        print('X-Discogs-Ratelimit-Remaining: {}'.format(remaining))
        return answer.json()

    def run_collection_query(self, query, parameters=None):
        return self.run_query('users/' + settings.instance().userName + '/collection/' + query, parameters)

    def get_collection_value(self):
        return self.run_collection_query('value')

    def get_collections(self):
        return self.run_collection_query('folders')

    def get_collection(self, collectionId):
        return Collection(self.run_collection_query('folders/{}/releases'.format(collectionId)))

    def get_artist(self, artistId):
        return Artist(self.run_query('artists/{}'.format(artistId)))

def instance():
    try:
        return instance.discogs
    except AttributeError:
        instance.discogs = Discogs()
        return instance.discogs
