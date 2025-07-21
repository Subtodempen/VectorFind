import pytest
import psycopg2
from psycopg2 import sql

import ast

from src.postgres import postgresWrapper

class postgresTest(postgresWrapper):
    def executeSQL(self, sqlQuery):
        self.cursor.execute(sqlQuery)

    def fetchAllResults(self):
        return self.cursor.fetchall()

    def getResults(self):
        self.executeSQL(sql.SQL(
            "SELECT * FROM {};"
        ).format(sql.Identifier(self.tableName)))

        results = self.fetchAllResults() 

        for i in range(0, len(results)):
            results[i] = list(results[i])
            results[i][1] = ast.literal_eval(results[i][1]) # fetch results returns a tuple of ill-formated tuples
        
        return results


@pytest.fixture
def dbWrapper():
    dbWrapper = postgresTest("testdb")
    
    dbWrapper.loadConfig("../database.ini")
    dbWrapper.connectToDatabase()

    yield dbWrapper
    
    dbWrapper.rollbackTransaction()
    dbWrapper.closeConnection() 

def testAppendValues(dbWrapper):
    # append *bufferLen* amount of string vector pairs, then assert that they were correctly added
    sampleEmbeddings = [1, 2, 39201, 4, 5]

    expectedResults = []
    actualResults = None
    
    for i in range(0, len(sampleEmbeddings)):
        address = "TEST ADDRESS"
        vector = [sampleEmbeddings[i]]*755

        dbWrapper.bufferedAppend(address, vector) # USAGE: append a vector to database 
        expectedResults.append([address, vector])

    actualResults = dbWrapper.getResults()

    assert actualResults == expectedResults
    dbWrapper.rollbackTransaction()
        
        
def testBuffer(dbWrapper):
    # append one address, wont append to database instead will be stored in bufferLen
    # then clear buffer, test will pass if value is stored in database
    # Can time inserting 5 items through flusghing buffer vs calling excecute many
    address = "TEST ADDRESS NOT REAL"
    vector = [1] * 755
    
    expectedResults = [[address, vector]]
    actualResults = None

    dbWrapper.bufferedAppend(address, vector) # USAGE: append a single vector without buffering
    dbWrapper.flushBuffer()
    
    actualResults = dbWrapper.getResults()

    assert actualResults == expectedResults
    dbWrapper.rollbackTransaction()
    



