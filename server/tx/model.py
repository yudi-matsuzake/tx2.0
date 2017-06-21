import tx.db as db
import sqlalchemy.orm
import sqlalchemy as sql

import threading

class Client(db.base):
    __tablename__ = 'clients'

    cpf  = sql.Column(sql.String, primary_key=True)
    name = sql.Column(sql.String)

    accounts = sql.orm.relationship('Account', back_populates='client')

    def __json__(self):
        accounts = []
        for a in self.accounts:
            accounts.append(a.__json__())

        return {
            'type': self.__tablename__,
            'cpf' : self.cpf,
            'name': self.name,
            'accounts' : accounts
        }

class Account(db.base):
    __tablename__ = 'accounts'

    id          = sql.Column(sql.Integer, primary_key=True)
    client_cpf  = sql.Column(sql.String, sql.ForeignKey('clients.cpf'))

    balance     = sql.Column(sql.Float)
    saving      = sql.Column(sql.Float)

    client  = sql.orm.relationship('Client', back_populates='accounts')

    @sql.orm.reconstructor
    def create_lock(self):
        self.lock = threading.Lock()

    def __json__(self):
        return {
            'type'      : self.__tablename__,
            'id'        : self.id,
            'client_cpf' : self.client_cpf,
            'balance'   : self.balance,
            'saving'    : self.saving
        }
