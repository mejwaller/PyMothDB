from dialogs import *
from Tkinter import *

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