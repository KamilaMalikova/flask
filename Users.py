from datetime import *
import datetime

class User():

    is_email_confirmed = False
    is_card_confirmed = False

    def __init__(self, id, name, email, phone, **kwargs):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        if not (
                isinstance(id, int) and isinstance(name, str)
                and isinstance(email, str) and isinstance(phone, str)
        ):
            raise TypeError

        if 'card' in kwargs:
            self.card = kwargs['card']
        if 'seller_deals' in kwargs:
            self.seller_deals = kwargs['seller_deals']
        else:
            self.seller_deals = {}

        if 'buyers_deals' in kwargs:
            self.buyer_deals = kwargs['buyer_deals']
        else:
            self.buyer_deals = {}

    def get_user_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_email(self):
        return self.email

    def get_phone(self):
        return self.phone

    def get_seller_deals(self):
        return self.seller_deals

    def get_buyer_deals(self):
        return self.buyer_deals

    def get_card(self):
        return self.card

    def is_card_confirmed(self):
        return self.is_card_confirmed

    def set_card (self, card):
        self.card = card
        self.is_card_confirmed = False

    def confirm_card (self):
        self.is_card_confirmed = True

    def confirm_mail (self):
        self.is_email_confirmed = True

    def register_seller_deal(self, deal):
        if self.seller_deals.get(deal.lot_id) is None and self.buyer_deals.get(deal.lot_id) is None:
            self.seller_deals[deal.lot_id]=deal
        else:
            raise KeyError

    def register_buyers_deal(self, deal):
            if self.buyer_deals.get(deal.lot_id) is None and self.seller_deals.get(deal.lot_id) is None:
                self.buyer_deals[deal.lot_id]=deal
            else:
                raise KeyError

class Card():
    def __init__(self, id, number, three_num, due_date, **kwargs):
        self.id = id
        self.number = number
        if len(str(three_num)) != 3:
            raise ValueError()
        self.three_num = three_num
        if due_date < date.today():
            raise ValueError()
        self.due_date = due_date
        if not (
                isinstance(id, int) and isinstance(number, str)
                and isinstance(three_num, str)
                and isinstance(due_date, datetime.date)
        ):
            raise TypeError


class Deal():
    is_sent = False
    is_delivered = False
    def __init__(self, id, lot_id, auct_id, **kwargs):
        self.id = id
        self.lot_id = lot_id
        self.auct_id = auct_id
        if not (
                isinstance(id, int) and isinstance(lot_id, int)
                and isinstance(auct_id, int)
        ):
            raise TypeError

    def get_deal_id(self):
        return self.id

    def get_lot_id(self):
        return self.lot_id

    def get_auct_id(self):
        return self.auct_id

    def get_is_sent(self):
        return self.is_sent

    def get_is_delivered(self):
        return self.is_delivered

    def confirm_send (self):
        self.is_sent = True

    def confirm_deliverence (self):
        self.is_delivered = True

    def sucsessful_deal (self):
        if self.is_sent and self.is_delivered:
            return True
        else:
            return False

    @staticmethod
    def commission_calculation (price):
        commission = price*0.1
        return commission
