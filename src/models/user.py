class User:
    def __init__(self, user_id, username, password=None):
        self.id = user_id
        self.username = username
        self.password = password  # Usually, don't store plain passwords. Kept simple here.

    @classmethod
    def from_dict(cls, data):
        return cls(data['id'], data['username'], data.get('password'))

    def __str__(self):
        return f"User({self.id}, {self.username})"
