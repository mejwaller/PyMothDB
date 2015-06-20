import mysql.connector  
from mysql.connector import Error

class dbController:
            
    #def connect(self,user,password,host,database):
    def connect(self,params):        
        self.cnx = mysql.connector.connect(user=params[2],password=params[3],host=params[0],database=params[1])
        
    def connected(self):
        return self.cnx.is_connected()
    
    def runInsert(self):  
        print "Running:" + self.lastCmd
        curA = self.cnx.cursor()
        curA.execute(self.lastCmd)
        self.cnx.commit()
        curA.close()
                
    def runQuery(self,query):
        self.lastCmd = query  
        print "Running:" + self.lastCmd
        curA = self.cnx.cursor()
        curA.execute(self.lastCmd)        
        self.lastResult = curA.fetchall()
        print str(self.lastResult)
        curA.close()      
        
      
    #note record_event is enforced unique on date,type and gridref (together)
    #so inserting a dupe should fail  
    def runAddRecEvent(self,stmt):
        #print stmt
        self.lastCmd = "INSERT INTO record_event(record_date,record_type,grid_ref,notes) \
VALUES('" + stmt[0] + "','" + stmt[1] + "','" + stmt[2] + "','" + stmt[3] + "');"
        #print self.lastInsert
        self.runInsert()
   
    def close(self):
        self.cnx.close
    