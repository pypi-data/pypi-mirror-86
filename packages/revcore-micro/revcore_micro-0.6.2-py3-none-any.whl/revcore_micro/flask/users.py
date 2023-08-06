class User:
    def __init__(self, user, client_class):
        self._meta = user
        self.client = client_class.get(id=user['aud'])
        self.groups = user['grp'].split(':')
        self.sub = user['sub']

    def __getattr__(self, value):
        if value.startswith('is_'):
            return value[3:] in self.groups
        return getattr(self.__class__, value)

    def __getitem__(self, key):
        return self._meta[key]
