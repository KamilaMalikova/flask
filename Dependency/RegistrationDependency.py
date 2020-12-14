from datetime import date

from Users import Card, User


class Database:
    def __init__(self):
        self.users = []
        self.confirmed = {}
        kwargs1 = {"card": Card(0, "111111111111111", "111", date.fromisocalendar(2021, 1, 1))}
        user1 = User(0, "user1", "user1@gmail.com", "+111111111111", **kwargs1)
        self.users.append(user1)

    def is_new(self, user):
        self.current_user = user
        for db_user in self.users:
            if user.get_name() == db_user.get_name() or user.get_email() == db_user.get_email():
                return False
        return True

    def save(self, user):
        user.id = len(self.users)
        self.users.append(user)
        return user

    def get_user_by_email(self, email):
        self.current_str = email
        for user in self.users:
            if user.get_email() == email:
                return user

    def save_mail_confirmation(self, user):
        self.current_user = user
        self.confirmed[user] = True

    def get_user_by_id(self, _id):
        self.current_int = _id
        for user in self.users:
            if user.id == _id:
                return user

    def save_user_card(self, user):
        self.current_user = user
        pass

    def save_card(self, card):
        self.current_card = card
        pass


class MailService:

    def __init__(self):
        self.users = []

    def send(self, user):
        self.users.append(user)

    def get_key(self, user):
        self.current_user = user
        return user.get_name()


class MailServiceDifferentKey:

    def __init__(self):
        self.users = []

    def send(self, user):
        self.users.append(user)

    def get_key(self, user):
        self.current_user = user
        return "key"

class BankService:
    def __init__(self):
        pass

    def pay(self, card, amount):
        self.current_card = card
        self.current_amount = amount
        return True

    def pay_back(self, card, amount):
        self.current_back_card = card
        self.current_back_amount = amount
        return True
