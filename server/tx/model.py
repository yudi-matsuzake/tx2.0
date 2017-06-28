import tx.db as db
import tx.control
import sqlalchemy.orm
import sqlalchemy.event
import sqlalchemy as sql
import random
import nomes
import json
import datetime

import time

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

    lock = threading.Lock()

    # @sql.orm.reconstructor
    # def create_lock(self):
    #     self.lock = threading.Lock()

    def __json__(self):
        return {
            'type'      : self.__tablename__,
            'id'        : self.id,
            'client_cpf' : self.client_cpf,
            'balance'   : self.balance,
            'saving'    : self.saving
        }

class Transaction(db.acid):
    __tablename__ = 'transactions'

    id                 = sql.Column(sql.Integer, primary_key=True)
    cordinator_tx      = sql.Column(sql.Integer)
    participant_tx     = sql.Column(sql.Integer)
    sender_id          = sql.Column(sql.Integer, nullable=False)
    receiver_id        = sql.Column(sql.Integer, nullable=False)
    sender_branch      = sql.Column(sql.Integer, nullable=False)
    receiver_branch    = sql.Column(sql.Integer, nullable=False)
    sender_method      = sql.Column(sql.String, nullable=False)
    receiver_method    = sql.Column(sql.String, nullable=False)
    value              = sql.Column(sql.Float, nullable=False)
    timestamp          = sql.Column(sql.DateTime)
    status             = sql.Column(sql.String)

    def __json__(self):
        return {
            'type'            : self.__tablename__,
            'id'              : self.id,
            'sender_id'       : self.sender_id,
            'receiver_id'     : self.receiver_id,
            'sender_branch'   : self.sender_branch,
            'sender_method'   : self.sender_method,
            'receiver_branch' : self.receiver_branch,
            'receiver_method' : self.receiver_method,
            'timestamp'       : time.mktime(self.timestamp.timetuple()),
            'value'           : self.value
        }

    def __from_json__(self, data):
        print('type: ', type(data))
        j = json.loads(data)

        keys = [ 'type',
                 'id',
                 'sender_id',
                 'receiver_id',
                 'sender_branch',
                 'sender_method',
                 'receiver_branch',
                 'receiver_method',
                 'timestamp',
                 'value']

        for k in keys:
            if k not in j:
                return False

        # remove timestamp
        keys.remove('timestamp')

        for k in keys:
            setattr(self, k, j[k])

        setattr(
            self,
            'timestamp',
            datetime.datetime.fromtimestamp(1498615201.0))

        return True

# populate
def random_cpf():
    cpf = str(random.randint(0, 999))
    cpf += '.' + str(random.randint(0, 999))
    cpf += '.' + str(random.randint(0, 999))
    cpf += '-' + str(random.randint(0, 99))
    return cpf

@sql.event.listens_for(Client.__table__, 'after_create')
def populate_client(*args, **kwargs):
    for i in range(random.randint(5, 15)):
        cpf  = random_cpf()
        name = nomes.nome_aleatorio()
        client = Client(cpf=cpf, name=name)
        tx.control.add_client(client)

@sql.event.listens_for(Account.__table__, 'after_create')
def populate_client(*args, **kwargs):
    for client in tx.control.get_clients():
        for i in range(random.randint(1, 3)):
            cpf = client.cpf
            balance = float(random.randint(0, 10000000.0))/100.0
            saving = float(random.randint(0, 100000000.0))/100.0
            account = Account(client_cpf=cpf, balance=balance, saving=saving)
            tx.control.add_account(account)

