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
    def runAddRecEvent(self,data):
        #print stmt
        self.lastCmd = "INSERT INTO record_event(record_date,record_type,grid_ref,notes) \
VALUES('" + data[0] + "','" + data[1] + "','" + data[2] + "','" + data[3] + "');"
        #print self.lastInsert
        self.runInsert()
   
    def close(self):
        self.cnx.close
        
    def runAddRecData(self,data):
        print "Adding record data..."
        self.lastCmd = "INSERT INTO record_data(recevent_id,taxon_id,count,notes) \
VALUES('" + data[0] + "','" + data[1] + "','" + data[2] + "','" + data[3] + "');"
        self.runInsert()
        
    def runAddTaxon(self,data):
        print "Adding taxon.."
        self.lastCmd = "INSERT INTO taxon_data(order_name,family_name,subfamily_name,genus_name,\
species_name,subspecies_name,aberration_name,form_name,vernacular_name,taxon_key) \
VALUES('" + data[0] + "','" + data[1] + "','" + data[2] + "','" + data[3] + "','" + data[4]\
 + "','" + data[5] + "','" + data[6] + "','" + data[7] + "','" + data[8] + "','" + data[9] + "');" 
        self.runInsert()
    