from dialogs import *
from Tkinter import *

class ConnectDlg(MyDialog):
    
    def apply(self):
        hostname = self.hstNameInp.get()
        dbName = self.dbNameInp.get()
        userName = self.usrNameInp.get()
        passwd = self.psswdInp.get()
        
        self.result = hostname,dbName,userName,passwd
        
    def body(self,master):        
        self.hstNameLbl = Label(master,text="Hostname:")
        self.hstNameLbl.grid(row=0,column=0,sticky=N+S+E+W)
        self.hstNameInp = Entry(master)
        self.hstNameInp.insert(0,"localhost")
        self.hstNameInp.grid(row=0,column=1,sticky=N+S+E+W)
        
        self.dbNameLbl = Label(master,text="Database:")
        self.dbNameLbl.grid(row=1,column=0,sticky=N+S+E+W)       
        self.dbNameInp = Entry(master)
        self.dbNameInp.insert(0,"mothrecs")
        self.dbNameInp.grid(row=1,column=1,sticky=N+S+E+W)
        
        self.usrNameLbl = Label(master,text="User Name:")
        self.usrNameLbl.grid(row=2,column=0,sticky=N+S+E+W)
        self.usrNameInp = Entry(master)
        self.usrNameInp.insert(0,"martin")
        self.usrNameInp.grid(row=2,column=1,sticky=N+S+E+W)
        
        self.psswdLbl = Label(master,text="Password:")
        self.psswdLbl.grid(row=3,column=0,sticky=N+S+E+W)
        self.psswdInp = Entry(master,show="*")
        self.psswdInp.grid(row=3,column=1,sticky=N+S+E+W) 
        
        return self.psswdInp#initial focus