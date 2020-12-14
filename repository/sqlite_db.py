from Users import User, Card
from repository.models import User as UserModel, Card as CardModel, Deal as DealModel

class SQliteRepository:
    def __init__(self, db):
        self.db = db
        pass

    def create_all(self):
        self.db.creat_all()

    def get_user_by_id(self, id) -> User:
        pass

    def is_new(self, new_user) -> bool:
        user = UserModel.query.filter_by(username=new_user.get_name(), email=new_user.get_email(), phone=new_user.get_phone())
        if user:
            return False
        else:
            return True

    def save(self, user) -> User:
        val = UserModel(username=user.get_name(), email=user.get_email(), phone=user.get_phone())
        self.db.session.add(val)
        self.db.session.commit()
        res = UserModel.query.filter_by(username=user.get_name())
        user = User(id=res.id, name=res.username, email=res.email, phone=res.phone)
        return user

    def save_mail_confirmation(self, user):
        pass

    def save_user_card(self, user):
        pass

    def get_user_by_email(self, email) -> User:
        pass

    def get_card(self, id) -> Card:
        pass

    def get_user_by_deal_id(self, deal_id) -> User:
        pass

    def get_seller_by_deal_lot(self, lot_id) -> User:
        pass

    def save_card(self, card):
        pass

    def save_deal(self, deal, user):
        pass

    @staticmethod
    def get_connection_path(db_path):
        return 'sqlite://{0}{1}'.format(db_path.get('host'), db_path.get('database'))
