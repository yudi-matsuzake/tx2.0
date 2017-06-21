import sqlalchemy.ext
import sqlalchemy.ext.declarative
import sqlalchemy.orm
import sqlalchemy as sql

base = sql.ext.declarative.declarative_base()
engine = sql.create_engine('sqlite:///tx.db', echo=True)
newsession = sql.orm.sessionmaker(bind = engine)
