import logging
import mysql.connector

log = logging.getLogger(__name__)

class DB:
    def __init__(self, props):
        try:

            self.serverHandler = mysql.connector.connect(host=props.get("database").get("url"),
                                                         database=props.get("database").get("name"),
                                                         user=props.get("database").get("userName"),
                                                         password=props.get("database").get("password"),
                                                         autocommit=True,
                                                         auth_plugin='mysql_native_password'
                                                         )

            self.cursor = self.serverHandler.cursor()
            self.cursor.execute('SET NAMES utf8;')
            self.cursor.execute('SET CHARACTER SET utf8;')
            self.cursor.execute('SET character_set_connection=utf8;')

        except:
            log.critical("__init__")

    def executeQuery(self, query):
        self.cursor.execute(query)
        if query.split()[0].lower() == "select":
            return self.cursor.fetchall()

    def closeConnection(self):
        self.serverHandler.close()
        self.cursor.close()