#!/usr/bin/env python      
import Tkinter as tk   
import dialogs as d 
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
        self.menuBar = tk.Menu(self.parent)
        self.parent.config(menu=self.menuBar) 
        
        self.fileMenu = tk.Menu(self.menuBar)
        self.fileMenu.add_command(label="Connect...", command=self.onConnectCmd)
        self.fileMenu.add_command(label="Quit", command=self.onExit)
        
        self.addRecMenu = tk.Menu(self.menuBar)
        self.addRecMenu.add_command(label = "Add record event...")
        self.addRecMenu.add_command(label = "Add record data...")
        self.addRecMenu.add_command(label = "Add taxon data...")
        
        self.queryMenu = tk.Menu(self.menuBar)
        self.queryMenu.add_command(label="Run a query...")
                
        self.menuBar.add_cascade(label="File", menu=self.fileMenu)                
        self.menuBar.add_cascade(label="Add records", menu=self.addRecMenu, state=tk.DISABLED)
        self.menuBar.add_cascade(label="Query", menu=self.queryMenu, state=tk.DISABLED)
                
        
    def onConnectCmd(self):
        dlg = d.ConnectDlg(self)
        params = dlg.result
        #print params
        
        #see e.g. http://www.mysqltutorial.org/python-mysql/
        try:
            self.cnx = mysql.connector.connect(user=params[2],password=params[3],
                              host=params[0],
                              database=params[1])
            self.connected = True
            #activate add and query records - indexing start at 1 not 0!
            self.menuBar.entryconfig(2, state=tk.NORMAL)
            self.menuBar.entryconfig(3, state=tk.NORMAL)
            
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


        
        
     


#app = Application()                       
#app.master.title('Sample application')    
#app.mainloop() 

root = tk.Tk()
app = Application(root)    
root.mainloop()                   