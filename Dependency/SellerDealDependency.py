from datetime import date

from Users import Card, User, Deal


class Database:
    def __init__(self):
        self.users = []
        kwargs1 = {"card": Card(1, "1111111111111111", "111", date.fromisocalendar(2021, 1, 1))}
        kwargs2 = {"card": Card(2, "2222222222222222", "222", date.fromisocalendar(2021, 1, 1))}

        deal2 = Deal(2, 2, 2)

        user1 = User(1, "user1", "user1@gmail.com", "+000000000000", **kwargs1)
        user2 = User(2, "user2", "user2@gmail.com", "+222222222222", **kwargs2)

        user2.register_seller_deal(deal2)
        user1.register_buyers_deal(deal2)

        self.users.append(user1)
        self.users.append(user2)

    def get_user_by_id(self, _id):
        self.current_int = _id
        for user in self.users:
            if user.id == _id:
                return user

    def save_deal(self, deal, user):
        self.current_deal = deal
        self.current_user = user


class BankService:
    pass


class AuctionService:

    def is_lot_valid(self, auction_id, lot_id):
        self.current_auction_id = auction_id
        self.current_lot_id = lot_id
        return True


class AuctionServiceNotValid:

    def is_lot_valid(self, auction_id, lot_id):
        self.current_auction_id = auction_id
        self.current_lot_id = lot_id
        return False