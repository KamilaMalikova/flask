import unittest

from Dependency.BuyerDealDependency import *
from service import DealService


class Test_Buyer_Deal(unittest.TestCase):

    def test_buyer_deal_registration(self):
        db = Database()
        bank_service = BankService()
        auction_service = AuctionService()
        buyer_deal = DealService(db, bank_service, auction_service)
        self.assertTrue(buyer_deal.register_buyer_deal(1, 1, 1))
        # check user_id  in db.get_user_by_id(user_id)
        self.assertEqual(1, db.current_int)
        # check auct_id, lot_id  in auction_service.is_lot_valid(auct_id, lot_id)
        self.assertEqual(1, auction_service.current_auction_id)
        self.assertEqual(1, auction_service.current_lot_id)
        # check lot_id in  auction_service.get_lot_cost(lot_id)
        self.assertEqual(1, auction_service.current_lot_id_cost)
        # check card in bank_service.pay(card)
        self.assertEqual(1, bank_service.current_card.id)
        self.assertEqual("1111111111111111", bank_service.current_card.number)
        self.assertEqual("111", bank_service.current_card.three_num)
        # check deal, user in db.save_deal(deal, user)
        self.assertEqual(1, db.current_deal.get_lot_id())
        self.assertEqual(1, db.current_deal.get_auct_id())
        self.assertEqual("user1", db.current_user.get_name())
        self.assertEqual("user1@gmail.com", db.current_user.get_email())

    def test_buyer_deal_registration_if_user_not_found(self):
        db = Database()
        bank_service = BankService()
        auction_service = AuctionService()

        buyer_deal = DealService(db, bank_service, auction_service)

        with self.assertRaises(ValueError) as cm:
            buyer_deal.register_buyer_deal(8, 1, 1)
        self.assertEqual(
            'Пользователь не найден',
            str(cm.exception)
        )
        # check user_id  in db.get_user_by_id(user_id)
        self.assertEqual(8, db.current_int)

    def test_buyer_deal_registration_if_lot_is_not_valid(self):
        db = Database()
        bank_service = BankService()
        auction_service = AuctionServiceNotValid()
        buyer_deal = DealService(db, bank_service, auction_service)
        with self.assertRaises(ValueError) as cm:
            buyer_deal.register_buyer_deal(1, 1, 1)
        self.assertEqual(
            'Лот не найден',
            str(cm.exception)
        )
        # check user_id  in db.get_user_by_id(user_id)
        self.assertEqual(1, db.current_int)
        # check auct_id, lot_id  in auction_service.is_lot_valid(auct_id, lot_id)
        self.assertEqual(1, auction_service.current_auction_id)
        self.assertEqual(1, auction_service.current_lot_id)

    def test_confirm_item_receive(self):
        db = Database()
        bank_service = BankService()
        auction_service = AuctionService()
        buyer_deal = DealService(db, bank_service, auction_service)
        self.assertTrue(buyer_deal.confirm_item_received(1, 2))
        # check user_id in db.get_user_by_id(user_id)
        self.assertEqual(1, db.current_int)
        # check lot_id in db.get_seller_by_deal_lot(lot_id)
        self.assertEqual(2, db.current_lot_id)
        # check lot_id in auction_service.get_lot_cost(lot_id)
        self.assertEqual(2, auction_service.current_lot_id_cost)
        # check card in  bank_service.pay_back(seller.get_card(), )
        self.assertEqual(2, bank_service.current_back_card.id)
        self.assertEqual("2222222222222222", bank_service.current_back_card.number)
        self.assertEqual("222", bank_service.current_back_card.three_num)

    def test_confirm_item_receive_if_deal_not_found(self):
        db = Database()
        bank_service = BankService()
        auction_service = AuctionService()
        buyer_deal = DealService(db, bank_service, auction_service)

        with self.assertRaises(ValueError) as cm:
            buyer_deal.confirm_item_received(2, 2)
        self.assertEqual(
            "Значение не найдено",
            str(cm.exception)
        )
        # check user_id in db.get_user_by_id(user_id)
        self.assertEqual(2, db.current_int)
        # check lot_id in db.get_seller_by_deal_lot(lot_id)
        self.assertEqual(2, db.current_lot_id)