import psycopg2
from psycopg2.extras import execute_values
from psycopg2 import sql

import logging
from configparser import ConfigParser

class postgresWrapper:
    def __init__(self):
        self.tableName = "vecQuery"
        self.config = None
        self.connection = None

        self.buffer = []
        self.bufferLimit = 50


    def __del__(self):
        self.connection.close()
        self.cursor.close()

    def loadConfig(self, configFile = 'database.ini'):
        parser = ConfigParser()
        parser.read(configFile)

        databaseSection = "postgresql"
        self.config = {}

        if parser.has_section(databaseSection):
            params = parser.items(databaseSection)
        
            for param in params:
                self.config[param[0]] = param[1]
        
        else:
            logging.error(
                'Section {0} not found in the config file'.format(databaseSection)
            )
        
    
    def connectToDatabase(self):
        if self.config == None:
            logging.error(
                'Configuration not loaded can not connect'
            )
            
            return None

        self.connection = psycopg2.connect(**self.config)
        self.cursor = self.connection.cursor()

        #self.connection.autocommit = True

    def appendAdressAndVec(self, address, imageVec):
        #https://dev.mysql.com/doc/refman/8.0/en/insert-optimization.html
        #check buffer to see if its too large
        #if small enough insert (address, imageVec) tuple to buffer
        #if too large then clear buffer and excecutemany
        
        if len(self.buffer) < self.bufferLimit:
            self.buffer += (address, imageVec)

        else:
            query = sql.SQL("INSERT INTO {} VALUES (%s, %s)")
                .format(sql.Identifier(self.tableName))

            excecute_values(self.cursor, 
                            query, 
                            self.buffer)

            self.buffer = []
    
    def getClosestVec(self, imageVec):
