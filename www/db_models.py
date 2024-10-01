from create_db import db
from sqlalchemy import BigInteger

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    tg_id = db.Column(db.BigInteger, unique=True, nullable=False)  
    invited_id = db.Column(db.BigInteger)
    lang = db.Column(db.String(5), default='en')

    balance = db.Column(db.BigInteger, default=0)
    last_tap_time = db.Column(db.Integer, default=0)

    town_name = db.Column(db.String(18))
    town_population = db.Column(db.Integer, default=0)
    town_balance = db.Column(db.Integer, default=0)
    town_rank = db.Column(db.Integer, default=1)
    town_residential_places = db.Column(db.Integer, default=0)
    town_entertainments = db.Column(db.Integer, default=0)
    town_medicine = db.Column(db.Integer, default=0)
    town_workplaces = db.Column(db.Integer, default=0)
    town_last_money_take_time = db.Column(db.Integer, default=0)
    town_balance_limit = db.Column(db.Integer, default=100000)

    def to_dict(self):
        return {
            'tg_id': self.tg_id,
            'balance': self.balance,
            'town_residential_places': self.town_residential_places,
        }

    referrals = db.relationship('Referals', backref='referrer', lazy=True, foreign_keys='Referals.referrer_tg_id')

class Referals(db.Model):
    __tablename__ = 'referals'
    id = db.Column(db.Integer, primary_key=True)
    referrer_tg_id = db.Column(db.BigInteger, db.ForeignKey('users.tg_id'), nullable=False)
    tg_id = db.Column(db.BigInteger)
    name = db.Column(db.String(128))
