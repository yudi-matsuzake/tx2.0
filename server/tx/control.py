## @package this is the control module of tx.
 # this module will operate with the tx data, inserting, deleting,
 # listing the objects in the database

import tx.db
import tx.model
import threading
import sqlalchemy.sql.functions as sqlfunc
import http
import http.client
import json
import datetime
import socket

session = tx.db.newsession()
acid_session = tx.db.acid_newsession()

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

def get_transaction(id):
    transaction = acid_session\
            .query(tx.model.Transaction)\
            .filter(tx.model.Transaction.id == id)\
            .one_or_none()

    return transaction

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

def abort_transaction(id):
    t = get_transaction(id)
    t.status = 'aborted'
    acid_session.commit()

## first phase of the participant
def participant_first_phase(transaction):
    receiver = get_account(transaction.receiver_id)

    if receiver == None:
        raise ControlError(
                'There is no account with id %d' % transaction.receiver_id, 400)

    receiver.lock.acquire()

    print('value: ', transaction.value)
    # add the transaction
    t = tx.model.Transaction(
            sender_id = transaction.sender_id,
            receiver_id = transaction.receiver_id,
            cordinator_tx = transaction.cordinator_tx,
            sender_branch = transaction.sender_branch,
            receiver_branch = transaction.receiver_branch,
            sender_method = transaction.sender_method,
            receiver_method = transaction.receiver_method,
            value = transaction.value,
            timestamp = transaction.timestamp,
            status = 'provisory')

    acid_session.add(t)
    acid_session.commit()

    t.participant_tx = t.id
    acid_session.commit()

    return t

## second phase from the participant perspective
def participant_second_phase(id):
    transaction = tx.control.get_transaction(id)

    if transaction == None:
        raise ControlError(
                'There is no transaction with id %d' % id, 400)

    receiver = get_account(transaction.receiver_id)
    currvalue = getattr(receiver, transaction.receiver_method)
    setattr(receiver, transaction.receiver_method, currvalue + transaction.value)
    session.commit()

    transaction.status = 'committed'
    acid_session.commit()

    if not receiver.lock.acquire(blocking=False):
        receiver.lock.release()

## two phase transaction
def coordinate_twophase_transaction(transaction, sender):

    with sender.lock:

        # verify if the sender was the amount
        sender_amount = getattr(sender, transaction.sender_method)

        if sender_amount < transaction.value:
            raise ControlError(
                    'The account %d does not have the money to transact'
                    % sender.id, 400)

        try:

            branch_port = 8080 + transaction.receiver_branch

            # FIRST PHASE
            # send the message to the another branch
            connection = http.client.HTTPConnection(
                    tx.db.port_to_ip[branch_port],
                    branch_port,
                    timeout=10)

            try:
                connection.request('POST', '/twophase', json.dumps(transaction.__json__()))
                response = connection.getresponse()
                status = response.status
                data = response.read()

            except:
                raise ControlError(
                        'Error on connecting the server of branch %d'
                        % transaction.receiver_branch, 500)

            # checking the response
            if status < 200 or status >= 300:
                transaction.status = 'aborted'
                if ( 'type' in jerror and
                        jerror['type'] == 'error' and
                        'msg' in jerror ):
                    raise ControlError(jerror['msg'], status)
                else:
                    raise ControlError(
                            'Error with the branch %d system' % branchid,
                            status)

            try:
                transaction_response = tx.model.Transaction()
                if not transaction_response.__from_json__(data):
                    raise ControlError(
                            'Bad json from branch response from branch id %d'
                            % branchid, 500)

                # change status
                transaction.participant_tx = transaction_response.participant_tx
                transaction.status = 'provisory'
                acid_session.commit()

                setattr(sender,
                        transaction.sender_method,
                        sender_amount - transaction.value)
                session.commit()

                # set phase
                transaction.status = 'committed'
                acid_session.commit()
            except:
                connection.request('DELETE', '/twophase/%d' % transaction_response.participant_tx)
                raise

            connection.request('PUT', '/twophase/%d' % transaction.participant_tx)

        except socket.timeout:
            transaction.status = 'aborted'
            acid_session.commit()
            raise ControlError(
                    'The branch %d system is unresponsive' % branchid, 500)
        except:
            transaction.status = 'aborted'
            acid_session.commit()
            raise

## Transaction to the same branch
 #
def same_branch_transaction(sender, receiver, sender_method, receiver_method, value):

    # concurrency directives
    # global lock
    with transaction_lock:
        # object locks
        sender.lock.acquire()
        receiver.lock.acquire()

    sender_amount = getattr(sender, sender_method)

    if sender_amount < value:
        raise ControlError(
                'The account %d does not have the money to transact'
                % sender.id, 400)

    setattr(sender, sender_method, sender_amount - value)
    setattr(receiver, receiver_method,
            getattr(receiver, receiver_method) + value)

    session.commit()

    sender.lock.release()
    receiver.lock.release()

## Realize a transaction from `sender` to `receiver` of value `value`
 # from the coordinator perspective
 #
def transaction(
        sender,
        receiver_id,
        sender_method,
        receiver_method,
        receiver_branch,
        value):

    if value <= 0:
        raise ControlError('The transaction value cannot be 0 or less', 400)

    if( (sender_method != 'saving' and
        sender_method != 'current') or
        (receiver_method != 'saving' and
        receiver_method != 'current')):
        raise ControlError(
                'The transaction method must be saving or current', 400)

    if receiver_method == sender_method and sender.id == receiver_id:
        raise ControlError(
                'The sender and the receiver of a transaction '
                'with the same type (%s) '
                'must be different!' % receiver_method, 400)

    if sender_method == 'current':
        sender_method = 'balance'
    if receiver_method == 'current':
        receiver_method = 'balance'

    # verify if is to another branch
    if receiver_branch == tx.db.get_branch_id():
        # get receiver model from the local database
        receiver = get_account(receiver_id)
        if receiver == None:
            raise ControlError(
                    'There is no account with id %d' % receiver_id, 400)

        same_branch_transaction(
                sender,
                receiver,
                sender_method,
                receiver_method,
                value)

    else:
        # populate transaction model
        transaction = tx.model.Transaction(
                sender_id = sender.id,
                receiver_id = receiver_id,
                sender_branch = tx.db.get_branch_id(),
                receiver_branch = receiver_branch,
                sender_method = sender_method,
                receiver_method = receiver_method,
                value = value,
                timestamp = datetime.datetime.now(),
                status = 'active')

        # add transaction into bd
        acid_session.add(transaction)
        acid_session.commit()

        # update the cordinator id
        transaction.cordinator_tx = transaction.id
        acid_session.commit()

        coordinate_twophase_transaction(transaction, sender)

## Restore the state of the transactions
def restore():

    acid_session = tx.db.acid_newsession()

    # restore the active transactions
    active_transactions = acid_session.query(tx.model.Transaction)\
        .filter(tx.model.Transaction.status == 'active')\
        .filter(tx.model.Transaction.sender_branch == tx.db.get_branch_id())\
        .all()

    for transaction in active_transactions:
        sender = get_account(transaction.sender_id)
        if sender != None:
            try:
                coordinate_twophase_transaction(transaction, sender)
            except:
                pass

    # restore provisory transactions who i coordinate
    provisory_transactions = acid_session.query(tx.model.Transaction)\
        .filter(tx.model.Transaction.status == 'provisory')\
        .filter(tx.model.Transaction.sender_branch == tx.db.get_branch_id())\
        .all()

    for transaction in provisory_transactions:
        sender = get_account(transaction.sender_id)
        if sender != None:
            try:
                setattr(sender,
                        transaction.sender_method,
                        sender_amount - transaction.value)
                session.commit()

                # set phase
                transaction.status = 'committed'
                acid_session.commit()

                branch_port = 8080 + transaction.receiver_branch
                connection = http.client.HTTPConnection(
                        tx.db.port_to_ip[branch_port],
                        branch_port,
                        timeout=10)
                connection.request('PUT', '/twophase/%d' % transaction.participant_tx)
            except:
                transaction.status = 'aborted'
                acid_session.commit()

    # restore provisory transactions who i participate
    provisory_transactions = acid_session.query(tx.model.Transaction)\
        .filter(tx.model.Transaction.status == 'provisory')\
        .filter(tx.model.Transaction.receiver_branch == tx.db.get_branch_id())\
        .all()

    for transaction in provisory_transactions:
        sender = get_account(transaction.sender_id)
        if sender != None:
            branch_port = 8080 + transaction.sender_branch
            connection = http.client.HTTPConnection(
                    tx.db.port_to_ip[branch_port],
                    branch_port,
                    timeout=10)
            connection.request('GET', '/twophase/%d' % transaction.cordinator_tx)
            response = connection.getresponse()
            data = response.read()

            cordinator_trasaction = tx.model.Transaction()
            if cordinator_trasaction.__from_json__(data):
                print(cordinator_trasaction.status)
                if cordinator_trasaction.status == 'committed':
                    participant_second_phase(transaction.id)
                elif cordinator_trasaction.status == 'aborted':
                    transaction.status = 'aborted'
                    acid_session.commit()

    acid_session.close()
