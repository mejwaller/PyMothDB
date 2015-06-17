import mysql.connector  
from mysql.connector import Error

class dbController:
            
    #def connect(self,user,password,host,database):
    def connect(self,params):        
        self.cnx = mysql.connector.connect(user=params[2],password=params[3],host=params[0],database=params[1])
        
    def connected(self):
        return self.cnx.is_connected()        
                
    def runQuery(self,query):
        self.lastQuery = query        
        curA = self.cnx.cursor()       
        curA.execute(self.lastQuery)        
        self.lastResult = curA.fetchall()
        print self.lastResult
        curA.close()

    
    def close(self):
        self.cnx.close
    