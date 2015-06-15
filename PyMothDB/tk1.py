#!/usr/bin/env python      
import Tkinter as tk   
import MyDialog as d 
import mysql.connector  
from mysql.connector import Error
import tkMessageBox

class Application(tk.Frame):              
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.parent = master
        self.connected = False
        self.constructUI()
        
    def constructUI(self):
        self.parent.title("Moth records database")  
        menuBar = tk.Menu(self.parent)
        self.parent.config(menu=menuBar) 
        
        fileMenu = tk.Menu(menuBar)
        fileMenu.add_command(label="Connect...", command=self.onConnectCmd)
        fileMenu.add_command(label="Quit", command=self.onExit)
        
        menuBar.add_cascade(label="File", menu=fileMenu)
                
        
    def onConnectCmd(self):
        dlg = ConnectDlg(self)
        params = dlg.result
        #print params
        
        #see e.g. http://www.mysqltutorial.org/python-mysql/
        try:
            self.cnx = mysql.connector.connect(user=params[2],password=params[3],
                              host=params[0],
                              database=params[1])
            self.connected = True
            
            #curA = self.cnx.cursor()

            #showtables = ("SHOW TABLES")

            #curA.execute(showtables)

            #print curA.fetchall()

            #curA.close()
            
            #self.cnx.close
        
        except Error as e: 
                tkMessageBox.showerror(
                "Database connect",
                "Cannot connect to database %s - error: %s" % (params[1], e))
                             
           
    def onExit(self):
        self.quit()                

class ConnectDlg(d.MyDialog):
    
    def apply(self):
        hostname = self.hstNameInp.get()
        dbName = self.dbNameInp.get()
        userName = self.usrNameInp.get()
        passwd = self.psswdInp.get()
        
        self.result = hostname,dbName,userName,passwd
        
    def body(self,master):        
        self.hstNameLbl = tk.Label(master,text="Hostname:")
        self.hstNameLbl.grid(row=0,column=0,sticky=tk.N+tk.S+tk.E+tk.W)
        self.hstNameInp = tk.Entry(master)
        self.hstNameInp.insert(0,"localhost")
        self.hstNameInp.grid(row=0,column=1,sticky=tk.N+tk.S+tk.E+tk.W)
        
        self.dbNameLbl = tk.Label(master,text="Database:")
        self.dbNameLbl.grid(row=1,column=0,sticky=tk.N+tk.S+tk.E+tk.W)       
        self.dbNameInp = tk.Entry(master)
        self.dbNameInp.insert(0,"mothrecs")
        self.dbNameInp.grid(row=1,column=1,sticky=tk.N+tk.S+tk.E+tk.W)
        
        self.usrNameLbl = tk.Label(master,text="User Name:")
        self.usrNameLbl.grid(row=2,column=0,sticky=tk.N+tk.S+tk.E+tk.W)
        self.usrNameInp = tk.Entry(master)
        self.usrNameInp.insert(0,"martin")
        self.usrNameInp.grid(row=2,column=1,sticky=tk.N+tk.S+tk.E+tk.W)
        
        self.psswdLbl = tk.Label(master,text="Password:")
        self.psswdLbl.grid(row=3,column=0,sticky=tk.N+tk.S+tk.E+tk.W)
        self.psswdInp = tk.Entry(master,show="*")
        self.psswdInp.grid(row=3,column=1,sticky=tk.N+tk.S+tk.E+tk.W) 
        
        return self.psswdInp#initial focus
        
        
     


#app = Application()                       
#app.master.title('Sample application')    
#app.mainloop() 

root = tk.Tk()
app = Application(root)    
root.mainloop()                   