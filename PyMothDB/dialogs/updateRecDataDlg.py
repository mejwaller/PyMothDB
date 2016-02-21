from dialogs import *
from Tkinter import *

class updateRecDataDlg(MyDialog):
    
    def body(self,master):
        self.isValid=False  
        
        #1st select a record event and list the available records
        self.selectedRecEvent=""
        
        #format record event data for populating recEvLbox below
        self.strrep=""
        self.recEvents = {}
        self.recDatEvents = {}
        for items in self.master.recEventsRaw:
            self.strrep=""
            for parts in items:
                self.strrep += str(parts)
                self.strrep += " "
            self.recEvents[items[0]] = self.strrep 
            self.recDatEvents[items[0]] = self.strrep 
            
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
        
        #create record list - to show vernacular genus, species, subsp, var,ab
        #when selected populate new record event, count and notes fields below for altering data in
        self.recLBox = Listbox(master, height=4, width=50,exportselection=0)
        self.recLBox.grid(row=1,column=2,sticky=N+S+E+W)
        self.recLBox.bind('<<ListboxSelect>>', self.onselectRec)
        
        self.recDatEvLbl = Label(master,text="Record event:")
        self.recDatEvLbl.grid(row=2,column=0,sticky=N+S+E+W)
        
        self.recDatEvSearch = StringVar()
        self.recDatEvSearch.trace("w", lambda name, index, mode: self.update_datRecev_list())
        self.recDatEvSearchEntry = Entry(master, textvariable=self.recDatEvSearch, width=13)
        self.recDatEvSearchEntry.grid(row=2,column=1,sticky=N+S+E+W)
        
        #create recev for selected data list box
        #see http://stackoverflow.com/questions/756662/using-multiple-listboxes-in-python-tkinter
        #else can't use multiple Listboxes per window (listbox selection loses focus...use exportseection=0
        self.recDatEvLBox = Listbox(master,height=4,width=30,exportselection=0)
        self.recDatEvLBox.grid(row=2,column=2,sticky=N+S+E+W)
        #this use case is to populate record's record event input
        self.recDatEvLBox.bind('<<ListboxSelect>>', self.onselectRecDatEv)
        
        self.countLbl = Label(master,text="Count:")
        self.countLbl.grid(row=3,column=0,sticky=N+S+E+W)
        
        self.countInp = Entry(master)
        self.countInp.grid(row=3, column=1, sticky=N+S+E+W)
        
        self.notesLbl = Label(master,text="Notes:")
        self.notesLbl.grid(row=4,column=0,sticky=N+S+E+W)
        
        self.notesInp = Text(master)
        self.notesInp.grid(row=4,column=1,sticky=N+S+E+W)
        
        # Function for updating the list/doing the search.
        # It needs to be called here to populate the listbox.
        self.update_recev_list()
        
    def update_recev_list(self):
        search_term = self.recev_search.get()
        
        self.recEvLBox.delete(0,END)
        
        for item in self.recEvents.values():
            if search_term.lower() in item.lower():
                self.recEvLBox.insert(0,item)
                
    def update_datRecev_list(self):
        search_term = self.recDatEvSearch.get()
        
        self.recDatEvLBox.delete(0,END)
        
        for item in self.recDatEvents.values():
            if search_term.lower() in item.lower():
                self.recDatEvLBox.insert(0,item)
                
    def update_rec_list(self):
        search_term = self.rec_search.get()
        
        self.recLBox.delete(0,END)
        
        for item in self.recs.values():
            if search_term.lower() in item.lower():
                self.recLBox.insert(0,item)
                
    def validate(self):
        
        #validate fields
        #note this field should have valid recevent_id as first entry - not validated here!
        retval1 = self.recDatEvSearchEntry.get() 
        retval2 = self.countInp.get()
        retval3 = self.notesInp.get(1.0,END)[:-1]
        
        #notes (retval3) maybe empty
        if retval1 and retval2:
            self.isValid=True 
            return True
        else:
            tkMessageBox.showerror("Record data validation failed","redord event:" + retval1 + "\n"
                + "count:" + retval2 + "\n"
                + "notes:" + retval3)                   
            return False
        
    def apply(self):
        print "updaterecdatadlg apply..."   
        
        #get and return inputs
             
        recevid = self.recDatEvSearchEntry.get().split()[0] 
        count = self.countInp.get()
        #see http://stackoverflow.com/questions/14824163/how-to-get-the-input-from-the-tkinter-text-box-widget
        #http://stackoverflow.com/questions/15565384/python-text-widget-get-method
        recNotes = self.notesInp.get(1.0,END)[:-1]
        
        self.result = self.recId,recevid,count,recNotes
        
    #from http://stackoverflow.com/questions/6554805/getting-a-callback-when-a-tkinter-listbox-selection-is-changed
    def onselectRecEv(self,evt):
        #get all associated records and populate record lbox
        # Note here that Tkinter passes an event object to onselect()
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        evid = value.split()[0]  
        
        self.master.dbase.runQuery("SELECT r.record_id, t.vernacular_name, t.genus_name, t.species_name, \
        t.subspecies_name, t.aberration_name, t.form_name, r.count, r.recevent_id, r.notes, \
        e.record_date, e.record_type, e.grid_ref \
        FROM taxon_data as t, record_data as r, record_event as e \
        WHERE r.recevent_id = %s \
        AND t.id = r.taxon_id \
        AND e.event_id = %s" % (evid, evid))
        self.queryres=self.master.dbase.lastResult 
        #an array of tuples - in this case an array containing records for given date   
        data = self.queryres;
        print data;
        
        self.recs = {} 
        asStr=""
        for records in data:
            asStr=""
            for fields in records:
                asStr += str(fields)
                asStr += " "
            self.recs[records[0]] = asStr
            #print asStr
            
        self.update_rec_list()
        
        #store recevent data as string for access later (to populate selected record data event
        #print "record: %s" % str(records[10])
        self.selectedRecEvent = evid + " " + str(records[10]) + " " + str(records[11]) + " " + str(records[12])
            
        
    def onselectRec(self,evt):
        #widget sleected
        w = evt.widget
        #index of selection
        index = int(w.curselection()[0])
        value = w.get(index)
        print "value of widget slected index: "
        print value
        
        self.update_datRecev_list()
        
        print "record index is %s" % value.split()[0]
        
        self.master.dbase.runQuery("SELECT record_id, count,notes FROM record_data where record_id = %s" % value.split()[0])
        self.queryres=self.master.dbase.lastResult
        
        #print self.queryres
                
        #see http://effbot.org/tkinterbook/text.htm#Tkinter.Text.insert-method
        #first delete everything (start is 1.0 for Text, 0 for Entry, end is END) then insert at END
        self.recDatEvSearchEntry.delete(0,END)
        self.countInp.delete(0,END)
        self.notesInp.delete(1.0,END)
        
        #populate dialog fields with result
        self.recDatEvSearchEntry.insert(INSERT,self.selectedRecEvent)
        self.recId = str(self.queryres[0][0])
        self.countInp.insert(INSERT,str(self.queryres[0][1]))
        self.notesInp.insert(END,str(self.queryres[0][2]))
                
    def onselectRecDatEv(self,evt):
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        
        self.recDatEvSearchEntry.delete(0,END)
        
        self.recDatEvSearchEntry.insert(INSERT, str(value))
        
        
            
        
        