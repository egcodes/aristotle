import logging
import mysql.connector


class DB:
    def __init__(self, props):
        self.log = logging.getLogger(__name__)

        try:

            self.serverHandler = mysql.connector.connect(host=props["url"],
                                                         database=props["name"],
                                                         user=props["userName"],
                                                         password=props["password"],
                                                         autocommit=True,
                                                         auth_plugin='mysql_native_password'
                                                         )

            self.cursor = self.serverHandler.cursor()
            self.cursor.execute('SET NAMES utf8;')
            self.cursor.execute('SET CHARACTER SET utf8;')
            self.cursor.execute('SET character_set_connection=utf8;')

        except:
            self.log.critical("__init__")

    def executeQuery(self, query):
        self.cursor.execute(query)
        if query.startswith("SELECT"):
            return self.cursor.fetchall()

    def closeConnection(self):
        self.serverHandler.close()
        self.cursor.close()