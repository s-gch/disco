"""
    Settings for Discogs connection
"""

class Settings:
    def __init__(self):
        self.userName = None
        self.userToken = None

    def set_user_name(self, userName):
        self.userName = userName

    def set_user_token(self, userToken):
        self.userToken = userToken

def instance():
    try:
        return instance.settings
    except AttributeError:
        instance.settings = Settings()
        return instance.settings
