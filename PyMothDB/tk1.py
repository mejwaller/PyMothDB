#!/usr/bin/env python      
import Tkinter as tk   
import dialogs as d 
import dbcontroller as db
from mysql.connector import Error
import tkMessageBox

class Application(tk.Frame):              
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.parent = master
        self.dbase = False
                
        self.constructUI()
        
    def constructUI(self):
        self.parent.title("Moth records database")  
        self.menuBar = tk.Menu(self.parent)
        self.parent.config(menu=self.menuBar) 
        
        self.fileMenu = tk.Menu(self.menuBar)
        self.fileMenu.add_command(label="Connect...", command=self.onConnectCmd)
        self.fileMenu.add_command(label="Quit", command=self.onExit)
        
        self.addRecMenu = tk.Menu(self.menuBar)
        self.addRecMenu.add_command(label = "Add record event...", command=self.onAddRecEvent)
        self.addRecMenu.add_command(label = "Add record data...", command=self.onAddRecData)
        self.addRecMenu.add_command(label = "Add taxon data...", command = self.onAddTaxonData)
        
        self.updateRecMenu = tk.Menu(self.menuBar);
        self.updateRecMenu.add_command(label = "Update record event...", command=self.onUpdateRecEvent)
        self.updateRecMenu.add_command(label = "Update record data...", command=self.onUpdateRecData)
        self.updateRecMenu.add_command(label = "Update taxon data...", command=self.onUpdateTaxonData)
        
        self.queryMenu = tk.Menu(self.menuBar)
        self.queryMenu.add_command(label="Run a query...",command=self.onAdHocQuery)
                
        self.menuBar.add_cascade(label="File", menu=self.fileMenu)                
        self.menuBar.add_cascade(label="Add records", menu=self.addRecMenu, state=tk.DISABLED)
        self.menuBar.add_cascade(label="Update Records", menu=self.updateRecMenu, state=tk.DISABLED)
        self.menuBar.add_cascade(label="Query", menu=self.queryMenu, state=tk.DISABLED)
                
        
    def onConnectCmd(self):
        dlg = d.ConnectDlg(self)
               
        if not dlg.cancelled:
            #see e.g. http://www.mysqltutorial.org/python-mysql/
            try:
                #db.dbController.connect(params[2],params[3],params[0],params[1])
                self.dbase = db.dbController()
                self.dbase.connect(dlg.result)
            
                if self.dbase.connected():  
                
                    #activate add, update and query records - indexing start at 1 not 0!
                    self.menuBar.entryconfig(2, state=tk.NORMAL) #add record
                    self.menuBar.entryconfig(3, state=tk.NORMAL) #update record
                    self.menuBar.entryconfig(4, state=tk.NORMAL) #query
                    
                    
                    #pre-populate taxondata and recevent data
                    getTaxa = "SELECT genus_name,species_name,vernacular_name,subspecies_name,\
aberration_name,form_name,id FROM taxon_data"
                    self.dbase.runQuery(getTaxa)
                    self.taxaRaw = self.dbase.lastResult
                    
                    getRecEvents="SELECT event_id,record_date,record_type,grid_ref FROM record_event"
                    self.dbase.runQuery(getRecEvents)
                    self.recEventsRaw = self.dbase.lastResult
            
            except Error as e: 
                tkMessageBox.showerror(
                    "Database connect",
                    "Cannot connect to database %s - error: %s" % (dlg .result[1], e))
                
    def onAdHocQuery(self):
        dlg = d.adHocQueryDlg(self)
            
        if not dlg.cancelled:
            try:
                self.dbase.runQuery(dlg.result)
            except Error as e:
                tkMessageBox.showerror("Query error","Got error: %s" % e)
            
    def onAddRecEvent(self):
        dlg = d.addRecEventDlg(self)
        
        if not dlg.cancelled:
            try:
                self.dbase.runAddRecEvent(dlg.result)
                #repopulate recevent cache
                getRecEvents="SELECT event_id,record_date,record_type,grid_ref FROM record_event"
                self.dbase.runQuery(getRecEvents)
                self.recEventsRaw = self.dbase.lastResult
            except Error as e:
                tkMessageBox.showerror("Problem adding record event","Got error: %s" % e)  
                
    def onAddRecData(self):
        dlg = d.addRecDataDlg(self,self.dbase) 
        
        if not dlg.cancelled:
            try:
                self.dbase.runAddRecData(dlg.result) 
            except Error as e:
                tkMessageBox.showerror("Problem adding record event","Got error: %s" % e)
                
    def onAddTaxonData(self):
        dlg = d.addTaxonDlg(self)
        
        if not dlg.cancelled:
            try:
                self.dbase.runAddTaxon(dlg.result)
                
                #repopulate taxon data cacahe
                getTaxa = "SELECT genus_name,species_name,vernacular_name,subspecies_name,\
aberration_name,form_name,id FROM taxon_data"
                self.dbase.runQuery(getTaxa)
                self.taxaRaw = self.dbase.lastResult
            except Error as e:
                tkMessageBox.showerror("Problem adding taxon","Got error: %s" % e)
                
    def onUpdateRecEvent(self):
        dlg = d.updateRecEventDlg(self,self.dbase)
        
        if not dlg.cancelled:
            try:
                self.dbase.runUpdateRecEvent(dlg.result)
                #repopulate recevent cache
                getRecEvents="SELECT event_id,record_date,record_type,grid_ref FROM record_event"
                self.dbase.runQuery(getRecEvents)
                self.recEventsRaw = self.dbase.lastResult
            except Error as e:
                tkMessageBox.showerror("Problem updating record event","Got error: %s" % e)
    
    def onUpdateRecData(self):
        pass
    
    def onUpdateTaxonData(self):
        pass
                
    def onExit(self):
        if not self.dbase == False:
            if self.dbase.connected():
                self.dbase.close()
        self.quit()                


        
        
     


#app = Application()                       
#app.master.title('Sample application')    
#app.mainloop() 

root = tk.Tk()
app = Application(root)    
root.mainloop()                   