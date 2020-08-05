import sqlalchemy as db
from settings import *


class Database:
    def __init__(self):
        props = getProps("database")
        self.engine = db.create_engine("mysql+pymysql://%s:%s@%s:%s/%s"
                                       % (props["userName"], props["password"],
                                          props["url"], props["port"], props["name"]))

        self.connection = self.engine.connect()
        self.metadata = db.MetaData()

    def getDB(self):
        return db

    def getEngine(self):
        return self.engine

    def getTable(self):
        return db.Table

    def getConnection(self):
        return self.connection

    def getMeta(self, tableName):
        return db.Table(tableName, self.metadata, autoload=True, autoload_with=self.engine)

    def closeDB(self):
        self.connection.invalidate()
        self.engine.dispose()
