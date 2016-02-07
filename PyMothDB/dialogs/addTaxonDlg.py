from dialogs import *
from Tkinter import *

class addTaxonDlg(MyDialog):
    
    def body(self,master):
        self.orderLbl = Label(master,text="Order:*")
        self.orderLbl.grid(row=0,column=0,sticky=N+S+E+W)        
        self.orderInp = Entry(master)
        self.orderInp.grid(row=0,column=1,sticky=N+S+E+W)
        
        self.familyLbl = Label(master, text="Family:")
        self.familyLbl.grid(row=1,column=0,sticky=N+S+E+W)
        self.familyInp = Entry(master)
        self.familyInp.grid(row=1, column=1,sticky=N+S+E+W)
        
        self.subFamilyLbl = Label(master, text="Sub-Family:")
        self.subFamilyLbl.grid(row=2,column=0,sticky=N+S+E+W)
        self.subFamilyInp = Entry(master)
        self.subFamilyInp.grid(row=2,column=1,sticky=N+S+E+W)
        
        self.genusLbl = Label(master, text="Genus:*")
        self.genusLbl.grid(row=3,column=0,sticky=N+S+E+W)
        self.genusInp = Entry(master)
        self.genusInp.grid(row=3,column=1,sticky=N+S+E+W)
        
        self.speciesLbl = Label(master, text="Species:*")
        self.speciesLbl.grid(row=4,column=0,sticky=N+S+E+W)
        self.speciesInp = Entry(master)
        self.speciesInp.grid(row=4,column=1, stick=N+S+E+W)
        
        self.subSpLbl = Label(master, text="Sub-species:")
        self.subSpLbl.grid(row=5,column=0,sticky=N+S+E+W)
        self.subSpInp = Entry(master)
        self.subSpInp.grid(row=5,column=1,sticky=N+E+S+W)
        
        self.abLbl = Label(master,text = "Aberration:")
        self.abLbl.grid(row=6,column=0,sticky=N+S+E+W)
        self.abInp = Entry(master)
        self.abInp.grid(row=6,column=1,sticky=N+S+E+W)
        
        self.formLbl = Label(master,text="Form:")
        self.formLbl.grid(row=7,column=0,sticky=N+S+E+W)
        self.formInp = Entry(master)
        self.formInp.grid(row=7,column=1,sticky=N+E+S+W)
        
        self.commonLbl = Label(master,text="Common name:")
        self.commonLbl.grid(row=8,column=0,sticky=N+S+E+W)
        self.commonInp = Entry(master)
        self.commonInp.grid(row=8,column=1,sticky=N+S+E+W)
        
        self.keyLbl = Label(master,text= "Taxon key:")
        self.keyLbl.grid(row=9,column=0,sticky=N+S+E+W)
        self.keyInp = Entry(master)
        self.keyInp.grid(row=9,column=1,sticky=N+S+E+W)
        
        self.reqLbl = Label(master,text = "*required")
        self.reqLbl.grid(row=10,column=0,sticky=N+S+E+W)
        
    def validate(self):
        
        order = self.orderInp.get()
        family = self.familyInp.get()
        subFamily = self.subFamilyInp.get()
        genus = self.genusInp.get()
        species = self.speciesInp.get()
        subSpecies = self.subSpInp.get()
        ab = self.abInp.get()
        f = self.formInp.get()
        commonName = self.commonInp.get()
        key = self.keyInp.get()        
        
        if order and genus and species:
            self.isValid=True 
            return True
        else:
            tkMessageBox.showerror("Record event validation failed","Order: " + order + "\n" 
                    + "Family: " + family + "\n"
                    + "sub-family: " + subFamily + "\n"
                    + "genus: " + genus + "\n"
                    + "species: " + species + "\n"
                    + "sub-species: " + subSpecies + "\n"
                    + "ab.: " + ab + "\n"
                    + "f.: " + f + "\n"
                    + "common name: " + commonName + "\n"
                    + "taxon key: " + key)
        return False
    
    def apply(self):
        order = self.orderInp.get()
        family = self.familyInp.get()
        subFamily = self.subFamilyInp.get()
        genus = self.genusInp.get()
        species = self.speciesInp.get()
        subSpecies = self.subSpInp.get()
        ab = self.abInp.get()
        f = self.formInp.get()
        commonName = self.commonInp.get()
        key = self.keyInp.get()  
        
        self.result = order,family,subFamily,genus,species,subSpecies,ab,f,commonName,key