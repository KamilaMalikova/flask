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

    def get_seller_by_deal_lot(self, lot_id):
        self.current_lot_id = lot_id
        for user in self.users:
            deal = user.get_seller_deals().get(lot_id)
            if deal is not None:
                return user
        return None

    def save_deal(self, deal, user):
        self.current_deal = deal
        self.current_user = user


class BankService:
    def pay(self, card, amount):
        self.current_card = card
        self.current_amount = amount
        return True

    def pay_back(self, card, amount):
        self.current_back_card = card
        self.current_back_amount = amount
        return True

    def freeze(card, amount):
        pass

    def unfreeze(card, amount):
        pass


class AuctionService:

    def is_lot_valid(self, auction_id, lot_id):
        self.current_auction_id = auction_id
        self.current_lot_id = lot_id
        return True

    def get_lot_cost(self, lot_id):
        self.current_lot_id_cost = lot_id
        return 5


class AuctionServiceNotValid:

    def is_lot_valid(self, auction_id, lot_id):
        self.current_auction_id = auction_id
        self.current_lot_id = lot_id
        return False