import psycopg2
from psycopg2.extras import execute_values
from psycopg2 import sql

import logging
from configparser import ConfigParser

class postgresWrapper:
    def __init__(self, tableName):
        self.tableName = tableName
        self.config = None
        self.connection = None

        self.buffer = ()
        self.bufferLimit = 5

    def closeConnection(self):
        if self.connection: # making sure the objects exist before we deconstruct them
            self.connection.close()
        
        if self.cursor:
            self.cursor.close()
        # empty buffer
        self.flushBuffer()



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
    

    #check buffer to see if its too large
    #if small enough insert (address, imageVec) tuple to buffer
    #if too large then call _appendBuffer which will clear buffer and excecutemany
    def bufferedAppend(self, address, imageVec):        
        self.buffer = self.buffer + ((address, imageVec),)

        if len(self.buffer) >= self.bufferLimit: # if buffer size is over limit then flush it
            self.flushBuffer()

    def commitTransaction(self):
        self.connection.commit()
    
    def rollbackTransaction(self):
        self.connection.rollback()
    
    #https://dev.mysql.com/doc/refman/8.0/en/insert-optimization.html
    def _appendBuffer(self):
        query = sql.SQL(
            "INSERT INTO {} (address, embedding) VALUES (%s, %s);" # wrap try except warnmiong tho 
        ).format(sql.Identifier(self.tableName))

        self.cursor.executemany(query, self.buffer) # use execute_values instead
    
    def getClosestVec(self, imageVec):
        results = None

        query = sql.SQL(
            "SELECT * FROM {} ORDER BY embedding <-> %s LIMIT 5;"
        ).format(sql.Identifier(self.tableName))

        try:
            self.cursor.execute(query, imageVec)
            results = self.cursor.fetchall()

        except ProgrammingError:
            logging.info(
                "Not able to retrieve closest vector, no address matches image"
            )
            
        return results

    def flushBuffer(self):
        if not self.buffer:
            return None
        
        self._appendBuffer()
        self.buffer = ()
