## @package this is the control module of tx.
 # this module will operate with the tx data, inserting, deleting,
 # listing the objects in the database

import tx.db
import tx.model
import threading
import sqlalchemy.sql.functions as sqlfunc

session = tx.db.newsession()

transaction_lock = threading.Lock()

class ControlError(BaseException):
    def __init__(self, msg, code):
        self.msg = msg
        self.code = code

## get a account with the id `id`
 # @param id the number of the account
 #
 # @return the model.Account with the id == `id` in case
 #         of the account exists, None otherwise
def get_account(id):

    account = session.query(tx.model.Account)\
               .filter(tx.model.Account.id == id)\
               .one_or_none()

    return account

## get the total amount
def total_amount():
    (balance,) = session \
                    .query(sqlfunc.sum(tx.model.Account.balance)
                    .label('balance_amount')).one_or_none()

    (saving,) = session \
                    .query(sqlfunc.sum(tx.model.Account.saving)
                    .label('saving_amount')).one_or_none()

    if balance == None: balance = 0.0
    if saving == None: saving = 0.0

    return balance + saving

## get client with cpf `cpf`
def get_client(cpf):
    client = session.query(tx.model.Client)\
              .filter(tx.model.Client.cpf == cpf)\
              .one_or_none()
    return client

def get_clients():
    return session.query(tx.model.Client).all()

def add_client(client):
    session.add(client)
    session.commit()

def add_account(account):
    session.add(account)
    session.commit()

## Realize the withdraw of `value` in `account` using
 # the savings or the current account specified by `method`
 #
 # @param account the model.Account to realize the withdraw
 # @param value   the value of the withdraw
 # @param method  must be 'saving' or 'current'
def withdraw(account, value, method):
    if value <= 0:
        raise ControlError('The withdraw value cannot be 0 or less', 400)

    with account.lock:
        if method == 'current':
            if value > account.balance:
                raise ControlError(
                        'The account %d does not have the money to withdraw'
                        % account.id, 400)
            else:
                account.balance -= value
                session.commit()

        elif method == 'saving':
            if value > account.saving:
                raise ControlError(
                        'The account %d does not have the money to withdraw'
                        % account.id, 400)
            else:
                account.saving -= value
                session.commit()

        else:
            raise ControlError(
                    'The withdraw method must be saving or current', 400)


## Realize the withdraw of `value` in `account` using
 # the savings or the current account specified by `method`
 #
 # @param account the model.Account to realize the withdraw
 # @param value   the value of the withdraw
 # @param method  must be 'saving' or 'current'
def deposit(account, value, method):
    if value <= 0:
        raise ControlError('The deposit value cannot be 0 or less', 400)

    with account.lock:
        if method == 'current':
            account.balance += value
            session.commit()

        elif method == 'saving':
            account.saving += value
            session.commit()

        else:
            raise ControlError(
                    'The deposit method must be saving or current', 400)


## Realize a transaction from `sender` to `receiver` of value `value`
 #
# def transaction(sender, receiver, sender_method, receiver_method, value):
#     if value <= 0:
#         raise ControlError('The transaction value cannot be 0 or less', 400)

#     if( (sender_method != 'saving' and
#         sender_method != 'current') or
#         (receiver_method != 'saving' and
#         receiver_method != 'current')):
#         raise ControlError(
#                 'The transaction method must be saving or current', 400)

#     if receiver_method == sender_method and sender == receiver:
#         raise ControlError(
#                 'The sender and the receiver of a transaction '
#                 'with the same type (%s) '
#                 'must be different!' % receiver_method, 400)

#     if sender_method == 'current':
#         sender_method = 'balance'
#     if receiver_method == 'current':
#         receiver_method = 'balance'

#     # concurrency directives
#     # global lock
#     with transaction_lock:

#         # object locks
#         sender.lock.acquire()
#         receiver.lock.acquire()

#     sender_amount = getattr(sender, sender_method)

#     if sender_amount < value:
#         raise ControlError(
#                 'The account %d does not have the money to transact'
#                 % sender.id, 400)

#     setattr(sender, sender_method, sender_amount - value)
#     setattr(receiver, receiver_method,
#             getattr(receiver, receiver_method) + value)

#     session.commit()

#     sender.lock.release()
#     receiver.lock.release()

