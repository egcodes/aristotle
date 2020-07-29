#!/usr/bin/python
# -*- coding: utf-8 -*-

from LogHandler import LogHandler
import mysql.connector


class DbHandler:
    def __init__(self):
        try:
            self.logHandler = LogHandler("DbHandler")

            self.serverHandler = mysql.connector.connect(host='localhost',
                                                         database='haberbus',
                                                         user='root',
                                                         password='root',
                                                         autocommit=True,
                                                         auth_plugin='mysql_native_password'
                                                         )

            self.cursor = self.serverHandler.cursor()
            self.cursor.execute('SET NAMES utf8;')
            self.cursor.execute('SET CHARACTER SET utf8;')
            self.cursor.execute('SET character_set_connection=utf8;')

        except:
            self.logHandler.logger("__init__")

    def executeQuery(self, query):
        self.cursor.execute(query)
        if query.split()[0].lower() == "select":
            return self.cursor.fetchall()
        else:
            self.serverHandler.commit()

    def closeConnection(self):
        self.serverHandler.close()
        self.cursor.close()