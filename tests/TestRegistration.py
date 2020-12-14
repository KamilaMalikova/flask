import unittest
from datetime import date

from Dependency.RegistrationDependency import Database
from Dependency.RegistrationDependency import BankService
from Dependency.RegistrationDependency import MailService
from Dependency.RegistrationDependency import MailServiceDifferentKey
from service import RegistrationService


class Test_Registration(unittest.TestCase):

    def test_user_registration(self):
        db = Database()
        bank_service = BankService()
        mail_service = MailService()

        registration = RegistrationService(db, bank_service, mail_service)
        self.assertEqual(1, registration.registration("user", "+555555555555", "user@gmail.com"))
        # check user in db.is_new(user)
        self.assertEqual("user", db.current_user.get_name())
        self.assertEqual("+555555555555", db.current_user.get_phone())
        self.assertEqual("user@gmail.com", db.current_user.get_email())
        # check user in db.save()
        self.assertEqual("user", db.users[1].get_name())
        self.assertEqual("+555555555555", db.users[1].get_phone())
        self.assertEqual("user@gmail.com", db.users[1].get_email())
        self.assertEqual("user", mail_service.users[0].get_name())

    def test_registration_if_user_exists(self):
        db = Database()
        bank_service = BankService()
        mail_service = MailService()

        registration = RegistrationService(db, bank_service, mail_service)
        with self.assertRaises(ValueError) as cm:
            registration.registration("user1", "+000000000000", "user1@gmail.com")
        self.assertEqual(
            'Данный пользователь уже зарегестрирован в системе',
            str(cm.exception)
        )
        # check if correct user is used in function db.is_new()
        self.assertEqual("user1", db.current_user.get_name())
        self.assertEqual("+000000000000", db.current_user.get_phone())
        self.assertEqual("user1@gmail.com", db.current_user.get_email())

    def test_mail_confirmation_if_user_not_found(self):
        db = Database()
        bank_service = BankService()
        mail_service = MailService()
        registration = RegistrationService(db, bank_service, mail_service)
        with self.assertRaises(ValueError) as cm:
            registration.confirm_mail("user0@gmail.com", "user0")
        self.assertEqual(
            'Пользователь не существует',
            str(cm.exception)
        )
        # check if correct email is used in function db.get_user_by_email(email)
        self.assertEqual("user0@gmail.com", db.current_str)

    def test_mail_confirmation(self):
        db = Database()
        bank_service = BankService()
        mail_service = MailService()
        registration = RegistrationService(db, bank_service, mail_service)

        self.assertTrue(registration.confirm_mail("user1@gmail.com", "user1"))

        # check user in db.get_user_by_email(user)
        self.assertEqual("user1@gmail.com", db.current_str)
        # check user in mail_service.get_key(user)
        self.assertTrue("user1@gmail.com", mail_service.current_user.get_email())
        self.assertTrue("user1", mail_service.current_user.get_name())
        # check user in db.save_mail_confirmation(user)
        self.assertTrue("user1@gmail.com", db.current_user.get_email())
        self.assertTrue("user1", db.current_user.get_name())

    def test_mail_confirmation_wrong_key(self):
        db = Database()
        bank_service = BankService()
        mail_service = MailServiceDifferentKey()
        registration = RegistrationService(db, bank_service, mail_service)

        self.assertFalse(registration.confirm_mail("user1@gmail.com", "user1"))
        # check user in db.get_user_by_email(user)
        self.assertEqual("user1@gmail.com", db.current_str)
        # check user in mail_service.get_key(user)
        self.assertTrue("user1@gmail.com", mail_service.current_user.get_email())
        self.assertTrue("user1", mail_service.current_user.get_name())


    def test_bank_card_confirmation_if_user_not_found(self):
        db = Database()
        bank_service = BankService()
        mail_service = MailService()

        registration = RegistrationService(db, bank_service, mail_service)
        # diff tests for cases
        with self.assertRaises(ValueError) as cm:
            registration.confirm_bank_card(5, "555555555555555", "555", date.fromisocalendar(2022, 1, 1))
        self.assertEqual(
            'Пользователь не существует',
            str(cm.exception)
        )
        # check if correct id is used in function db.get_user_by_id(user_id)
        self.assertEqual(5, db.current_int)

    def test_bank_card_confirmation(self):
        db = Database()
        bank_service = BankService()
        mail_service = MailService()

        registration = RegistrationService(db, bank_service, mail_service)
        self.assertTrue(registration.confirm_bank_card(0, "555555555555555", "555", date.fromisocalendar(2022, 1, 1)))
        # check if correct user_id is used in function db.get_user_by_id(user_id)
        self.assertEqual(0, db.current_int)
        # check if correct user is used in function db.save_user_card(user)
        self.assertEqual("user1", db.current_user.get_name())
        self.assertEqual("user1@gmail.com", db.current_user.get_email())
        self.assertEqual(0, db.current_user.get_user_id())
        # check if correct card is used in function bank_service.pay(card, 1)
        self.assertEqual(0, bank_service.current_card.id)
        self.assertEqual("555555555555555", bank_service.current_card.number)
        self.assertEqual("555", bank_service.current_card.three_num)
        # check if correct card is used in function bank_service.pay_back(card, 1)
        self.assertEqual(0, bank_service.current_back_card.id)
        self.assertEqual("555555555555555", bank_service.current_back_card.number)
        self.assertEqual("555", bank_service.current_back_card.three_num)

        self.assertEqual(bank_service.current_amount, bank_service.current_back_amount)
