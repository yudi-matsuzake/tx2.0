import tx.db as db
import tx.control
import sqlalchemy.orm
import sqlalchemy.event
import sqlalchemy as sql
import random
import nomes

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

# populate
def random_cpf():
    cpf = str(random.randint(0, 999))
    cpf += '.' + str(random.randint(0, 999))
    cpf += '.' + str(random.randint(0, 999))
    cpf += '-' + str(random.randint(0, 99))
    return cpf

@sql.event.listens_for(Client.__table__, 'after_create')
def populate_client(*args, **kwargs):
    for i in range(random.randint(5, 10)):
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

