#from http://www.effbot.org/tkinterbook/tkinter-dialog-windows.htm

from Tkinter import *
from datetime import datetime, timedelta
import tkMessageBox
import dbcontroller as db

class MyDialog(Toplevel):

    def __init__(self, parent, title = None):
        
        Toplevel.__init__(self, parent)
        self.transient(parent)
        self.cancelled = False
        if title:
            self.title(title)

        self.parent = parent

        self.result = None

        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)

    #
    # construction hooks

    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden

        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = Frame(self)

        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    #
    # standard button semantics

    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()

        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    #override
    def cancel(self, event=None):
        self.cancelled = True
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()
        

    #
    # command hooks

    def validate(self):

        return 1 # override

    def apply(self):

        pass # override
    
    
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
    
class adHocQueryDlg(MyDialog):
        
    def body(self,master):
            self.cancelled = False
            self.queryLbl = Label(master,text="Query:")
            self.queryLbl.grid(row=0,column=0, sticky=N+S+E+W)
            self.queryInp = Entry(master)
            self.queryInp.grid(row=0,column=1,sticky=N+S+E+W)
#            self.entryScroll = Scrollbar(self, orient=HORIZONTAL,command=self.__scrollHandler)
#            self.entryScroll.grid(row=1,column=1, sticky=N+S+E+W)
#            self.queryInp['xscrollcommand'] = self.entryScroll.set
            
    def apply(self):            
        self.result = self.queryInp.get()
         
#    def __scrollHandler(self, *L):
#        op, howMany = L[0], L[1]
#        if op == 'scroll':
#            units = L[2]
#            self.queryInp.xview_scroll(howMany, units)
#        elif op == 'moveto':
#            self.queryInp.xview_moveto(howMany)
            
class addRecEventDlg(MyDialog):
    
    def body(self,master):
        self.isValid = False
        self.dateLbl = Label(master,text="Date (YYYY-MM-DD):")
        self.dateLbl.grid(row=0,column=0,sticky=N+S+E+W)
        self.dateInp = Entry(master)
        #use yesterdays date as default as most likely 
        #we are entering records from last night's trapping
        yesterday = datetime.now()-timedelta(days=1)
        self.dateInp.insert(0,yesterday.strftime("%Y-%m-%d"))      
        self.dateInp.grid(row=0,column=1,sticky=N+S+E+W)
        
        #NOTE: to validate do strptime(<nput>,"%Y-%m-%d")
        
        self.typeLbl = Label(master, text="Record type:")
        self.typeLbl.grid(row=1,column=0,sticky=N+S+E+W)
        self.typeInp = Entry(master)
        self.typeInp.insert(0,"MV Light Trap")
        self.typeInp.grid(row=1,column=1,sticky=N+S+E+W)
        
        self.gridLbl = Label(master,text="Grd ref:")
        self.gridLbl.grid(row=2,column=0,sticky=N+S+E+W)
        self.gridInp = Entry(master)
        self.gridInp.insert(0,"SU993553")
        self.gridInp.grid(row=2,column=1,sticky=N+S+E+W)
        
        self.notesLbl = Label(master,text="Notes:")
        self.notesLbl.grid(row=3,column=0,sticky=N+S+E+W)
        self.notesInp = Text(master)
        self.notesInp.grid(row=3,column=1,sticky=N+S+E+W)
           
    def validate(self):
        try:            
            retval1 = datetime.strptime(self.dateInp.get(),"%Y-%m-%d")
            retval2 = self.typeInp.get() 
            retval3 = self.gridInp.get()
            if retval1 and retval2 and retval3:
                self.isValid=True 
                return True
            else:
                tkMessageBox.showerror("Record event validation failed","date:" + str(retval1) + "\n" 
                    + "type:" + retval2 + "\n"
                    + "gridref:" + retval3 + "\n"
                    + "notes:" + self.notesInp.get())                   
        except ValueError as e:
            self.isValid=False
            tkMessageBox.showerror("Date format error:",e)
        return False
    
    def apply(self):
        #print "receventdlg apply..."
        recDate = self.dateInp.get()
        recType = self.typeInp.get()
        gridRef = self.gridInp.get()
        #see http://stackoverflow.com/questions/14824163/how-to-get-the-input-from-the-tkinter-text-box-widget
        #http://stackoverflow.com/questions/15565384/python-text-widget-get-method
        recNotes = self.notesInp.get(1.0,END)[:-1]
        
        self.result = recDate,recType,gridRef,recNotes

class addRecDataDlg(MyDialog):
    
    def body(self,master):
        self.isValid=False  
        
        #1st, need to select a record event             
        getRecEvents="SELECT event_id,record_date,record_type,grid_ref FROM record_event"
        self.master.dbase.runQuery(getRecEvents)
        self.recEventsRaw = self.master.dbase.lastResult
        self.strrep=""
        self.recEvents = {}
        for items in self.recEventsRaw:
            self.strrep=""
            for parts in items:
                self.strrep += str(parts)
                self.strrep += " "
            self.recEvents[items[0]] = self.strrep                 
        #print self.recEvents               
        self.recEvLbl = Label(master,text="Record event:")
        self.recEvLbl.grid(row=0,column=0,sticky=N+S+E+W)
        
        #from http://code.activestate.com/recipes/578860-setting-up-a-listbox-filter-in-tkinterpython-27/
        self.recev_search = StringVar()
        self.recev_search.trace("w", lambda name, index, mode: self.update_recev_list())
        self.recev_searchEntry = Entry(master, textvariable=self.recev_search, width=13)
        self.recev_searchEntry.grid(row=0,column=1,sticky=N+S+E+W)
        
        #see http://stackoverflow.com/questions/756662/using-multiple-listboxes-in-python-tkinter
        #else can't use multiple Listboxes per window (listbox selection loses focus...use exportseection=0
        self.recEvLBox = Listbox(master,height=4,width=30,exportselection=0)
        self.recEvLBox.grid(row=0,column=2,sticky=N+S+E+W)
        
        
        #2nd. need to chose taxon..
        getTaxa = "SELECT genus_name,species_name,vernacular_name,subspecies_name,\
aberration_name,form_name,id FROM taxon_data"
        self.master.dbase.runQuery(getTaxa)
        self.taxaRaw = self.master.dbase.lastResult
        self.strrep=""
        self.taxa = {}
        for items in self.taxaRaw:
            self.strrep=""
            for parts in items:
                self.strrep += str(parts)
                self.strrep += " "
            #use id (7th item from query) as index...
            self.taxa[items[6]] = self.strrep                 
        #print self.taxa               
        self.taxaLbl = Label(master,text="Species:")
        self.taxaLbl.grid(row=1,column=0,sticky=N+S+E+W)
        
        #from http://code.activestate.com/recipes/578860-setting-up-a-listbox-filter-in-tkinterpython-27/
        self.taxa_search = StringVar()
        self.taxa_search.trace("w", lambda name, index, mode: self.update_taxa_list())
        self.taxa_searchEntry = Entry(master, textvariable=self.taxa_search, width=13)
        self.taxa_searchEntry.grid(row=1,column=1,sticky=N+S+E+W)
        
        
        self.taxaLBox = Listbox(master,height=4,width=50,exportselection=0)
        self.taxaLBox.grid(row=1,column=2,sticky=N+S+E+W)   
        
        # Function for updating the list/doing the search.
        # It needs to be called here to populate the listbox.
        self.update_recev_list()
        self.update_taxa_list()
        
    def update_taxa_list(self):
        search_term = self.taxa_search.get()
        
        self.taxaLBox.delete(0, END)
     
        for item in self.taxa.values():
            #print item
            if search_term.lower() in item.lower():
                self.taxaLBox.insert(END, item)
                
    def update_recev_list(self):
        search_term = self.recev_search.get()
        
        self.recEvLBox.delete(0,END)
        
        for item in self.recEvents.values():
            if search_term.lower() in item.lower():
                self.recEvLBox.insert(0,item)

        
    def apply(self):
        recIndex=self.recEvLBox.curselection()
        if recIndex:           
            #BROWSE selection mode so only 1 can be selected ata time
            #so chosen if not empty will have [0] entry
            self.recev_chosen=self.recEvLBox.get(recIndex[0])
            print "selected event_id " + self.recev_chosen.split(" ")[0]
        
        taxaIndex = self.taxaLBox.curselection()
        if taxaIndex:
            self.taxa_chosen=self.taxaLBox.get(taxaIndex[0])
            print "selected taxa id " + self.taxa_chosen.split()[-1]
        
        
        
        
        
        
        
        
        
        
                   

            