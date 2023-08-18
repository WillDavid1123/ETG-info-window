#start_screen.py
#This file holds the start_screen class, which creates the starting screen for the program. Users can search an item or gun from 
#   Enter the Gungeon and, if the info for that weapon is found, call the info_screen class to show the item's information.

#Imports
from tkinter import *
from tkinter import ttk
#   Web Scrapping (requests and Beautiful Soup)
import requests #External Library
from bs4 import BeautifulSoup #External Library
#   Displaying Images from URL (PIL/Pillow with TKinter) (WIP)
# from PIL import ImageTk, Image #External Library
#   Helpful imports
import pdb

#Custom Class(es)
from info_screen import info_screen

class start_screen:
    '''Window with search bar and basic explanation of program'''

    def __init__(self, root):
        '''Create window for the start screen'''
        #Setup
        root.title("Enter the Gungeon Info Window")
        self.mainframe = ttk.Frame(root, padding="3 3 3 3")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        #Text Elements
        title = ttk.Label(self.mainframe, text="Enter the Gungeon Info Window", font=('bold', 17)).grid(column=1, row=1)
        use_text = "Enter an item or gun name from Enter the Gungeon to see its stats and synergies"
        use = ttk.Label(self.mainframe, text=use_text).grid(column=1, row=2)
        self.item = StringVar()
        item_entry = ttk.Entry(self.mainframe, width=30, textvariable=self.item)
        item_entry.grid(column=1, row=3)

        #Search button
        ttk.Button(self.mainframe, text="Search", command=self.search).grid(column=1, row=4)

        #Warning label if item doesn't exist
        self.warning = ttk.Label(self.mainframe, text="Item doesn't exist or spelt incorrectly, please try again", foreground="red")
        self.warning.grid(column=1, row=5)

        #Space out elements on the window
        for child in self.mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)
        
        #Ease-of-life keys
        root.bind("<Return>", self.search)
        root.bind("<Escape>", lambda x: root.destroy())
        self.warning.grid_remove()
    
    def search(self, *args):
        '''Search for and, if found, show info for a given item'''
        if self.item.get() != "":
            item_name = self.format_item_name(self.item.get())
            print(item_name)
            self.item.set("")

            req = requests.get("https://enterthegungeon.fandom.com/wiki/" + item_name)

            #Check that the searched item exists
            if req.text.find("no text in this page") == -1: #Info found
                self.warning.grid_remove()
                soup = BeautifulSoup(req.content, "html.parser")
                root_2 = Tk()
                info_screen(root_2, item_name.replace("_", " ").replace("%27", "'").replace("%2B", "+"), soup)
                root_2.mainloop()
            else: #Info not found
                self.warning.grid()

    def format_item_name(self, name):
        '''Format the given item name for web scrapping'''
        new_name = []
        for x in str.split(name, " "):
            if x == "of" or x == "the" or x == "r":
                new_name.append(x)
                continue
            new_name.append(x.capitalize())
        item = "_".join(new_name)
        for i, chr in enumerate(item):
            if chr == "-" and i != len(item) - 1:
                item = item[:i+1] + item[i+1].capitalize() + item[i+2:]

        #Unconventional Naming
        item = self.unconventional_name(item)

        return item.replace("'", "%27").replace("+", "%2B")

    def unconventional_name(self, name):
        '''Fix unconventional names (extra capitals, odd syntax, etc.)'''
        match name:
            #Guns
            case "A.w.p":
                return "A.W.P."
            case "A.w.p.":
                return "A.W.P."
            case "Ac-15":
                return "AC-15"    
            case "Ak-47":
                return "AK-47" 
            case "Akey-47":
                return "AKEY-47"
            case "Au_Gun":
                return "AU_Gun"
            case "Bsg":
                return "BSG"         
            case "Gunner":
                return "GuNNER"
            case "Jk-47":
                return "JK-47"
            case "Mac10":
                return "MAC10"
            case "Rc Rocket":
                return "RC Rocket"
            case "Rpg":
                return "RPG"
            case "Rube-Adyne_Prototype":
                return "RUBE-ADYNE_Prototype"
            case "Rube-Adyne_Mk.ii":
                return "RUBE-ADYNE_MK.II"
            case "Rube-Adyne_Mk.2":
                return "RUBE-ADYNE_MK.II"
            case "Saa":
                return "SAA"    
            case "Vertebraek-47":
                return "VertebraeK-47"
            #Items
            case "Ibomb_Companion_App":
                return "iBomb_Companion_App"
            case _:
                return name
            
if __name__ == "__main__":
    '''Start the main window and put it into an infinite loop'''
    root = Tk()
    start_screen(root)
    root.mainloop()