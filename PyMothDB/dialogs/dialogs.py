#from http://www.effbot.org/tkinterbook/tkinter-dialog-windows.htm

from Tkinter import *
from datetime import datetime, timedelta
import tkMessageBox
#import dbcontroller as db

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
     

        
class updateRecEventDlg(MyDialog):
    
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
        self.recEvLBox.bind('<<ListboxSelect>>', self.onselect)
        
        self.typeLbl = Label(master, text="Record type:")
        self.typeLbl.grid(row=1,column=0,sticky=N+S+E+W)
        self.typeInp = Entry(master)
        #self.typeInp.insert(0,"MV Light Trap")
        self.typeInp.grid(row=1,column=1,sticky=N+S+E+W)
        
        self.gridLbl = Label(master,text="Grid ref:")
        self.gridLbl.grid(row=2,column=0,sticky=N+S+E+W)
        self.gridInp = Entry(master)
        #self.gridInp.insert(0,"SU993553")
        self.gridInp.grid(row=2,column=1,sticky=N+S+E+W)
        
        self.notesLbl = Label(master,text="Notes:")
        self.notesLbl.grid(row=3,column=0,sticky=N+S+E+W)
        self.notesInp = Text(master)
        self.notesInp.grid(row=3,column=1,sticky=N+S+E+W)
        
        # Function for updating the list/doing the search.
        # It needs to be called here to populate the listbox.
        self.update_recev_list()
        
    def update_recev_list(self):
        search_term = self.recev_search.get()
        
        self.recEvLBox.delete(0,END)
        
        for item in self.recEvents.values():
            if search_term.lower() in item.lower():
                self.recEvLBox.insert(0,item)

     
    def validate(self):
   
        retval1 = self.typeInp.get() 
        retval2 = self.gridInp.get()
        retval3 = self.notesInp.get(1.0,END)[:-1]
            
        #notes (retval3) maybe empty
        if retval1 and retval2:
            self.isValid=True 
            return True
        else:
            tkMessageBox.showerror("Record event validation failed","type:" + retval1 + "\n"
                + "gridref:" + retval2 + "\n"
                + "notes:" + retval3)                   
            return False
        
    def apply(self):
        print "updatereceventdlg apply..."        
        recType = self.typeInp.get()
        gridRef = self.gridInp.get()
        #see http://stackoverflow.com/questions/14824163/how-to-get-the-input-from-the-tkinter-text-box-widget
        #http://stackoverflow.com/questions/15565384/python-text-widget-get-method
        recNotes = self.notesInp.get(1.0,END)[:-1]
        
        self.result = self.recevid,recType,gridRef,recNotes
    
    #from http://stackoverflow.com/questions/6554805/getting-a-callback-when-a-tkinter-listbox-selection-is-changed
    def onselect(self,evt):
        # Note here that Tkinter passes an event object to onselect()
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        evid = value.split()[0]  
             
        self.master.dbase.runQuery("SELECT * from record_event where event_id=%s" % evid); 
        queryres=self.master.dbase.lastResult 
        #an array of tuples - in this case an array conatining one tuple i.e. at queryres[0]   
        data = queryres[0];
        #print data;
                
        #see http://effbot.org/tkinterbook/text.htm#Tkinter.Text.insert-method
        #first delete everything (start is 1.0 for Text, 0 for Entry, end is END) then insert at END
        #self.recev_searchEntry.delete(0,END)
        self.typeInp.delete(0,END)
        self.gridInp.delete(0,END)
        self.notesInp.delete(1.0,END)
        
        #populate dialog fields with result
        #self.recev_searchEntry.insert(INSERT,str(data[1]))
        self.typeInp.insert(INSERT,str(data[2]))
        self.gridInp.insert(INSERT,str(data[3]))
        self.notesInp.insert(END,str(data[4]))
        
        #store id
        self.recevid = str(data[0])
           
        
        
        
        
        