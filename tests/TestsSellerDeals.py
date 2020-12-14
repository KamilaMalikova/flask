import unittest

from Dependency.SellerDealDependency import *
from service import DealService


class Test_SellerDeal(unittest.TestCase):

    def test_seller_deal_registration(self):
        db = Database()
        bank_service = BankService()
        auction_service = AuctionService()
        seller_deal = DealService(db, bank_service, auction_service)
        self.assertTrue(seller_deal.register_seller_deal(1, 1, 1))
        # check user_id  in db.get_user_by_id(user_id)
        self.assertEqual(1, db.current_int)
        # check auct_id, lot_id  in auction_service.is_lot_valid(auct_id, lot_id)
        self.assertEqual(1, auction_service.current_auction_id)
        self.assertEqual(1, auction_service.current_lot_id)
        # check deal, user in db.save_deal(deal, user)
        self.assertEqual(1, db.current_deal.get_lot_id())
        self.assertEqual(1, db.current_deal.get_auct_id())
        self.assertEqual("user1", db.current_user.get_name())
        self.assertEqual("user1@gmail.com", db.current_user.get_email())

    def test_seller_deal_registration_if_user_is_not_found(self):
        db = Database()
        bank_service = BankService()
        auction_service = AuctionService()

        seller_deal = DealService(db, bank_service, auction_service)

        with self.assertRaises(ValueError) as cm:
            seller_deal.register_seller_deal(8, 1, 1)
        self.assertEqual(
            'Пользователь не найден',
            str(cm.exception)
        )
        # check user_id  in db.get_user_by_id(user_id)
        self.assertEqual(8, db.current_int)


    def test_seller_deal_registration_if_lot_is_not_valid(self):
        db = Database()
        bank_service = BankService()
        auction_service = AuctionServiceNotValid()

        seller_deal = DealService(db, bank_service, auction_service)

        with self.assertRaises(ValueError) as cm:
            seller_deal.register_seller_deal(1, 1, 1)
        self.assertEqual(
            'Лот не действителен',
            str(cm.exception)
        )
        # check user_id  in db.get_user_by_id(user_id)
        self.assertEqual(1, db.current_int)
        # check auct_id, lot_id  in auction_service.is_lot_valid(auct_id, lot_id)
        self.assertEqual(1, auction_service.current_auction_id)
        self.assertEqual(1, auction_service.current_lot_id)

    def test_confirm_item_send(self):
        db = Database()
        bank_service = BankService()
        auction_service = AuctionService()
        seller_deal = DealService(db, bank_service, auction_service)
        self.assertTrue(seller_deal.confirm_item_send(2, 2))
        # check user_id  in db.get_user_by_id(user_id)
        self.assertEqual(2, db.current_int)
        # check deal in db.save_deal(deal)
        self.assertEqual(2, db.current_deal.get_auct_id())
        self.assertEqual(2, db.current_deal.get_lot_id())
        self.assertEqual(2, db.current_deal.get_deal_id())

    def test_confirm_item_send_if_deal_is_not_fount(self):
        db = Database()
        bank_service = BankService()
        auction_service = AuctionService()
        seller_deal = DealService(db, bank_service, auction_service)
        with self.assertRaises(ValueError) as cm:
            seller_deal.confirm_item_send(1, 2)
        self.assertEqual(
            "Недействитльный договор",
            str(cm.exception)
        )
        # check user_id  in db.get_user_by_id(user_id)
        self.assertEqual(1, db.current_int)

