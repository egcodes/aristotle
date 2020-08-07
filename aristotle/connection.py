import sqlalchemy as db
from settings import *


class Database:
    __instance__ = None

    def __init__(self):
        if Database.__instance__ is None:
            Database.__instance__ = self
            dbProps = getProps("database")
            self.engine = db.create_engine("mysql+pymysql://%s:%s@%s:%s/%s"
                                           % (dbProps["userName"], dbProps["password"],
                                              dbProps["url"], dbProps["port"], dbProps["name"]))

            self.connection = self.engine.connect()
            self.metadata = db.MetaData()

    @staticmethod
    def get_instance():
        if not Database.__instance__:
            Database()
        return Database.__instance__

    def getDB(self):
        return db

    def getEngine(self):
        return self.engine

    def getTable(self):
        return db.Table

    def getConnection(self):
        return self.connection

    def getMeta(self):
        return self.metadata
        # return db.Table(tableName, self.metadata, autoload=True, autoload_with=self.engine)

    def closeDB(self):
        self.connection.invalidate()
        self.engine.dispose()
