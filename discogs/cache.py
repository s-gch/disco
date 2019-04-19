"""
    Discogs data cache/proxy
"""

from discogs import interface

class Cache:
    def __init__(self):
        self.artists = dict()

    def get_artist(self, artistId):
        if artistId not in self.artists:
            artist = interface.instance().get_artist(artistId)
            self.artists[artistId] = artist
            return artist
        return self.artists[artistId]

def instance():
    try:
        return instance.cache
    except AttributeError:
        instance.cache = Cache()
        return instance.cache
