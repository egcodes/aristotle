from sqlalchemy import *
from connection import Database
from datetime import datetime

db = Database().get_instance()
meta = db.getMeta()

present = datetime.now()
yearMonth = str(present.strftime('%Y%m'))

link_cache_table = Table(
    'link_cache', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('domain', String(50, collation='utf8_bin')),
    Column('link', String(500, collation='utf8_bin')),
)

link_table = Table(
    'links_%s' % yearMonth, meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('date', Date),
    Column('category', String(32)),
    Column('domain', String(255)),
    Column('link', String(500, collation='utf8_bin')),
    Column('title', String(500, collation='utf8_bin')),
    Column('description', String(1024, collation='utf8_bin')),
    Column('image', String(500, collation='utf8_bin')),
    Column('clicked', Integer, default=0),
    Column('timestamp', TIMESTAMP)
)
