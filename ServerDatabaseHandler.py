#!/usr/bin/python
# -*- coding: utf-8 -*-

from LogHandler import LogHandler
import MySQLdb

class ServerDatabaseHandler:
    def __init__(self):
        try:
            self.logHandler = LogHandler("ServerDatabaseHandle")
			
            self.serverHandler = MySQLdb.connect('127.0.0.1', 'root', 'yourdbpassowrd', 'haberbus');
            self.serverHandler.set_character_set('utf8')
            self.serverHandler.autocommit(True)
			
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
