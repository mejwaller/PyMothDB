from dialogs import *
from Tkinter import *

class addRecDataDlg(MyDialog):
    
    def body(self,master):
        self.isValid=False  
        
        #1st, need to select a record event             
        #getRecEvents="SELECT event_id,record_date,record_type,grid_ref FROM record_event"
        #self.master.dbase.runQuery(getRecEvents)
        #self.recEventsRaw = self.master.dbase.lastResult
        self.strrep=""
        self.recEvents = {}
        for items in self.master.recEventsRaw:
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
        #getTaxa = "SELECT genus_name,species_name,vernacular_name,subspecies_name,\
#aberration_name,form_name,id FROM taxon_data"
        #self.master.dbase.runQuery(getTaxa)
        #self.taxaRaw = self.master.dbase.lastResult
        self.strrep=""
        self.taxa = {}
        for items in self.master.taxaRaw:
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
        
        self.countLbl = Label(master,text="Count:")
        self.countLbl.grid(row=3,column=0,sticky=N+S+W+E)
        self.countInp = Entry(master)
        self.countInp.grid(row=3,column=1,sticky=N+S+E+W)
        
        self.notesLbl = Label(master,text="Notes:")
        self.notesLbl.grid(row=4,column=0,sticky=N+S+E+W)
        self.notesInp = Text(master)
        self.notesInp.grid(row=4,column=1,sticky=N+S+E+W)
        
        
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
            #BROWSE selection mode so only 1 can be selected at a time
            #so chosen if not empty will have [0] entry
            self.recev_chosen=self.recEvLBox.get(recIndex[0])
            recEvId = self.recev_chosen.split()[0]
            #print "selected event_id " + recEvId
        
        taxaIndex = self.taxaLBox.curselection()
        if taxaIndex:
            self.taxa_chosen=self.taxaLBox.get(taxaIndex[0])
            #primary key id is at end of data - split() uses generic whitespace as default!
            taxaId = self.taxa_chosen.split()[-1]
            #print "selected taxa id " + taxaId
            
        count=self.countInp.get()
        #if count:
        #    print "Count was " + count
            
        recNotes = self.notesInp.get(1.0,END)[:-1]
        #if recNotes:
        #    print "Notes were " + recNotes
        
        self.result = recEvId,taxaId,count,recNotes
        
    def validate(self):
        recIndex=self.recEvLBox.curselection()
        taxaIndex = self.taxaLBox.curselection()
        rawCount=self.countInp.get()
        
        if recIndex and taxaIndex and rawCount:
            self.isValid=True 
            return True
        else:
            tkMessageBox.showerror("Record event validation failed","record event index: " + str(recIndex) + "\n" 
                    + "taxIndex: " + str(taxaIndex) + "\n"
                    + "count: " + rawCount + "\n"
                    + "notes: " + self.notesInp.get(1.0,END)[:-1])
        return False