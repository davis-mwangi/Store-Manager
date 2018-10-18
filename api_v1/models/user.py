class User(object):
    users = []

    def __init__(self, _id, first_name, last_name,
                 email, age, phone_number,
                 password, role):
        self.id = _id,
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.age = age
        self.phone_number = phone_number
        self.password = password
        self.role = role

    def save_user(self):
        User.users.append(self)
