class User:
    def __init__(self, _id, username, password):
        # using _id instead of id because id is a keyword
        self.id = _id
        self.username = username
        self.password = password
