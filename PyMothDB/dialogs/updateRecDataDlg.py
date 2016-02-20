from dialogs import *
from Tkinter import *

class updateRecDataDlg(MyDialog):
    
    def body(self,master):
        self.isValid=False  
        
        #1st select a record event and list the available records
        
        #format record event data for populating recEvLbox below
        self.strrep=""
        self.recEvents = {}
        for items in self.master.recEventsRaw:
            self.strrep=""
            for parts in items:
                self.strrep += str(parts)
                self.strrep += " "
            self.recEvents[items[0]] = self.strrep 
            
        #setup records
        self.recs = {}  
            
        #create label
        self.recEvLbl = Label(master,text="Record event:")
        self.recEvLbl.grid(row=0,column=0,sticky=N+S+E+W)  
        
        #create recev search field
        #from http://code.activestate.com/recipes/578860-setting-up-a-listbox-filter-in-tkinterpython-27/
        self.recev_search = StringVar()
        self.recev_search.trace("w", lambda name, index, mode: self.update_recev_list())
        self.recev_searchEntry = Entry(master, textvariable=self.recev_search, width=13)
        self.recev_searchEntry.grid(row=0,column=1,sticky=N+S+E+W)      
        
        #create recev list box
        #see http://stackoverflow.com/questions/756662/using-multiple-listboxes-in-python-tkinter
        #else can't use multiple Listboxes per window (listbox selection loses focus...use exportseection=0
        self.recEvLBox = Listbox(master,height=4,width=30,exportselection=0)
        self.recEvLBox.grid(row=0,column=2,sticky=N+S+E+W)
        self.recEvLBox.bind('<<ListboxSelect>>', self.onselectRecEv)
        
        #create record label
        self.recLbl = Label(master,text="Record:")
        self.recLbl.grid(row=1, column=0,sticky=N+S+E+W)
        
        #create record search field
        #from http://code.activestate.com/recipes/578860-setting-up-a-listbox-filter-in-tkinterpython-27/
        self.rec_search = StringVar()
        self.rec_search.trace("w", lambda name, index, mode: self.update_rec_list())
        self.rec_searchEntry = Entry(master, textvariable=self.rec_search, width=13)
        self.rec_searchEntry.grid(row=1,column=1,sticky=N+S+E+W)
        
        
        
        # Function for updating the list/doing the search.
        # It needs to be called here to populate the listbox.
        self.update_recev_list()
        
    def update_recev_list(self):
        search_term = self.recev_search.get()
        
        self.recEvLBox.delete(0,END)
        
        for item in self.recEvents.values():
            if search_term.lower() in item.lower():
                self.recEvLBox.insert(0,item)
                
    def update_rec_list(self):
        search_term = self.rec_search.get()
        
        self.recLbox.delete(0,END)
        
        for item in self.recs.values():
            if search_term.lower() in item.lower():
                self.recLbox.insert(0,item)
                
    def validate(self):
        
        #validate fields
        return True
   
        #retval1 = self.typeInp.get() 
        #retval2 = self.gridInp.get()
        #retval3 = self.notesInp.get(1.0,END)[:-1]
            
        #notes (retval3) maybe empty
        #if retval1 and retval2:
        #    self.isValid=True 
        #    return True
        #else:
        #    tkMessageBox.showerror("Record event validation failed","type:" + retval1 + "\n"
        #        + "gridref:" + retval2 + "\n"
        #        + "notes:" + retval3)                   
        #    return False
        
    def apply(self):
        print "updaterecdatadlg apply..."   
        
        #get and return inputs
             
        #recType = self.typeInp.get()
        #gridRef = self.gridInp.get()
        #see http://stackoverflow.com/questions/14824163/how-to-get-the-input-from-the-tkinter-text-box-widget
        #http://stackoverflow.com/questions/15565384/python-text-widget-get-method
        #recNotes = self.notesInp.get(1.0,END)[:-1]
        
        #self.result = self.recevid,recType,gridRef,recNotes
        
    #from http://stackoverflow.com/questions/6554805/getting-a-callback-when-a-tkinter-listbox-selection-is-changed
    def onselectRecEv(self,evt):
        #get all associated records and populate record lbox
        # Note here that Tkinter passes an event object to onselect()
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        evid = value.split()[0]  
        
        self.master.dbase.runQuery("SELECT * from record_data where recevent_id = %s" % evid)
        queryres=self.master.dbase.lastResult 
        #an array of tuples - in this case an array conatining one tuple i.e. at queryres[0]   
        data = queryres[0];
        print data;
        
        #===== from receventupdate - different use case...     
        #self.master.dbase.runQuery("SELECT * from record_event where event_id=%s" % evid); 
        #queryres=self.master.dbase.lastResult 
        #an array of tuples - in this case an array conatining one tuple i.e. at queryres[0]   
        #data = queryres[0];
        #print data;
                
        #see http://effbot.org/tkinterbook/text.htm#Tkinter.Text.insert-method
        #first delete everything (start is 1.0 for Text, 0 for Entry, end is END) then insert at END
        #self.recev_searchEntry.delete(0,END)
        #self.typeInp.delete(0,END)
        #self.gridInp.delete(0,END)
        #self.notesInp.delete(1.0,END)
        
        #populate dialog fields with result
        #self.recev_searchEntry.insert(INSERT,str(data[1]))
        #self.typeInp.insert(INSERT,str(data[2]))
        #self.gridInp.insert(INSERT,str(data[3]))
        #self.notesInp.insert(END,str(data[4]))
        
        #store id
        #self.recevid = str(data[0])
        
        