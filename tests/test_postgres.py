import pytest
import psycopg2
from psycopg2 import sql

from src.postgres import postgresWrapper

class postgresTest(postgresWrapper):
    def executeSQL(self, sqlQuery):
        self.cursor.execute(sqlQuery)

    def getAllResults(self):
        return self.cursor.fetchall()

    #def rollbackAllCommits(self):

@pytest.fixture
def dbWrapper():
    dbObj = postgresTest("testdb")
    
    dbObj.loadConfig("../database.ini")
    dbObj.connectToDatabase()

    return dbObj
    # dbObj.closeConnection
    # dbObj.ROLLBACK

def testAppendValues(dbWrapper):
    db = dbWrapper

    # append *bufferLen* amount of string vector pairs, then assert that they were correctly added
    sampleEmbeddings = [1, 2, 3, 4, 5, 6]
    
    for i in range(0, len(sampleEmbeddings)):
        db.bufferedAppend("TEST ADDRESS", [sampleEmbeddings[i]]*755)
        
        query = sql.SQL(
            "SELECT embedding FROM testdb;"
        )

        db.executeSQL(query)
        results = db.getAllResults() 

        # compare results appended to the sampleEmbeddings
        for i in range(0, len(results)):
            print(results)
            assert  == sampleEmbeddings[i]


def testBuffer(dbWrapper):
    # append one address, wont append too database instead will be stored in bufferLen
    # then clear buffer, test will pass if value is stored in database
# Can time:w inserting 5 items through flusghing buffer vs calling excecute many



