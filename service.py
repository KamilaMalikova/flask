from Users import *


class RegistrationService:
    def __init__(self, data_base, bank_service, mail_service):
        self.db = data_base
        self.bank_service = bank_service
        self.mail_service = mail_service

    def registration(self, username, phone, email):
        user = User(-1, username, email, phone)
        if not self.db.is_new(user):
            raise ValueError("Данный пользователь уже зарегестрирован в системе")
        else:
            user = self.db.save(user)
            self.mail_service.send(user)
        return user.id

    def confirm_mail(self, email, key):
        user = self.db.get_user_by_email(email)
        if user is None:
            raise ValueError('Пользователь не существует')

        if self.mail_service.get_key(user) == key:
            user.confirm_mail()
            self.db.save_mail_confirmation(user)
            return True
        else:
            return False

    def confirm_bank_card(self, user_id, number, three_num, due_date):
        card = Card(user_id, number, three_num, due_date)
        user = self.db.get_user_by_id(user_id)
        if user is None:
            raise ValueError('Пользователь не существует')
        user.set_card(user)
        self.db.save_user_card(user.get_card())
        if self.bank_service.pay(card, 1):
            self.bank_service.pay_back(card, 1)
            user.confirm_card()
            self.db.save_user_card(user)
            return True
        else:
            return False


class DealService:

    def __init__(self, data_base, bank_service, auction_service):
        self.db = data_base
        self.bank_service = bank_service
        self.auction_service = auction_service

    def register_seller_deal(self, user_id, lot_id, auct_id):
        deal = Deal(-1, lot_id, auct_id)
        user = self.db.get_user_by_id(user_id)
        if user is None:
            raise ValueError('Пользователь не найден')
        if self.auction_service.is_lot_valid(auct_id, lot_id):
            user.register_seller_deal(deal)
            self.db.save_deal(deal, user)
            return id
        else:
            raise ValueError("Лот не действителен")

    def register_buyer_deal(self, user_id, lot_id, auct_id):
        deal = Deal(-1, lot_id, auct_id)
        user = self.db.get_user_by_id(user_id)
        if user is None:
            raise ValueError('Пользователь не найден')
        if self.auction_service.is_lot_valid(auct_id, lot_id):
            user.register_buyers_deal(deal)
            self.bank_service.pay(user.get_card(), self.auction_service.get_lot_cost(lot_id))
            self.db.save_deal(deal, user)
            return id
        else:
            raise ValueError("Лот не найден")

    def confirm_item_send(self, user_id, lot_id):
        seller = self.db.get_user_by_id(user_id)
        deal = seller.get_seller_deals().get(lot_id)
        if deal is None:
            raise ValueError("Недействитльный договор")
        deal.confirm_send()
        self.db.save_deal(deal, seller)
        return deal.get_is_sent()

    def confirm_item_received(self, user_id, lot_id):
        buyer = self.db.get_user_by_id(user_id)
        seller = self.db.get_seller_by_deal_lot(lot_id)
        deal = buyer.get_buyer_deals().get(lot_id)
        if deal is None or seller is None:
            raise ValueError("Значение не найдено")
        deal.confirm_deliverence()
        self.bank_service.pay_back(seller.get_card(), self.auction_service.get_lot_cost(lot_id))
        self.db.save_deal(deal)
        return deal.get_is_delivered()
