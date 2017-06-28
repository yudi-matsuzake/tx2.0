import sqlalchemy.ext
import sqlalchemy.ext.declarative
import sqlalchemy.orm
import sqlalchemy as sql
import sys
import os

dbpath = 'db'

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

if len(sys.argv) != 2:
    print('USAGE: %s <port>' % sys.argv[0])
    sys.exit(1)
try:
    port = int(sys.argv[1])
    bank = port_to_bank[port]
    branchid = port - 8080

    print('port: ', port)

    if not os.path.isdir(dbpath):
        os.mkdir(dbpath)

    dbname  = '%s/%s' % (dbpath, str(branchid) +  ' - ' + bank + '.db')
    txdbname  = '%s/%s' % (dbpath, str(branchid) +  ' - ' + bank + '.txdb')
except KeyError:
    print('ERROR: Please input a valid branch port')
    sys.exit(1)
except os.error as e:
    print('Error creating db dir:', dbpath)
    print(e.strerror)
    exit(1)
    pass

acid = sql.ext.declarative.declarative_base()
acid_engine = sql.create_engine('sqlite:///%s' % txdbname, echo=True)
acid_newsession = sql.orm.sessionmaker(bind = acid_engine)

base = sql.ext.declarative.declarative_base()
engine = sql.create_engine('sqlite:///%s' % dbname, echo=True)
newsession = sql.orm.sessionmaker(bind = engine)

def get_ip():
    return port_to_ip[port]

def get_branch_id():
    return port - 8080
