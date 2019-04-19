"""
    Discogs' types
"""

class Release:
    def __init__(self, json):
        self.instanceId = json['instance_id']
        self.rating = json['rating']
        basic_info = json['basic_information']
        self.labels = [Label(label) for label in basic_info['labels']]
        self.year = basic_info['year']
        self.artists = [Artist(artist) for artist in basic_info['artists']]
        self.id = basic_info['id']
        self.thumbUrl = basic_info['thumb']
        self.title = basic_info['title']
        """ formats ignored for now """
        self.coverUrl = basic_info['cover_image']
        self.masterId = basic_info['master_id']
        self.incomplete = True

class Collection:
    def __init__(self, json):
        self.page = json['pagination']['page']
        self.pages = json['pagination']['pages']
        self.releases = [Release(rel) for rel in json['releases']]

    def loading_done(self):
        return self.page == self.pages

class Artist:
    def __init__(self, json):
        self.name = json['name']
        self.artistId = json['id']
        self.incomplete = True

class Label:
    def __init__(self, json):
        self.name = json['name']
        self.id = json['id']
        self.incomplete = True
