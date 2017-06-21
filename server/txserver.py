import flask
import tx.db
import tx.model
import tx.control

import sys

import json

tx.db.base.metadata.create_all(tx.db.engine)
app = flask.Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return flask.make_response(
            flask.jsonify(
                {
                    'type' : 'error',
                    'msg': 'Not found'
                }), 404)

@app.errorhandler(400)
def not_found(error):
    return flask.make_response(
            flask.jsonify(
                {
                    'type' : 'error',
                    'msg': 'Bad request'
                }), 400)

def txjson(obj):
    if isinstance(obj, list):
        j = []
        for i in obj:
            j.append(i.__json__())

        return j
    else:
        return obj.__json__()

def txerror(msg, code = 404):
    json_response = flask.jsonify(
            {
                'type' : 'error',
                'msg'  : msg
            })

    return flask.make_response(json_response, code)

## get the account with number `account_number`
@app.route('/accounts/<int:account_number>', methods=['GET'])
def accounts(account_number):

    account = tx.control.get_account(account_number)

    if account == None:
        return txerror('Cannot found account with number %d' % account_number)

    return flask.jsonify(txjson(account))

## get the sum of the current accounts
@app.route('/total_amount', methods=['GET'])
def total_amount():

    amount = tx.control.total_amount()

    return flask.jsonify({ 'total_amount' : amount })


@app.route('/clients/<string:cpf>', methods=['GET'])
def clients(cpf):
    client = tx.control.get_client(cpf)

    if client == None:
        return txerror('Cannot found client with cpf %s' % cpf)

    return flask.jsonify(txjson(client))

@app.route('/withdraw', methods=['PUT'])
def withdraw():
    #print('data: ', str(flask.request.get_data(), errors='ignore'))
    withdraw_request = json.loads(flask.request.get_data().decode('utf-8'))

    if( not 'type' in withdraw_request or
        withdraw_request['type'] != 'withdraw' or
        not 'account_id' in withdraw_request or
        not 'value' in  withdraw_request or
        not 'withdraw_method' in withdraw_request):
        flask.abort(400)

    withdraw_method = withdraw_request['withdraw_method']
    withdraw_value  = withdraw_request['value']

    account = tx.control.get_account(withdraw_request['account_id'])

    if account == None:
        return txerror('Cannot found account with number %d' % withdraw_request['account_id'])

    try:
        tx.control.withdraw(account, withdraw_value, withdraw_method)
        return flask.make_response(flask.jsonify(
                { 'status' : 'Accepted' }), 202 )
    except tx.control.ControlError as error:
        return txerror(error.msg, error.code)

@app.route('/deposit', methods=['PUT'])
def deposit():
    deposit_request = json.loads(flask.request.get_data())

    if( not 'type' in deposit_request or
        deposit_request['type'] != 'deposit' or
        not 'account_id' in deposit_request or
        not 'value' in deposit_request or
        not 'deposit_method' in deposit_request):
        flask.abort(400)

    deposit_value = deposit_request['value']
    deposit_method = deposit_request['deposit_method']

    account = tx.control.get_account(deposit_request['account_id'])

    if account == None:
        return txerror('Cannot found account with number %d'
                        % deposit_request['account_id'])

    try:
        tx.control.deposit(account, deposit_value, deposit_method)
        return flask.make_response(flask.jsonify(
                { 'status' : 'Accepted' }), 202 )
    except tx.control.ControlError as error:
        return txerror(error.msg, error.code)

port_to_bank = {
    8080 : 'Banco do Brasil',
    8081 : 'Banco do Brasil',
    8082 : 'Caixa Econômica Federal',
    8083 : 'Bradesco',
    8084 : 'Santander'
}

port_to_ip  = {
    8080 : 'localhost',
    8081 : 'localhost',
    8082 : 'localhost',
    8083 : 'localhost',
    8084 : 'localhost'
}

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('USAGE: %s <port>' % sys.argv[0])
        sys.exit(1)

    try:
        port = int(sys.argv[1])
        bank = port_to_bank[port]
        print(bank)
    except KeyError:
        print('ERROR: Please input a valid branch port')
        sys.exit(1)

    app.run(debug=True, threaded=True, port=port)
