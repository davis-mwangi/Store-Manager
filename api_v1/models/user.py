class User(object):
    users = []

    def __init__(self, _id, name, email, username,
                 password, role):
        self.id = _id,
        self.name = name
        self.email = email
        self.username = username
        self.password = password
        self.role = role

    def save_user(self):
        User.users.append(self)
