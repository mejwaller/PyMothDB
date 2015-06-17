#from http://www.effbot.org/tkinterbook/tkinter-dialog-windows.htm

from Tkinter import *

class MyDialog(Toplevel):

    def __init__(self, parent, title = None):

        Toplevel.__init__(self, parent)
        self.transient(parent)

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

        self.cancel()

    def cancel(self, event=None):

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
            self.queryLbl = Label(master,text="Query:")
            self.queryLbl.grid(row=0,column=0, sticky=N+S+E+W)
            self.queryInp = Entry(master)
            self.queryInp.grid(row=0,column=1,sticky=N+S+E+W)
            
    def apply(self):            
            self.result = self.queryInp.get()
            
           

            