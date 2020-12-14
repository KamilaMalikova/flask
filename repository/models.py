import app

db = app.db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(12), unique=True, nullable=False)
    is_email_confirmed = db.Column(db.BOOLEAN, default=False)
    is_card_confirmed = db.Column(db.BOOLEAN, default=False)
    seller_deal = db.Column(db.Integer, nullable=False)
    buyer_deal = db.Column(db.Integer, nullable=False)
    card = db.relationship('Card', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.phone}')"


class Card(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    number = db.Column(db.String(12), nullable=False)
    three_num = db.Column(db.String(3), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"Card('{self.id}', '{self.number}', '{self.three_num}', '{self.due_date}')"


class Deal(db.Model):
    deal_id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, nullable=False)
    auction_id = db.Column(db.Integer, nullable=False)
    is_sent = db.Column(db.BOOLEAN, default=False)
    is_delivered = db.Column(db.BOOLEAN, default=False)
    seller_id = db.Column(db.Integer, nullable=False)
    buyer_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Deal('{self.deal_id}', '{self.lot_id}', '{self.auction_id}', '{self.is_sent}', '{self.is_delivered}', '{self.seller_id}', '{self.buyer_id}')"
