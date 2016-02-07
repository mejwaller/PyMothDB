
from dialogs import *
from Tkinter import *

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