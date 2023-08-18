#info_screen.py
#This file holds the info_screen class, which creates a screen that shows information for a given item from Enter the Gungeon. Users
#   can (currently) switch between 2 different pages, one for the basic stats of the item and one for any synergies the item has
#   with other items from the game.

#Imports
#   Graphics and Windows (Tkinter -> Built-in to Python 3.8 on)
from tkinter import *
from tkinter import ttk
#   Web Scrapping (requests and Beautiful Soup)
import requests #External Library
from bs4 import BeautifulSoup #External Library
#   Displaying Images from URL (PIL/Pillow with TKinter) (WIP)
# from PIL import ImageTk, Image #External Library
#   Helpful imports
import pdb

class info_screen:
    '''Window that shows item information (works for guns and items)'''

    def __init__(self, root, item_name, soup):
        '''Give the info window a title and get all info'''
        #Setup
        root.title(item_name)
        self.entry_text_title = ""
        self.entry_text = ""
        info_dict = [] #Each index holds a dict of all information for a single page
        self.win_elements = [] #Each index holds the unique elements of each window
        self.page_titles = ["Base Stats", "Synergies"]
        self.curr_page = 1
        self.num_pages = 2

        #Create window
        win_mainframe = self.create_window(root, item_name)

        #Grab information for each page and create labels for them
        info_dict.append(self.grab_win1_info(soup))
        win_mainframe = self.create_window(root, item_name) #Create window (Must be placed here for code to work)
        self.create_labels(info_dict[0], win_mainframe, 0)
        info_dict.append(self.grab_win2_info(soup))
        self.create_labels(info_dict[1], win_mainframe, 1)
        # print(self.win_elements)

        #Show first page info
        self.add_info(0)
        # print(self.win_elements)

    def grab_win1_info(self, soup):
        '''Grab info off of the given website (basic table info)'''
        info = {} #Keys: category name | values: category values/text
        table = soup.find("table", class_="infoboxtable")
        
        #Grab Text from table
        table_data = table.find_all("tr")
        for i, data in enumerate(table_data):
            if data.text.replace("\n", "") == "Meta Info":
                table_data = table_data[:i]
        
        num_items = len(table_data) - 1 #Find number of labels for the given item
        for i in range(3, num_items - 2):
            image = table_data[i].find("img") #grab image if it exists for the given item
            if i == 4: #Quality shown with an image
                arr = table_data[i].text.split(":")
                info[arr[0].replace("\n", "")] = image["alt"][0]
                continue
            arr = table_data[i].text.split(":")

            if arr[0].replace("\n", "") == "Recharge": #Table includes a recharge table (ex. Partially-Eaten Cheese)
                table = self.recharge_table(arr[1].split("\n"))
                info[arr[0].replace("\n", "")] = table
                continue

            if len(arr) < 2: #Extra table info thats delt with above (ex. Recharge Table)
                continue

            arr[1] = arr[1].replace("\n", "")
            if len(arr) > 2: #Details for stats that have an odd format
                self.fix_details(table_data[i], arr, info)
                continue

            if len(arr[1].replace(" ", "")) == 0: #Details for stats that are only an image or are blank
                if arr[0].replace("\n", "") == "Max Ammo" or arr[0].replace("\n", "") == "Damage" or arr[0].replace("\n", "") == "Range":
                    arr[1] = "Infinite"
                elif arr[0].replace("\n", "") == "Sell Creep Price":
                    arr[1] = "-"
                elif arr[0].replace("\n", "") == "Introduced in":
                    arr[1] = image['alt'].replace(" Indicator", "") + " Update"
            elif arr[0].replace("\n", "") == "Sell Creep Price": #Shell image needs to be replaced
                arr[1] += "Shells"
            info[arr[0].replace("\n", "")] = arr[1].replace("\n", "")
        if info["Quality"] == "N":
            info["Quality"] = "Starter Weapon"

        self.grab_header_info(table_data, num_items - 1)
        return info
    
    def grab_win2_info(self, soup):
        '''Grab info off of the given website (Synergies)'''
        info = {} #Keys: category name | values: category values/text
        synergies = soup.find("div", class_="mw-parser-output").find_all("ul")
        # print(synergies)

        for s in synergies: #Sometimes synergies are on different parts of the page
            #Separate synergies into array
            synergy_data = s.find_all("li")
            
            for syn in synergy_data:
                data = syn.text.split(" - ")
                if len(data) != 2: #Info grabed is not a synergy
                    continue
                info[data[0].replace("\xa0", "")[1:]] = data[1].replace("\xa0", " ")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          

                # print(" -", syn.text.split(" - "))

            # print("Info dict:", info)
        return info

    def grab_header_info(self, data, i):
        '''Grab info thats at the top of every page of the info screen'''
        self.entry_text_title = data[i].text.replace("\n", "")
        self.entry_text = data[i + 1].text.replace("\n", "")

    def recharge_table(self, data):
        '''Create workable text from given recharge table'''
        #Remove all blank indexes from \n
        while data.__contains__(""):
            data.remove("")
        formated_data = ""
        for i, d in enumerate(data):
            formated_data += d
            if i % 2 == 0:
                formated_data += "\t\t"
            else:
                formated_data += "\n"
        return formated_data  
        
    def fix_details(self, data, arr, info):
        '''Fix text with additional ":" characters and breaks for different line displays'''
        desc = data.find_all("td")
        details = list(desc[1].stripped_strings)
        arr[1] = ""
        for i, d in enumerate(details):
            arr[1] += d
            if i != len(details) - 1:
                arr[1] += "\n"
        info[arr[0].replace("\n", "")] = arr[1]

    def create_window(self, root, item_name):
        '''Create info screen with header info'''
        #Setup
        mainframe = ttk.Frame(root, padding="3 3 3 3")
        mainframe.grid(column=10, row=10, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        #Header info
        ttk.Label(mainframe, text=item_name, font=('bold 24 underline')).grid(column=1, row=1, columnspan=10)
        ttk.Label(mainframe, text=self.entry_text_title, font=("times 12")).grid(column=1, row=2, columnspan=10)
        ttk.Label(mainframe, text=self.entry_text, font=("times 10 normal italic"), wraplength=500, justify="center").grid(column=1, row=3, columnspan=10)

        return mainframe

    def create_labels(self, info, mainframe, page):
        '''Create labels for page and immediately hide them for later use'''
        unique_elms = [] #Info labels (saved for later use)

        #Page title (Doesn't follow <Category: Value> format)
        title = self.page_titles[page]
        page_title = ttk.Label(mainframe, text=title, font=('bold 16 underline'))
        page_title.grid(column=1, row=4, columnspan=10)
        unique_elms.append(page_title)
        page_title.grid_remove()

        #All other unique info
        match page:
            case 0:
                unique_elms = self.create_win1_labels(info, mainframe, unique_elms, 5)
            case 1:
                unique_elms = self.create_win2_labels(info, mainframe, unique_elms, 5)
            case _:
                pass

        self.win_elements.append(unique_elms)

    def create_win1_labels(self, info, mainframe, unique_elms, last_row):
        "create page 1 labels for info screen (Base Stats)"
        for i, value in enumerate(info.keys(), 5):
            x = ttk.Label(mainframe, text=value + ":")
            x.grid(column=1, row=i, columnspan=5)
            unique_elms.append(x)
            x.grid_remove()

            x = ttk.Label(mainframe, text=info[value], wraplength=300, justify="center")
            x.grid(column=6, row=i, columnspan=5)
            unique_elms.append(x)
            x.grid_remove()

            last_row += 1

        unique_elms = self.create_page_change_buttons(mainframe, unique_elms, 1, last_row)
            
        return unique_elms

    def create_win2_labels(self, info, mainframe, unique_elms, last_row):
        "create page 2 labels for info screen (Synergies)"
        if len(info.keys()) != 0: #If the item has synergies
            for i, value in enumerate(info.keys(), 5):
                text_color = "black"
                if value.__contains__("Unused"):
                    text_color = "red"
                x = ttk.Label(mainframe, text=value + ":", font=('normal 11 underline'), foreground=text_color)
                x.grid(column=1, row=i, columnspan=5, pady=(10, 10))
                unique_elms.append(x)
                x.grid_remove()

                x = ttk.Label(mainframe, text=info[value], wraplength=300, justify="center", foreground=text_color)
                x.grid(column=6, row=i, columnspan=5, pady=(10, 10))
                unique_elms.append(x)
                x.grid_remove()

                last_row += 1

        else: #The weapon has no synergies
            x = ttk.Label(mainframe, text="This item has no synergies", font=('bold 13'))
            x.grid(column=1, row=5, columnspan=10, pady=(10, 10))
            unique_elms.append(x)
            x.grid_remove()

            last_row += 1
        
        unique_elms = self.create_page_change_buttons(mainframe, unique_elms, 2, last_row)

        return unique_elms

    def create_page_change_buttons(self, mainframe, unique_elms, page_num, r):
        '''Create buttons for changing the page shown'''
        padding = (8, 0)

        button = ttk.Button(mainframe, text="Prev Page", command=lambda: self.change_page(-1))
        button.grid(column=1, row=r, columnspan=3, pady=padding)
        if page_num == 1: #No page before the first
            button.state(["disabled"])
        unique_elms.append(button)
        button.grid_remove()

        x = ttk.Label(mainframe, text=str(page_num) + " / " + str(self.num_pages), justify="center")
        x.grid(column=4, row=r, columnspan=5, pady=padding)
        unique_elms.append(x)
        x.grid_remove()

        button = ttk.Button(mainframe, text="Next Page", command=lambda: self.change_page(1))
        button.grid(column=8, row=r, columnspan=3, pady=padding)
        if page_num == self.num_pages: #No page after the last
            button.state(["disabled"])
        unique_elms.append(button)
        button.grid_remove()

        return unique_elms

        # ttk.Button(self.mainframe, text="Search", command=self.search).grid(column=1, row=4)

    def change_page(self, change):
        '''Change shown page either to the prev or next page'''
        page = self.curr_page - 1
        #Remove current page labels
        self.remove_info(page)

        #Change variables to match new state
        page += change
        self.curr_page += change

        #Add next wanted page labels
        self.add_info(page)

    def add_info(self, page_num):
        '''Add unique page info to window'''
        labels = self.win_elements[page_num]
        for l in labels:
            l.grid()

    def remove_info(self, page_num):
        '''remove unique page info from window'''
        labels = self.win_elements[page_num]
        for l in labels:
            l.grid_remove()

if __name__ == "__main__":
    '''Start the main window and put it into an infinite loop'''
    root = Tk()
    soup = BeautifulSoup((requests.get("https://enterthegungeon.fandom.com/wiki/Cold_45").content), "html.parser")
    info_screen(root, "Cold 45", soup)
    root.mainloop()