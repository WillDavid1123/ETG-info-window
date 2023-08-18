#Main.py
#Hub file for Enter the Gungeon information window. This program is meant to make searching for item info
#   easy and simple using info from the Gungeon Wiki

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

#Custom Class(es)
from start_screen import start_screen


if __name__ == "__main__":
    '''Start the main window and put it into an infinite loop'''
    root = Tk()
    start_screen(root)
    root.mainloop()



# Image code that doesn't work yet
    #Images
        # images = table.find_all("img")
        # info["Gun Image"] = images[0].get("src")
        # info["Quality"] = images[1].get("src") 

        # print(table_data[1].find("a").find("img")["src"])
        # image_data = requests.get("https://static.wikia.nocookie.net/enterthegungeon_gamepedia/images/c/c2/Cold_45.png").content
        # image = Image.open(image_data)
        # image.show()
        # # image_url = Image.open(image_url)

        #Image of gun
        # gun_image = ttk.Label(mainframe, image=info["Gun Image"]).grid(column=1, row=4, rowspan=5, columnspan=5)

        # image = None #Holds image within table record/row# 