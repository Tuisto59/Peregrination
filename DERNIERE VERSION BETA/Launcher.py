#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(c) Copyright Yoan BOUZIN

  This file is part of Pérégrination v1.0.

    Pérégrination v2.0 is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Pérégrination v2.0 is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Pérégrination v2.0.  If not, see <http://www.gnu.org/licenses/>. 2
"""

###########
# IMPORTS #
###########

from __future__ import division
from peregrination import *
import Tkinter
import tkFileDialog
import tkMessageBox
import ttk
import time
import re
import requests
import urllib2
from difflib import SequenceMatcher
import glob
import random

import csv
import os
import shutil
import webbrowser
import tkFont

### NON NATIVE PACKAGE ###

import shapefile
import gedcom
#from geopy.geocoders import Nominatim #because with py2exe not work
from staticmap import StaticMap, CircleMarker

######
# GUI #
######

cert = 'cacert.pem'
os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(os.getcwd(), cert)

GOOGLE_API = []

class Peregrination():
    #principal application
    def __init__(self):
        """
        initialize the GUI
        """
        #check platform
        from sys import platform
        if platform == "linux" or platform == "linux2":
            font = "URW Chancery L"
        elif platform == "darwin":
            font = "URW Chancery L"
        elif platform == "win32":
            font = "Segoe Script"
        self.main = Tkinter.Tk()
        self.main.title("Pérégrination v2.0")
        self.main.resizable(width=False, height=False)
        self.main.configure(bg="#a0522d")
        self.main.grab_set()
        self.main.focus_set()
        iconImage=Tkinter.PhotoImage(master=self.main, data=icon)
        self.label1 = Tkinter.Label(self.main,image=iconImage)
        self.label1.image = iconImage # keep a reference!
        self.label1.grid(sticky='EW', padx=10, pady=5)
        
        self.step1 = Tkinter.Button(self.main, text="Etape 1: Import du fichier GEDCOM",command=self.gedcom_step1, bg="#f5deb3")
        self.step1.grid(sticky="NSEW")
        self.step1.bind('<Return>', self.gedcom_step1)
        self.step1.focus_set()
        
        self.step2 = Tkinter.Button(self.main, text="Etape 2: Correspondance des lieux",command=self.gedcom_step2, bg="#f5deb3", activebackground="#f5deb3")
        self.step2.grid(sticky="NSEW")
        self.step2.bind('<Return>', self.gedcom_step2)
        self.step2.config(state='disabled')
        
        self.step3 = Tkinter.Button(self.main, text="Etape 3: Recherche des coordonées GPS",command=self.gedcom_step3, bg="#f5deb3", activebackground="#f5deb3")
        self.step3.grid(sticky="NSEW")
        self.step3.bind('<Return>', self.gedcom_step3)
        self.step3.config(state='disabled')
        
        self.step4 = Tkinter.Button(self.main, text="Etape 4: Sélection de la personne",command=self.gedcom_step4, bg="#f5deb3", activebackground="#f5deb3")
        self.step4.grid(sticky="NSEW")
        self.step4.bind('<Return>', self.gedcom_step4)
        self.step4.config(state='disabled')
        
        self.step5= Tkinter.Button(self.main, text="Etape 5: Options d'affichage",command=self.gedcom_step5, bg="#f5deb3", activebackground="#f5deb3")
        self.step5.grid(sticky="NSEW")
        self.step5.bind('<Return>', self.gedcom_step5)
        self.step5.config(state='disabled')
        
        self.step6= Tkinter.Button(self.main, text="Etape 6: Créer la carte des périgrinations",command=self.gedcom_step6, bg="#f5deb3",activebackground="#f5deb3")
        self.step6.grid(sticky="NSEW")
        self.step6.bind('<Return>', self.gedcom_step6)
        self.step6.config(state='disabled')
        
        self.step7= Tkinter.Button(self.main, text="Quitter",command=self.main.destroy, bg="#f5deb3")
        self.step7.grid(sticky="NSEW")
        
        self.label1 = Tkinter.Label(self.main,text="© Yoan BOUZIN - Licence GNU", font=(font, 12), bg="#f5deb3")
        self.label1.grid(sticky='EW', padx=10, pady=5)

        ##########
        # VARIABLES #
        ##########
        
        self.fichier_ascendance = None
        self.fichier_descendance = None
        self.fichier_lieux = None
        self.choosen_options = list()
        self.fichier_gedcom = None
        self.parsed_gedcom = None
        self.GoogleAPI_index = 1
        
    def run(self):
        """
        Keep the GUI in live
        """
        self.center(self.main)
        self.main.mainloop()
    def center(self,toplevel):
        """
        To center a Tkinter TopLevel() window
        """
        toplevel.update_idletasks()
        w = toplevel.winfo_screenwidth()
        h = toplevel.winfo_screenheight()
        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

    def progress_bar(self):
        """
        Progress bar with virtual console
        Display the progression of an event
        """
        self.pb_gui = Tkinter.Toplevel()
        self.pb_gui.grab_set()
        self.pb_gui.focus_set()
        self.frame_pb = ttk.Frame(self.pb_gui)
        self.frame_pb.grid()
        self.pb = ttk.Progressbar(self.frame_pb, orien='horizontal', mode='determinate', length=500)
        self.pb.grid(row=0, column=0, sticky="EW")
        self.pb["value"] = 0
        self.pb["maximum"] = 100
        
        self.label_pb = Tkinter.Label(self.frame_pb)
        self.label_pb.grid(row=0,column=1)
        
        self.label_town_pb = Tkinter.Label(self.frame_pb)
        self.label_town_pb.grid(row=1,column=0,columnspan=2)

        #====== FRAME CONSOLE ======
            #first frame
        self.frameConsole = Tkinter.Frame(self.pb_gui)
        self.frameConsole.grid(row=9, columnspan=10,rowspan=10,sticky='EW')
        
            #first canvas
        self.canvasConsole = Tkinter.Canvas(self.frameConsole, height=130, width=500, bg="black")
        self.canvasConsole.grid(row=0, sticky="EW")
            #second frame
        self.console = Tkinter.Frame(self.canvasConsole)
        self.console.config(relief='sunken', bg="black", height=130, width=500)
        self.console.grid(row=0,sticky="EW")
        
            #scrollbar
        self.vsbc = Tkinter.Scrollbar(self.frameConsole,command=self.canvasConsole.yview)
        self.hsbc = Tkinter.Scrollbar(self.frameConsole, orient='horizontal', command=self.canvasConsole.xview)
            #configure scrollbar
        self.canvasConsole.configure(yscrollcommand=self.vsbc.set, xscrollcommand=self.hsbc.set)
        self.canvasConsole.create_window((0,0),window=self.console,anchor='nw')
            #positions
        self.vsbc.grid(row=0,column=3, sticky="NS")
        self.hsbc.grid(row=1,column=0, sticky="WE")
        
        #label position in console
        self.row = 0
        self.label_console = Tkinter.Label(self.console, bg='black', justify='left')

    def update_virtual_console(self, text=False,fg='white',same=False,label_prog=False,label_title=False,value=False):
        """
        Display the message in the progress bar console
        input :
            text :(string) : text to display in the 'virtual console', default set to FALSE
            same (bool) : if TRUE, we us the last label to replace his text, default set to FALSE
            label_prog (bool/float) : if TRUE, we change the text of the progression in the label '[number] %'
            label_title (bool/string) : if TRUE, change the text by the given text
            value (bool/float or integer) : if TRUE, change the value of the tkk.Progressbar for the visualisation
        """
        if label_prog:
            self.label_pb['text'] = str(label_prog)+' %'
        if label_title:
            self.label_town_pb['text'] = label_title
        if value:
            self.pb['value'] = value
            
        if self.row == 1000:
            self.row = 0
            for widget in self.console.winfo_children():
                widget.destroy()
        # update the row increment
        if text:
            if not same:
            #create the label in the console
                label = Tkinter.Label(self.console,text=text,bg='black',fg=fg, justify='left')
                label.grid(row=self.row,sticky="W")
                self.row = self.row+1
            else:
                self.label_console['text'] = text
                self.label_console['fg'] = fg
                self.label_console.grid(row=self.row,sticky="EW")
            # adapt and update the canvas content to the scroll bar
            self.canvasConsole.config(scrollregion=self.canvasConsole.bbox("all"))
            self.canvasConsole.yview_moveto(1.)
        ##update the Progress Bar GUI
        self.pb_gui.update_idletasks()
        self.pb_gui.update()
        
    def control_map_places(self, filename):
        """
        Control the geolocalisation by showing the geocoded Places on a Map
        All the Map come from OpenStreetMap data
        All  for all the town are downloaded (places with identical coordinate are grouping)
        By button and some command, the User check if the automated localisation have been work well
        """
        
        #run the function to get the images
        self.load_image_from_file(filename)

        #make the gui
        self.control = Tkinter.Toplevel()
        self.control.config( bg="#a0522d")
        self.control.grab_set()
        self.control.focus_set()
        self.control.title("Pérégrination v2.0 - Controlleur visuel des lieux géolocalisés")
        #self.control.configure(bg="#a0522d")
        self.label_titre = Tkinter.Label(self.control, text="Vérification des lieux",bg="#a0522d",fg='#f5deb3',font=(None,10,'bold'))
        self.label_titre.grid(column=0,row=0, columnspan = 4)
        self.number = 1
        self.label_lieux = Tkinter.Label(self.control,text="\n".join(self.dico_coordinate[self.index_dico_coordinate[self.number]]),bg="#a0522d",fg='#f5deb3',relief= 'ridge')
        self.label_lieux.grid(column=0,columnspan = 4, row = 1)
        self.info = Tkinter.Label(self.control, text="(Pour visionner la carte dans son ensemble, cliquer sur l'image, ou sur le bouton \" + \" )",bg="#a0522d",fg='#f5deb3', font=(None, 10, 'italic'))
        self.info.grid(column=0,row=2,columnspan=4)
        #image
        iconImage=Tkinter.PhotoImage(file=self.dico_pictures[self.number])
        self.label1 = Tkinter.Label(self.control,image=iconImage, relief='sunken',cursor="hand2")
        self.label1.image = iconImage # keep a reference!
        self.label1.grid(column=0, row=3, rowspan= 11, sticky='EW', padx=10, pady=5)
        self.label1.bind("<Button-1>", self.plus)
        
        #commande
        self.number_town = Tkinter.Label(self.control, text=' '+str(self.number)+'/'+str(len(self.index_dico_coordinate))+' ',bg="#a0522d",fg='#f5deb3',relief= 'ridge')
        self.number_town.grid(column=1, columnspan=3, row=3)
        self.left_button =Tkinter.Button(self.control, text= " < ",command=self.left,fg="#a0522d",bg='#f5deb3',font=(None, 12, 'bold'))
        self.left_button.grid(column=1,row=4)
        self.left_button.bind('<Return>', self.left)
        self.left_button.bind('<Left>', self.left)
        self.plus_button =Tkinter.Button(self.control, text= " + ",command=self.plus,fg="#a0522d",bg='#f5deb3',font=(None, 12, 'bold'))
        self.plus_button.grid(column=2, row=4)
        self.plus_button.bind('<Return>', self.plus)
        self.right_button =Tkinter.Button(self.control, text= " > ",command=self.right,fg="#a0522d",bg='#f5deb3',font=(None, 12, 'bold'))
        self.right_button.grid(column=3, row=4)
        self.right_button.bind('<Return>', self.right)
        self.right_button.bind('<Right>', self.right)
        self.right_button.focus_set()
        self.current_lon = Tkinter.Label(self.control, text='Longitude : '+str(self.index_dico_coordinate[self.number][0]),bg="#a0522d",fg='#f5deb3')
        self.current_lon.grid(column = 1 , row = 5 , columnspan = 3)
        self.current_lat = Tkinter.Label(self.control, text='Latitude : '+str(self.index_dico_coordinate[self.number][1]),bg="#a0522d",fg='#f5deb3')
        self.current_lat.grid(column = 1 , row = 6 , columnspan = 3)

        #to control value of Entry
        vcmd = (self.control.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        
        self.label_modifier = Tkinter.Label(self.control, text='Modifier : ',bg="#a0522d",fg='#f5deb3')
        self.label_modifier.grid(column = 1 , row = 7 , columnspan = 3)
        underline_font = tkFont.Font(self.label_modifier, self.label_modifier.cget("font"))
        underline_font.configure(underline = True)
        self.label_modifier.configure(font=underline_font)
        
        self.new_lon = Tkinter.Label(self.control, text='Longitude : ',bg="#a0522d",fg='#f5deb3')
        self.new_lon.grid(column = 1 , row = 8 , columnspan = 3)
        self.entry_lon = Tkinter.Entry(self.control, validate = 'key', validatecommand = vcmd)
        self.entry_lon.grid(column = 1 , row = 9 , columnspan = 3, padx=5)
        self.new_lat = Tkinter.Label(self.control, text='Latitude : ',bg="#a0522d",fg='#f5deb3')
        self.new_lat.grid(column = 1 , row = 10 , columnspan = 3)
        self.entry_lat = Tkinter.Entry(self.control, validate = 'key', validatecommand = vcmd)
        self.entry_lat.grid(column = 1 , row = 11 , columnspan = 3, padx=5)
        self.button_validate = Tkinter.Button(self.control, text="Mettre à jour les\ncoordonées GPS\npour ce lieu", command=self.change_coordinate,fg="#a0522d",bg='#f5deb3')
        self.button_validate.grid(column = 1 , row = 12 , columnspan = 3)
        self.button_validate.bind('<Return>', self.change_coordinate)
        self.button_validate = Tkinter.Button(self.control, text="Quitter", command=self.control_map_quit,fg="#a0522d",bg='#f5deb3')
        self.button_validate.grid(column = 1 , row = 13 , columnspan = 3)
        self.button_validate.bind('<Return>', self.control_map_quit)
        
    def control_map_quit(self, *args):
        """
        Destroy the control_map_gui
        """
        self.control.destroy()
        self.main.grab_set()
        self.main.focus_set()
        self.step4.config(state="active")
        self.step4.focus_set()
        
    def load_image_from_file(self,f):
        """
        create image from OSM for all Places
        """
        #check folder
        if not os.path.exists('Tmp'):
            os.makedirs('Tmp')
        else:
            #delete the folder with his content and create a new one
            shutil.rmtree('Tmp')
            os.makedirs('Tmp')
        #counter
        cpt = 0
        #loop through data and get picture from tile OSM
        a = time.time()
        self.dico_coordinate = dict()
        
        for town, (y, x) in f.items():
            if (x,y) not in self.dico_coordinate.keys():
                self.dico_coordinate[(x,y)] = [town]
            else:
                self.dico_coordinate[(x,y)] += [town]

        self.dico_pictures = dict()
        self.index_dico_coordinate = dict()
        self.progress_bar()
        cpt = 1
        for (x,y) in self.dico_coordinate.keys():
            town_string = '\n'.join(self.dico_coordinate[(x,y)])
            self.update_virtual_console(text=str(cpt)+"/"+str(len(self.dico_coordinate))+' : '+town_string+'\n'+str(y)+', '+str(x),
                                        label_title= str(cpt)+"/"+str(len(self.dico_coordinate))+' : '+town_string,
                                        label_prog= round(cpt/len(self.dico_coordinate)*100,2),
                                        value=int(cpt/len(self.dico_coordinate)*100))
            #largeur, hauteur
            m = StaticMap(600, 300, url_template='http://a.tile.osm.org/{z}/{x}/{y}.png')
            #longitude = x, latitude=y , create marker (because its not work without) , 
            marker = CircleMarker((x, y),'#0036FF', 5)
            m.add_marker(marker)
            #set zoom : 13 = village area
            image = m.render(zoom=13)
            #save
            picture_file = os.getcwd()+'/Tmp/control'+str(cpt)+'.gif'
            image.save(picture_file)
            self.dico_pictures[cpt]=picture_file
            self.index_dico_coordinate[cpt] = (x,y)
            cpt+=1
        b = time.time()
        seconds = b-a
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        self.pb_gui.destroy()
        tkMessageBox.showinfo(title='Terminé' , message= 'Terminé en %d:%02d:%02d secondes' % (h, m, s))
        
    def left(self, *args):
        """
        Go to the next town
        """
        #control
        if self.number != 1:
            self.number -= 1
            self.label_lieux['text'] ="\n".join(self.dico_coordinate[self.index_dico_coordinate[self.number]])
            self.number_town['text'] = ' '+str(self.number)+'/'+str(len(self.index_dico_coordinate))+' '
            self.current_lon['text'] = 'Longitude : '+str(self.index_dico_coordinate[self.number][0])
            self.current_lat['text'] = 'Latitude : '+str(self.index_dico_coordinate[self.number][1])
            iconImage=Tkinter.PhotoImage(file=self.dico_pictures[self.number])
            self.label1['image'] = iconImage
            self.label1.image = iconImage # keep a reference!
            self.entry_lat.delete(0, 'end')
            self.entry_lon.delete(0, 'end')
            self.control.update_idletasks()
            
            
    def right(self, *args):
        """
        Go to the next town
        """
        #control
        len_idx = len(self.index_dico_coordinate)
        if self.number != len_idx:
            self.number += 1
            self.label_lieux['text'] ="\n".join(self.dico_coordinate[self.index_dico_coordinate[self.number]])
            self.number_town['text'] = ' '+str(self.number)+'/'+str(len(self.index_dico_coordinate))+' '
            self.current_lon['text'] = 'Longitude : '+str(self.index_dico_coordinate[self.number][0])
            self.current_lat['text'] = 'Latitude : '+str(self.index_dico_coordinate[self.number][1])
            iconImage=Tkinter.PhotoImage(file=self.dico_pictures[self.number])
            self.label1['image'] = iconImage
            self.label1.image = iconImage # keep a reference!
            self.entry_lat.delete(0, 'end')
            self.entry_lon.delete(0, 'end')
            self.control.update_idletasks()
            
    def plus(self, *args):
        """
        Open default browser with GogleMap to the actual latitude and longitude coordinate
        """
        x, y = self.index_dico_coordinate[self.number]
        #webbrowser.open('https://www.google.com/maps/preview/@'+str(y)+','+str(x)+',20z')
        webbrowser.open('http://maps.google.com/maps?q='+str(y)+','+str(x)+'&z=15')
        
    def validate(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        #for copy-paste from clipboard
        if len(text) > 1:
            for c in text:
                if c not in '0123456789.-':
                    tkMessageBox.showerror(title='Caractère non autorisé',message='Le caractère "'+c+'" n\'est pas autorisé')
                    return False
            return True
        elif text in '0123456789.-':
            return True
        else:
            return False
        
    def change_coordinate(self, *args):
        """
        change the coordinate in the CSV File
        """
        #Get the entry value
        latitude = float(self.entry_lat.get())
        longitude = float(self.entry_lon.get())
        #get old value and key for dict
        lon_lat = self.index_dico_coordinate[self.number]
        towns_list = self.dico_coordinate[lon_lat]
        towns_string = "\n".join(towns_list)
        if latitude == '' or longitude == '':
            tkMessageBox.showerror(title="Erreur de saisie",message="Vous n'avez pas correctement remplit les coordonnées GPS")
            return
        else:
            response = tkMessageBox.askyesno(message="Êtes-vous sur de modifier les coordonnées ?")
            if response:
                
                #modification of the current coordinate for all the town with these coordinate
                towns_list = self.dico_coordinate[self.index_dico_coordinate[self.number]]
                for town in towns_list:
                    self.gedcom_town_list[town] = (latitude, longitude)
                with open(self.fichier_lieux, 'w') as f:
                    writer = csv.writer(f, delimiter=',', lineterminator='\n')
                    for key, (i, j) in self.gedcom_town_list.items():
                        row = [key, i, j]
                        writer.writerow(row)
                    
                picture_file = self.dico_pictures[self.number]
                #largeur, hauteur
                m = StaticMap(600, 300, url_template='http://a.tile.osm.org/{z}/{x}/{y}.png')
                #longitude = x, latitude=y , create marker (because its not work without) , 
                marker = CircleMarker((longitude, latitude),'#0036FF', 5)
                m.add_marker(marker)
                #set zoom : 13 = village area
                image = m.render(zoom=13)
                #save
                image.save(picture_file)
                # UPDATE ALL GUI
                self.current_lon['text'] = 'Longitude : '+str(longitude)
                self.current_lat['text'] = 'Latitude : '+str(latitude)
                iconImage=Tkinter.PhotoImage(file=picture_file)
                self.label1['image'] = iconImage
                self.label1.image = iconImage # keep a reference!
                self.entry_lat.delete(0, 'end')
                self.entry_lon.delete(0, 'end')
                self.control.update_idletasks()
                tkMessageBox.showinfo(title="Modification des coordonnées GPS",message="Les nouvelles coordonnées GPS pour le/les lieu(x) suivant(s) :"+towns_string+"\nsont :\n"+str(longitude)+", "+str(latitude))
            else:
                return

    def get_place(self,ged_file):
        """
        Read the file and retrieve all the place
        Store it in a set object and return it and these corresponding subdivisons
        
        input :
            ged_file (string) : Path to the GEDCOM File
            
        output :
            town_set (set) : list of unique Places
            town_org (list) : list of all the subdivison
        """
        #variable
        town_org = None
        town_set = set()
        #variable for if statement
        town_sub = None
        total = len(re.findall(r'(?<=2 PLAC )(.*)(?=\n)',''.join(open(self.fichier_gedcom,'r').readlines())))
        self.update_virtual_console(text=self.label_console['text'])
        self.update_virtual_console(text=str(len(town_set))+" Lieux trouvés",same=True, value=0)
        cpt = 0
        with open(self.fichier_gedcom, 'r') as ged:
            for line in ged:
                if line.startswith('2 PLAC '):
                    cpt+=1
                    self.update_virtual_console(text='Lieux : '+str(cpt)+'/'+str(total), same=True,value=cpt/total*100)
                    town_set.add(line.replace('2 PLAC ',''))
        #In case it's not heredis file
        if not town_org:
            town_org = ['Commune','Code Postal','Departement','Region','Pays','Subdivision','Ignorer']
        return town_set, town_org

    def verify_location(self, ad, n):
        """
        Check if the address have all the elements of the combination
        They are today 6 combinations given by these value :
            0 : The place as it is written in the file without comma
            1 : Subdivision - Postal Code - Town - State
            3 : Postal Code - Town -State
            4 : Town - Pays
            5 : 'Mairie' (String) - Town
            6 : Town
            
        input :
            ad (string) : the address
            n (integer) : value of the address combination
            
        output:
            Boolean (True/False) : True if the adress correspond of the criteria
        """
        # convert to unicode the different
        city = unicode(self.city.decode('iso8859_15')).lower()
        if city == '':
            city = None
        postcode = unicode(self.code.decode('iso8859_15')).lower()
        if postcode == '':
            postcode = None
        sub = unicode(self.sub.decode('iso8859_15')).lower()
        if sub == '':
            sub = None
        country = unicode(self.country.decode('iso8859_15')).lower()
        if country == '':
            country = None
        adresse = ad.lower()
        split_google_address = adresse.split(', ')
        
        if n == 1 or n ==2 or n == 0:
            if city and postcode and country:
                if sub:
                    #check if the street is the same but with the corresponding town
                    if sub in adresse and city in adresse:
                        return True
                #check if the corresponding town is the same with the associated postcode and country
                elif city in adresse and postcode in adresse and country in adresse:
                    return True
                #because google return english country name we make the same as above
                elif city in adresse or postcode in adresse:
                    return True
                else:
                    return False
        if n == 3:
            if city and country:
                if city in adresse and country in adresse:
                    return True
                else:
                    return False
        if n == 4 or n ==5:
            if city:
                if city in adresse:
                    return True
                else:
                    return False

    def get_gps_GoogleMapHTMLRequest(self, address):
        """
        Make a request in google map with the address combination and
        caught the latitude and longitude and the address with regex in the response
        
        input:
            address (string) : The address combination
            
        output:
            lat (float) : latitude of the Place
            lon (float) : longitude of the Place
            addresse (string) : the address given by GoogleMap for the given address combination
        """
        time.sleep(2)
        address = address.decode('iso8859_15')
        address = address.encode('utf8')
        address = urllib2.quote(address)
        #add these two line especially for EXE compilation
        #http://stackoverflow.com/questions/21201238/twilio-python-module-errors-after-compiling/21206079#21206079
        r = requests.get(u'http://maps.google.com/?q='+address+'&hl=fr')
        text = r.text
        try:
            lat, lon = eval(re.findall(ur'\[[-+]?\d+\.\d+,[-+]?\d+\.\d+\]',r.text)[0])
            # I remove the "u" for the regex to avoid unequal comparaison by difflib.SequenceMatcher
            addresse = re.findall(ur'\[\[".*?","(.*?)",\[',r.text)[0]
            return lat,lon, addresse
        except:
            return None, None, None
        
        
    def nominatim(self, address):
        """
        Nominatim geocoder (from geopy)
        return the latitude and longitude for a given place

        input :
            address (list) : the list of the different component of the adress
            
        output:
            lat (float) : latitude
            lon (float) : longitude
        """
        lat = None
        lon = None
        address.insert(0, " ".join(address))
        URL = 'http://nominatim.openstreetmap.org/search?'
        params = {'format':'json', 'q':''}
        for i in address:
            if i != '':
                self.update_virtual_console(text='Nominatim (OpenStreetMap) : '+i)
                params['q'] = i
                r = requests.get(URL, params=params)
                try:
                    lat = r.json()[0]['lat']
                    lon = r.json()[0]['lon']
                    return lat,lon
                except:
                    self.update_virtual_console(text='Echec geolocalisation', fg='red')
                    continue        
        
    def  geocoderGoogleV3(self, key, address):
        """
        for EXE only
        """
        url = 'https://maps.googleapis.com/maps/api/geocode/json'
        params = {'address': address, 'key':key}
        r = requests.get(url, params=params)
        if r.json()['status'] == u'ZERO_RESULTS':
            self.update_virtual_console(text='ZERO_RESULTS: aucun résultat')
            return None, None, None
        if r.json()['status'] == u'OVER_QUERY_LIMIT':
            self.update_virtual_console(text='OVER_QUERY_LIMIT: Vous avez depasse la limite des 2500 requetes')
            #query limit reached, take one of our API
            for api in GOOGLE_API:
                self.update_virtual_console(text='Checking Google API : '+api)
                params = {'address': address, 'key':api}
                r = requests.get(url, params=params)
                #because this software are distributed to everyone,
                #the probability that the query limit of the other API have been reached is high
                if r.json()['status'] == u'OVER_QUERY_LIMIT':
                    self.update_virtual_console(text='limit Reached')
                    continue
                else:
                    self.GoogleAPI = api
                    if r.json()['status'] == u'OK':
                       results = r.json()['results']
                       location = results[0]['geometry']['location']
                       ad = results[0]['formatted_address']
                       lat = location['lat']
                       lon = location['lng']
                       return lat, lon, ad
            self.GoogleAPI = False
            return None, None, None
        
        if r.json()['status'] ==u'REQUEST_DENIED':
            self.update_virtual_console(text='REQUEST_DENIED: la requete a ete refusee')
            return None, None, None
        if r.json()['status'] == u'INVALID_REQUEST':
            self.update_virtual_console(text='INVALID_REQUEST : Il manque un element de la requete (address, components ou latlng) ou un parametre result_type ou location_type invalide a ete fourni.')
            return None, None, None
        if r.json()['status'] == u'UNKNOWN_ERROR':
            self.update_virtual_console(text="UNKNOWN_ERROR: la requete n'a pas pu etre traitee en raison d'une erreur de serveur")
            return None, None, None
        if r.json()['status'] == u'OK':
           results = r.json()['results']
           location = results[0]['geometry']['location']
           ad = results[0]['formatted_address']
           lat = location['lat']
           lon = location['lng']
           return lat, lon, ad
    
    def get_gps_town(self, towns):
        """
        Open a CSV tabulated file with Places, Latitudes, Longitudes
        or create the file and looking for the coordinates for all the places:
            - Get the latitude, longitude and address by the get_gps_GoogleMapHTMLRequest function
              and control them with the verify_location function.
            - If its not possible we use the Nominatim geocoder by the nominatim function
        All the town are writing in the csv file nammed by the User
        By a progress bar, we show all the elements
        
        input :
            towns (set) : set of town
        output :
            output.name (string) : path to the created or opened csv file
        """
        try:
            output = tkFileDialog.asksaveasfile(title="Sauvegarder le fichier de lieux", mode='w', defaultextension=".csv")
        except IOError:
            tkMessageBox.showerror(title="Document déjà ouvert", message="Le document "+os.path.split(output.name)[1]+" est ouvert\nVeuillez le fermer et recommencer")
        if not output:
            return
        a= time.time()
        town_set = set()
        self.dico_gps = dict()
        self.dico_gps_adre = dict()
        fail = 0
        cpt = 0
        if self.GoogleAPI:
            #checking GoogleMap API
            self.progress_bar()
            self.update_virtual_console(text='Geolocalisation en utilisant le servive Google Map API v3')
        else:
            self.progress_bar()
        for town in towns:
            cpt+=1
            #Set variable to lat and lon
            town_string = town.replace('\n','')
            self.update_virtual_console(text=str(cpt)+"/"+str(len(towns))+' : '+town_string,
                                        label_title=str(cpt)+"/"+str(len(towns))+' : '+town_string,
                                        label_prog=round(cpt/len(towns)*100,2),
                                        value=int(cpt/len(towns)*100))
            
            town_list = town_string.split(',')
            if town_string not in town_set:
                town_set.add(town_string)
                self.sub = ''
                self.city = ''
                self.code = ''
                self.country = ''
                if 'Commune' in self.dico_index_subdivisions:
                    self.city = town_list[self.dico_index_subdivisions['Commune']]
                if 'Code Postal' in self.dico_index_subdivisions:
                    self.code = town_list[self.dico_index_subdivisions['Code Postal']]
                if 'Subdivision' in self.dico_index_subdivisions:
                    self.sub = town_list[self.dico_index_subdivisions['Subdivision']]
                if 'Pays' in self.dico_index_subdivisions:
                    self.country = town_list[self.dico_index_subdivisions['Pays']]
                adresse0 = town_string.replace(',',' ')
                adresse1 = self.sub+' '+self.code+' '+self.city+' '+self.country
                adresse2 = self.code+' '+self.city+' '+self.country #google map query
                adresse3 = self.city+' '+self.country
                adresse4 = 'Mairie '+self.city
                adresse5 = self.city
                verif = False
                for adre, n in (adresse0,0),(adresse1, 1), (adresse2,2), (adresse3,3), (adresse4,4), (adresse5,5) :
                    if adre not in town_set or adre == town_string:
                        #get gps coordinate from Google Map
                        lat, lon = None, None
                        self.update_virtual_console(text='Combinaison #-'+str(n+1)+' : '+adre)
                        if self.GoogleAPI:
                            result = self.geocoderGoogleV3(self.GoogleAPI, adre.decode('iso8859_15').encode('utf8'))
                            lat, lon, ad = result
                        if not self.GoogleAPI:
                            result = self.get_gps_GoogleMapHTMLRequest(adre)
                            lat, lon, ad = result
                        if lat:
                            self.update_virtual_console(text='Résultat :\n\t- '.decode('iso8859_15')+str(lat)+', '+str(lon)+'\n\t- '+ad)
                        
                        if lat != None:
                            #verification
                            self.update_virtual_console(text='Controle de la geolocalisation')
                            ratio = SequenceMatcher(None,ad.lower().replace(', ',' '),adre.lower()).ratio()
                            if ratio > 0.6:
                                verif = True
                                self.update_virtual_console(text='ratio : '+str(ratio), fg = 'green')
                            else:
                                self.update_virtual_console(text='ratio : '+str(ratio), fg = 'red')
                                self.update_virtual_console(text="Vérification des éléments de l'adresse retrouvé")
                                verif = self.verify_location(ad, n)
                            if verif:
                                self.update_virtual_console(text="==> OK",fg="green")
                                self.update_virtual_console(text='\t'+town_string+' : '+str(lat)+','+str(lon))
                                
                                self.dico_gps_adre[adre] = (lat,lon)
                                self.dico_gps[town_string] = result
                                town_set.add(adre)
                                break
                            else:
                                self.update_virtual_console(text='Echec controle', fg='red')
                                #the control fail, but gps coordinate have been found
                                if n ==4:
                                    self.dico_gps[town_string] = (lat,lon)
                        else:
                            self.update_virtual_console(text='Echec geolocalisation', fg='red')
                            if verif == False and n == 4:
                                self.update_virtual_console(text='### Echec lors de la recuperation des donnees GPS\n### Essai de recuperation avec Nominatim (OpenStreetMap) :')
                                #last chance to retrieve None result with nominatin
                                lat, lon = self.nominatim(town_list)
                                self.update_virtual_console(text="OpenStreetMap GPS : "+str(lat)+", "+str(lon))
                                
                                if lat:
                                    self.dico_gps[town_string] = (lat,lon)
                                else:
                                    self.update_virtual_console(text="### La commune n as pas ete retrouve", fg='red')
                                    self.dico_gps[town_string] = (lat,lon)
                                    fail += 1
                    else:
                        self.update_virtual_console(text='Lieux deja localise',fg='green')
                        lat, lon = self.dico_gps_adre[adre]
                        self.dico_gps[town_string] = self.dico_gps_adre[adre]
                        break
                
        writer = csv.writer(output, delimiter=',', lineterminator='\n')
        for i in self.dico_gps.keys():
            row = [i,self.dico_gps[i][0],self.dico_gps[i][1]]
            writer.writerow(row)
        b = time.time()
        seconds = b-a
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        self.pb_gui.destroy()
        tkMessageBox.showinfo(title="Terminer",message=str(len(towns)-fail)+" ont été analysé(s)\n"+str(fail)+" n'ont pas été retrouvé(s)\nRéalise en %d:%02d:%02d secondes" % (h, m, s))
        return output.name
    
    def town_custom(self, *args):
        """
        Retrieves the subdivision order chosen by the user
        in the TopLevel GUI window Subdivision
        """
        self.var_value = list()
        for i in self.var:
            self.var_value += [i.get()]
        self.text = ",".join(self.var_value)
        self.town_org_now['text'] = "Séléction choisis : "+self.text
        self.town_org_now.grid()
        self.Button_validate.config(state="active")
        self.Button_validate.focus_set()
        

    def town_validate(self, *args):
        """
        Validates the choice of the user in the subdivision order by displaying a tkMessageBox :
            - if yes, the order is saved
            - otherwise, the user returns to the subdivision window
        """
        self.town_custom()
        self.question = tkMessageBox.askquestion('Ordre des subdivisions des lieux', "Valider l'ordre ?\n"+self.town_org_now['text'])
        if self.question == 'yes':
            self.dico_index_subdivisions = dict()
            for i in range(len(self.var_value)):
                self.dico_index_subdivisions[self.var_value[i]]=i
            self.subdivision.destroy()
            self.main.grab_set()
            self.main.focus_set()
            self.step3.config(state="active")
            self.step3.focus_set()
        else:
            return            
    
    def choose_correct_subdivision(self, town_set, town_org):
        """
        Toplevel windows to the user choose the corect subdivision
        """ 
        self.subdivision = Tkinter.Toplevel()
        self.subdivision.grab_set()
        self.subdivision.focus_set()
        self.subdivision.title('Organisation des subdivisions')
        self.subdivision.config(bg="#a0522d")
        self.label_titre = Tkinter.Label(self.subdivision, text="Liste des 10 premiers lieux du GEDCOM", fg="#f5deb3", bg='#a0522d', relief='groove')
        self.label_titre.grid(row=0,columnspan = 10, sticky='EW')
        
        #create a frame/canvas/frame to see the first 10th city
        #====== FRAME CONSOLE ======
            #first frame
        nb_col = len(list(self.town_set)[0].replace('\n','').split(','))
        self.frameConsole = Tkinter.Frame(self.subdivision, bg="#f5deb3")
        self.frameConsole.grid(row=1, columnspan = nb_col)
        
            #first canvas
        self.canvasConsole = Tkinter.Canvas(self.frameConsole, height=130, width=680, bg="white")
        self.canvasConsole.grid()
            #second frame
        self.console = Tkinter.Frame(self.canvasConsole)
        self.console.config(relief='sunken', bg="white", height=130, width=680)
        self.console.grid()
        
            #scrollbar
        self.vsbc = Tkinter.Scrollbar(self.frameConsole,command=self.canvasConsole.yview)
        self.hsbc = Tkinter.Scrollbar(self.frameConsole, orient='horizontal', command=self.canvasConsole.xview)
            #configure scrollbar
        self.canvasConsole.configure(yscrollcommand=self.vsbc.set, xscrollcommand=self.hsbc.set)
        self.canvasConsole.create_window((0,0),window=self.console,anchor='nw')
            #positions
        self.vsbc.grid(row=0,column=3, sticky="NS")
        self.hsbc.grid(row=1,column=0, sticky="WE")     

        for i in range(10):
            text = list(self.town_set)[i].replace('\n','')
            text_split = text.split(',')
            
            for j in range(nb_col):
                stringLabel = Tkinter.Label(self.console,text=text_split[j],bg='white', fg='black').grid(row=i, column= j, sticky='W')
                #update the view of the console
                self.console.update_idletasks()
                # adapt and update the canvas content to the scroll bar
                self.canvasConsole.config(scrollregion=self.canvasConsole.bbox("all"))
                self.canvasConsole.yview_moveto(1.)
        #frame separator
        self.space = Tkinter.Frame(self.subdivision, height=25, bg="#a0522d")
        self.space.grid(row=2, columnspan = nb_col)
        self.label_field = Tkinter.Label(self.subdivision, text = "Ordre des lieux actuel : "+",".join(town_org), fg="#f5deb3", bg="#a0522d", relief="ridge").grid(row=3,columnspan =nb_col)

        #combobox loop
        self.var = list()
        for i in range(nb_col):
            self.label_field = Tkinter.Label(self.subdivision, text = "Champ "+str(i+1), fg="#f5deb3", bg="#a0522d", relief='groove')
            self.label_field.grid(row=4, column=i, sticky='WE',pady=10, padx=5)
            self.field = Tkinter.StringVar()
            self.var += [self.field]
            self.fields = ttk.Combobox(self.subdivision, textvariable = self.field, values = town_org, state = 'readonly', width=len(max(self.town_org, key=len)))
            self.fields.current(i)
            self.fields.grid(row=5, column=i)
        #dynamic label
        self.town_org_now = Tkinter.Label(self.subdivision, bg="#f5deb3", fg="#a0522d", relief="ridge", font=(None,'10','bold'))
        self.town_org_now.grid(row=6,columnspan = nb_col, pady=5)
        self.town_org_now.grid_remove()
        #button
        self.Button_save = Tkinter.Button(self.subdivision, text="Enregistrer vos choix", command=self.town_custom, bg="#f5deb3")
        self.Button_save.grid(row=7, column=0, columnspan=int(nb_col/2))
        self.Button_save.focus_set()
        self.Button_save.bind('<Return>', self.town_custom)
        self.Button_quit = Tkinter.Button(self.subdivision, text="Quitter", command=self.subdivision.destroy, bg="#f5deb3")
        self.Button_quit.grid(row=7, column=int(nb_col/2), columnspan=int(nb_col/2), rowspan=2, sticky = "NS")
        self.Button_validate = Tkinter.Button(self.subdivision, text="Valider", command=self.town_validate, bg="#f5deb3", activebackground="#f5deb3")
        self.Button_validate.grid(row=8, column=0, columnspan=int(nb_col/2))
        self.Button_validate.config(state="disabled")
        self.Button_validate.bind('<Return>', self.town_validate)
        self.subdivision.update()
        
    def get_data_gedcom(self):
        """
        By using the Gedcompy methods, extract the information from the GEDCOM file to create a list like an pedigree table:
        the retrieved data are :
            ID (String)
            Name and Surname (String)
            birth_date (String)
            birth_place (String)
            - list of spouse name and surname (List of String) :
                *!!!* in the case they are nothing the list is empty
            - list of spouse date of wedding (List of String) :
                *!!!* in the case they are nothing the list is empty
            - list of spouse wedding town (List of String) :
                *!!!* in the case they are nothing the list is empty
            death_date (String)
            death_place(String)
            ID_father (String)
            ID_mother (String)
            *!!!* In the case they are nothing we had an empty string ''
        the data are stored in the memory in the self.dico_data_list dictionnary
        with:
            key = ID, value = data_list
            data_list = [ID,name,birth_date,birth_place,[1],[2],[3],death_date,death_place,ID_father,ID_mother,[4]]
                [1] = [husband_wife1, ... , husband_wifeN]
                [2] = [wedding_place1, ... , wedding_placeN]
                [3] = [wedding_date1, ... , wedding_dateN]
                [4] = [husband_wife_id1, ... , husband_wife_idN]
        The second step is to get all the children of each familly for the descendance
        the data are stored in a dictionnary in the memory with:
            key : tuple of the husband and the wife ID:
                (husb_id,wife_id)
            value : childs (List) : List of the ID of all children
        create an object self.dico_descendant, self.dico_data_list , self.dico_ID
        """
        self.dico_data_list = dict()
        self.dico_ID = dict()
        cpt = 1
        total = len(list(self.parsed_gedcom.individuals))
        for ind in self.parsed_gedcom.individuals:
            self.update_virtual_console(text='Individu : '+str(cpt)+'/'+str(total), same=True,value=cpt/total*100)
            cpt+=1
            data_liste = list()
            ID = ind.id
            name = " ".join(ind.name)
            try:
                birth_date = ind.birth.date
                if not birth_date:
                    birth_date = ''
            except IndexError:
                birth_date = ''
            try:
                birth_place = ind.birth.place
            except IndexError:
                birth_place = ''
            try:
                death_date = ind.death.date
                if not death_date:
                    death_date = ''
            except IndexError:
                death_date = ''
            try:
                death_place = ind.death.place
            except IndexError:
                death_place = ''
            try:
                ID_father =  ind.father.id
            except AttributeError:
                ID_father = ''
            try:
                ID_mother = ind.mother.id
            except AttributeError:
                ID_mother = ''
            #4 ,5,6 wife, wedding, place
            data_list = [ID,name,birth_date,birth_place,[],[],[],death_date,death_place,ID_father,ID_mother,[]]
            self.dico_data_list[ID] = data_list
            self.dico_ID[ID] = name
            self.dico_ID[name] = ID

        self.dico_descendant = dict()
        cpt = 1
        total = len(list(self.parsed_gedcom.families))
        self.update_virtual_console(text=self.label_console['text'])
        for fam in self.parsed_gedcom.families:
            self.update_virtual_console(text='Famille : '+str(cpt)+'/'+str(total),same=True,value=cpt/total*100)
            cpt+=1
            husb_id = ''
            wife_id = ''
            date = ''
            place = ''
            childs = list()
            for e in fam.child_elements:
                if e.tag == 'MARR':
                    try:
                        date = e.date
                        if not date:
                            date = ''
                    except IndexError:
                        date = ''
                    try:
                        place = e.place
                    except IndexError:
                        place = ''
                if e.tag == 'HUSB':
                    husb_id = e.value
                if e.tag == 'WIFE':
                    wife_id = e.value
                if e.tag == 'CHIL':
                    childs.append(e.value)
            if wife_id and husb_id:
                liste_husb = self.dico_data_list[husb_id]
                liste_husb[4].append(self.dico_ID[wife_id])
                liste_husb[5].append(date)
                liste_husb[6].append(place)
                liste_husb[11].append(wife_id)
                self.dico_data_list[husb_id] = liste_husb
                
                liste_wife = self.dico_data_list[wife_id]
                liste_wife[4].append(self.dico_ID[husb_id])
                liste_wife[5].append(date)
                liste_wife[6].append(place)
                liste_wife[11].append(husb_id)
                self.dico_data_list[wife_id] = liste_wife
                
            self.dico_descendant[(husb_id,wife_id)]= childs
            self.dico_descendant[(wife_id,husb_id)]= childs

    def search_engine_gui(self):
        """
        Top Level GUI
        Search Engine to found an individu and make the ascendance or descendance
        """
        #Control of Gedcom File
        if not self.fichier_gedcom:
            tkMessageBox.showwarning(message="Vous n'avez pas charger de fichier GEDCOM")
            return
        #GUI
        self.search_engine = Tkinter.Toplevel()
        self.search_engine.grab_set()
        self.search_engine.focus_set()
        self.search_engine.config(bg="#f5deb3")
        
        self.label_name = Tkinter.Label(self.search_engine, text="Nom ou Prénom :", bg="#f5deb3")
        self.label_name.grid(column=0, row=0)
        self.var_name = Tkinter.StringVar()
        self.entry_name = Tkinter.Entry(self.search_engine, textvariable= self.var_name)
        self.entry_name.grid(column=1, row=0)
        self.entry_name.focus_set()
        self.entry_name.bind('<Return>', self.search_engine_function)
        
        self.button_search = Tkinter.Button(self.search_engine, text='Rechercher',command = self.search_engine_function, bg="#f5deb3")
        self.button_search.grid(column = 4 , row=0)
        #label listbox
        self.labelbox = Tkinter.Label(self.search_engine, text="Résultats :",  bg="#f5deb3")
        self.labelbox.grid(row=1, columnspan = 5)
        #frame listbox
        self.frame = Tkinter.Frame(self.search_engine, bd=2, relief='sunken')
        self.frame.grid(row=2,column=0,columnspan=6)
        #scrollbar listbox1
        self.scrollbar1 = Tkinter.Scrollbar(self.frame)
        self.scrollbar1.grid(row=0,column=1, sticky="NS")
        self.scrollbar2 = Tkinter.Scrollbar(self.frame, orient='horizontal')
        self.scrollbar2.grid(row=1,column=0, sticky="WE")
        
        #liste box
        self.listeBox = Tkinter.Listbox(self.frame, selectmode='SINGLE', exportselection=0, yscrollcommand=self.scrollbar1.set, xscrollcommand=self.scrollbar2.set, width = 100, height = 20)
        self.listeBox.grid(row=0,column = 0)
        self.scrollbar1.config(command=self.listeBox.yview)
        self.scrollbar2.config(command=self.listeBox.xview)

        #Button 
        #radio button type
        self.arbre = Tkinter.IntVar()
        for item in [1,2]:
            if item == 1:
                self.rb = Tkinter.Radiobutton(self.search_engine, text='Ascendance',value=item,variable=self.arbre, bg="#f5deb3")
                self.rb.grid(row=3, column=0)
            if item == 2:
                self.rb = Tkinter.Radiobutton(self.search_engine, text='Descendance',value=item,variable=self.arbre, bg="#f5deb3")
                self.rb.grid(row=3, column=1)
        #button
        self.button_validate = Tkinter.Button(self.search_engine, text="Validez",command=self.search_engine_validate, bg="#f5deb3")
        self.button_validate.grid(row=4, column=0)
        #button
        self.button_validate = Tkinter.Button(self.search_engine, text="Quitter",command=self.search_engine.destroy, bg="#f5deb3")
        self.button_validate.grid(row=4, column=1)

    def search_engine_validate(self):
        """
        This function is a part of the Search Engine TopLevel GUI
        Validate the choice of the person you choose in the GEDCOM file
        """
        self.ID = re.findall(ur'[@]\w+[@]',self.listeBox.get(self.listeBox.curselection()))[0]
        self.direction = self.arbre.get()
        if not self.ID or  self.direction == 0:
            if self.direction == 0:
                tkMessageBox.showerror(title = "Erreur !", message="Vous n'avez pas choisi la direction de l'arbre :\nAscendant / Descendant")
            if self.ID:
                tkMessageBox.showerror(title = "Erreur !", message="Vous n'avez pas choisi de personne !")
            return
        else:
            if self.ID:
                tkMessageBox.showinfo(title = "Personne", message="Personne choisis :\n"+self.dico_data_list[self.ID][1])
            self.search_engine.destroy()
            self.main.grab_set()
            self.main.focus_set()
            self.step5.config(state="active")
            self.step5.focus_set()

    def search_engine_function(self, *args):
        """
        This function is a part of the Search Engine TopLevel GUI
        Look for the person in the gedcom file
        """
        self.listeBox.delete(0, 'end')
        try:
            name1 = self.var_name.get().decode('iso8859_15')
        except:
            name1 = self.var_name.get()
        if not name1:
            tkMessageBox.showerror(title = "Erreur", message="Vous n'avez rien insrit")
        else:
            insert_list = set()
            name2 = name1.upper()
            name3 = name1.lower()
            for name in name1, name2, name3:
                for key in self.dico_ID.keys():
                    value = self.dico_ID[key].decode('iso8859_15')
                    if name in value.lower() or name in value.lower():
                        a = self.dico_data_list[key]
                        item = str()
                        for i in range(len(a)):
                            if i == 2:
                                item = item + " ° "+a[i]
                            elif i == 4:
                                if a[i] != [] :
                                    item = item + " x "+" x ".join(a[i])
                            elif i == 5:
                                if a[i] != [] :
                                    item = item + " x "+" x ".join(a[i])
                            elif i == 6:
                                if a[i] != [] :
                                    item = item + " ".join(a[i])
                            elif i == 7:
                                item = item + " + "+a[i]
                            elif i == 11:
                                continue
                            else:
                                item = item + " " + a[i]
                        insert_list.add(item)
            if len(insert_list) == 0:
                self.labelbox['text'] = 'Résultats : 0'
            else:
                self.labelbox['text'] = 'Résultats : '+str(len(insert_list))
            for item in insert_list:
                self.listeBox.insert('end', item)
                self.search_engine.update_idletasks()
        self.search_engine.update()
        
    def ascendance(self, ID, g=1, g_limit=10, liste = dict(), set_id = set()):
        """
        *!!!* RECURSIVE FUNCTION *!!!*
        Returns pedigree table with a recursive mode to go as far as possible in the pedigree
        
        input :
            - ID (String) : its a string with "@#@" with # is a sequence of number and letter
        default value :
            - sosa (integer) : set to 1 (de-cujus)
            - generation (integer) : set to 10
            - liste (dict) : dictionnary to store the data from dico_data_list (created by the get_data_gedcom)
            - set_id (set) : set to store the ID to avoid duplication
            
        output:
            liste (dictionnary) :
                key : ID (String) : Sosa stradonitz number of the individual in the ascendance
                value (List) : liste_data List of string and sub_list corresponding to these value :
                    [ID,name,birth_date,birth_place,[],[],[],death_date,death_place,ID_father,ID_mother]
                    (see the doc for get_data_gedcom for more detail)
        """
        if ID not in set_id:
            liste_data = self.dico_data_list[ID]
            liste_data.append(g)
            liste[ID]=liste_data
            id_father = liste_data[9]
            if id_father != '':
                gp = g+1
                liste, set_id = self.ascendance(id_father, g=gp, liste=liste, set_id=set_id)
            id_mother = liste_data[10]
            if id_mother != '':
                gm = g+1
                liste, set_id = self.ascendance(id_mother, g=gm, liste=liste, set_id=set_id)
            set_id.add(ID)
            return liste, set_id
        else:
            return liste, set_id

    def descendance(self, ID, g=1, g_limit=10, liste = dict(), set_id = set()):
        """
        *!!!* RECURSIVE FUNCTION *!!!*
        Returns pedigree table with a recursive mode to go as far as possible in the pedigree
        
        input :
            - ID (String) : its a string with "@#@" with # is a sequence of number and letter
        default value :
            - sosa (integer) : set to 1 (de-cujus)
            - generation (integer) : set to 10
            - liste (dict) : dictionnary to store the data from dico_data_list (created by the get_data_gedcom)
            - set_id (set) : set to store the ID to avoid duplication
            
        output:
            liste (dictionnary) :
                key : ID (String) : Sosa stradonitz number of the individual in the ascendance
                value (List) : liste_data List of string and sub_list corresponding to these value :
                    [ID,name,birth_date,birth_place,[],[],[],death_date,death_place,ID_father,ID_mother]
                    (see the doc for get_data_gedcom for more detail)
        """
        if ID not in set_id:
            set_id.add(ID)
            liste_data = self.dico_data_list[ID]
            liste_data.append(g)
            liste[ID]=liste_data
            spouses = liste_data[11]
            #they are wifes (the lenght of the list is different to 0)
            if spouses:
                for spouse_id in spouses:
                    childs_id_list = self.dico_descendant[(ID,spouse_id)]
                    #they are childs (the lenght of the list is different to 0)
                    if childs_id_list:
                        for child_id in childs_id_list:
                            g_child = g+1
                            liste, set_id = self.descendance(child_id, g=g_child, liste=liste, set_id=set_id)
                        return liste, set_id
                    #no childs
                    else:
                        return liste, set_id
            #Unmarried men or girl, or unknown spouse, but they can also have childs
            else:
                #no know wife
                if self.dico_descendant.get((ID,'')):
                    # il/elle a fondé une famille
                    childs_id_list = self.dico_descendant[(ID,'')]
                    #they are childs (the lenght of the list is different to 0)
                    if childs_id_list:
                        for child_id in childs_id_list:
                            g_child = g+1
                            liste, set_id = self.descendance(child_id, g=g_child, liste=liste, set_id=set_id)
                        return liste, set_id
                    #no childs
                    else:
                        return liste, set_id
                else:
                    # pas de famille
                    return liste, set_id
        else:
            #l'id et deja dans le set, return
            return liste, set_id
    
    def gedcom_step1(self, *args):
        """
        First step of the analysis with the GEDCOM pipeline :
            1- Open and parse the GEDCOM File with the Gedcompy method
                and store the data in memory into the self.parsed_gedcom object
            2- Extract the data with self.get_data_gedcom function
            3- Extract the Places with the self.get_place function
            4- Active the next step
        """
        self.fichier_gedcom = tkFileDialog.askopenfilename(title="Ouvrir le fichier GEDCOM:", initialdir=os.getcwd(), \
                                                               initialfile="", filetypes = [("Fichiers GEDCOM","*.ged"),("Tous", "*")])

        if "/" in self.fichier_gedcom:
            self.filename = self.fichier_gedcom.split('/')[-1]
        else:
            self.filename = self.fichier_gedcom.split('\\')[-1]
        if not self.fichier_gedcom:
            return
        else:
            a = time.time()
            #parsing gedcom
            self.progress_bar()
            self.update_virtual_console(text='Lecture du GEDCOM...',label_title="Lecture de "+self.filename+"...")
            
            a = time.time()
            self.parsed_gedcom = gedcom.parse(self.fichier_gedcom)
            b = time.time()
            
            self.update_virtual_console(text=str(b-a)+' secondes',value=int(1./3*100))
            self.update_virtual_console(text='Extraction des données...',label_title="Extraction des données...")
            
            self.get_data_gedcom()
            
            self.update_virtual_console(value=0,label_title="Extraction des lieux...")
            
            self.town_set, self.town_org = self.get_place(self.fichier_gedcom)
            
            self.update_virtual_console(value=100)
            
            
        b = time.time()
        seconds = b-a
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        tkMessageBox.showinfo("Terminé !", message="Traitement du GEDCOM terminé\nRéalisé en %d:%02d:%02d secondes" % (h, m, s))
        self.pb_gui.destroy()
        self.main.grab_set()
        self.main.focus_set()
        self.step2.config(state="active")
        self.step2.focus_set()

    def gedcom_step2(self, *args):
        """
        Second step of the analysis with the GEDCOM pipeline :
            1- Stores correct organization of subdivision and active the next step
        """
        #Toplevel window
        self.choose_correct_subdivision(self.town_set, self.town_org)

    def google_map_api_get(self, *args):
        """
        make the variable self.GoogleAPI
        """
        self.GoogleAPI = self.entry_api.get()
        if self.GoogleAPI:
            output = tkMessageBox.askyesno(title="Clé API Google Map", message="Clé API Google MAP:\n"+self.GoogleAPI)
            if output:
                self.api.destroy()
                self.gedcom_step3_bis()
            else:
                return
        else:
            tkMessageBox.showerror(title="Clé API Google Map", message="Erreur, champ vide, veuillez recommencer")
            return
            

    def google_map_api_destroy(self, *args):
        """
        """
        self.api.destroy()
        #self.gedcom_step3_bis()

    def google_map_api_toplevel(self):
        """
        Toplevel to get Google Map API
        """
        self.api = Tkinter.Toplevel()
        self.api.grab_set()
        self.api.focus_set()
        self.api.config(bg="#f5deb3")
        self.label_api = Tkinter.Label(self.api, text="Clé API : ", bg="#f5deb3", activebackground="#f5deb3")
        self.label_api.grid(row=0, column = 0)
        self.entry_api = Tkinter.Entry(self.api)
        self.entry_api.grid(row=0, column=1)
        self.bouton_annuler_api = Tkinter.Button(self.api, text="Annuler",command=self.google_map_api_destroy,bg="#f5deb3", activebackground="#f5deb3")
        self.bouton_annuler_api.grid(row=1,column=0)
        self.bouton_annuler_api.bind('<Return>',self.google_map_api_destroy)
        self.bouton_valider_api = Tkinter.Button(self.api, text="Valider", command=self.google_map_api_get,bg="#f5deb3", activebackground="#f5deb3")
        self.bouton_valider_api.grid(row=1,column=1)
        self.bouton_valider_api.focus_set()
        self.bouton_valider_api.bind('<Return>',self.google_map_api_get)
        self.center(self.api)
            
            
        
    def gedcom_step3(self, *args):
            """
            Third step of the analysis with the GEDCOM pipeline :
                1 : Ask if the CSV Places file exist:
                    -YES : Load the file in memory
                    - NO :
                        1 - Looking for GPS coordinate and create the CSV with self.get_gps_town
                        2 - Load the data in memory
                2 : Active the next step
            """
            file_exist = tkMessageBox.askyesno("Fichier de Lieux GPS", message="Le fichier de lieux du GEDCOM existe il déjà ?")
            if file_exist:
                self.fichier_lieux = tkFileDialog.askopenfilename(title="Ouvrir le fichier CSV des Lieux (GEDCOM) :", initialdir=os.getcwd(), \
                                initialfile="", filetypes = [("Fichiers CSV","*.csv"),("Tous", "*")])
                if self.fichier_lieux:
                    self.gedcom_town_list = import_town_gps_coord(self.fichier_lieux)
                    tkMessageBox.showinfo(title = "Terminé !", message="Lieux chargés")
                    yesno = tkMessageBox.askyesno(title="Controle visuel",message="Afin de pallier à d'éventuelle erreur de géolocalisation,\voulez-vous vérifier les lieux sur les cartes maintenant ?\n(vous pouvez néanmoins modifier les coordonnées dans le fichier)")
                    if yesno:
                        self.control_map_places(self.gedcom_town_list)
                        self.step4.config(state="active")
                        self.step4.focus_set()
                    else:
                        self.step4.config(state="active")
                        self.step4.focus_set()
                else:
                    return
            else:
                #check for GoogleMap API
                self.GoogleAPI = False
                output1 = tkMessageBox.askyesno(title="Clé API Google Map", message="Avez-vous une clef API Google Map ? (Une clef API Google Map permet d'utiliser leur service de géolocalisation avec 2500 requêtes maximum par jour)")
                if output1:
                    self.google_map_api_toplevel()
                else:
                    output2 = tkMessageBox.askyesno(title="Clé API Google Map", message="Voulez-vous créer une clé API Google Map ? (Un compte Gmail et nécessaire pour créer une clé API Google Map)")
                    if output2:
                        webbrowser.open('https://accounts.google.com/SignUp?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&ltmpl=default')
                        webbrowser.open('https://developers.google.com/maps/documentation/geocoding/get-api-key?hl=fr')
                        webbrowser.open('https://console.developers.google.com/?hl=FR')
                        self.google_map_api_toplevel()
                    else:
                        tkMessageBox.showinfo(title="Création du fichier CSV", message="Vous allez maintenant être redirigé pour créer votre fichier CSV")
                        self.gedcom_step3_bis()

    def gedcom_step3_bis(self):
        """
        Third step (bis) of the analysis with the GEDCOM pipeline :
            1 - Looking for GPS coordinate and create the CSV with self.get_gps_town
            2 - Load the data in memory
            3 : Active the next step
        """
        #take one of the API Key
        self.GoogleAPI = random.choice(GOOGLE_API)
        self.fichier_lieux = self.get_gps_town(self.town_set)
        if self.fichier_lieux:
            self.gedcom_town_list = import_town_gps_coord(self.fichier_lieux)
            tkMessageBox.showinfo(title = "Terminé !", message="Lieux chargés")
            yesno = tkMessageBox.askyesno(title="Controle visuel",message="Afin de pallier à d'éventuelle erreur de géolocalisation,\voulez-vous vérifier les lieux sur les cartes maintenant ?\n(vous pouvez néanmoins modifier les coordonnées dans le fichier)")
            if yesno:
                self.control_map_places(self.gedcom_town_list)
                self.step4.config(state="active")
                self.step4.focus_set()
            else:
                self.step4.config(state="active")
                self.step4.focus_set()
        else:
            return
                
    def gedcom_step4(self, *args):
        """
        Fourth step of the analysis with the GEDCOM pipeline :
            - 1 : Open the Search Engine TopLevel GUI
            - 2 : Active the next step
        """
        self.search_engine_gui()
        self.step5.config(state="active")
        self.step5.focus_set()

    def gedcom_step5(self, *args):
        """
        Fifth step of the analysis with the GEDCOM pipeline :
            - 1 : Show the Options in the Top Level GUI and store it into memory
            - 2 : Active the next step
        """
        self.options()
        self.step6.config(state="active")
        self.step6.focus_set()
        
    def gedcom_step6(self, *args):
        """
        Sixth step of the analysis with the GEDCOM pipeline :
            - 1 : Create a Top Level GUI to show the Options to regroup the Places
        """
        self.regroup = Tkinter.Toplevel()
        self.regroup.config(bg="#f5deb3")
        #radio button type
        self.varchoice = Tkinter.IntVar()
        label = Tkinter.Label(self.regroup, text= 'Regrouper les communes par :', bg="#f5deb3").grid()
        for item in range(len(self.town_org)):
            if self.town_org[item] == 'Code Postal':
                continue
            if self.town_org[item] == 'Subdivision':
                continue
            if self.town_org[item] == 'Ignorer':
                continue
            self.rb = Tkinter.Radiobutton(self.regroup, text=self.town_org[item],value=item,variable=self.varchoice, bg="#f5deb3")
            self.rb.grid()
        self.valider1 = Tkinter.Button(self.regroup, text= 'Valider',command=self.gedcom_map_validate, bg="#f5deb3")
        self.valider1.grid(sticky="EW")
        self.valider1.bind('<Return>', self.gedcom_map_validate)
        self.valider2 = Tkinter.Button(self.regroup, text= 'Passer',command=self.gedcom_map_pass, bg="#f5deb3")
        self.valider2.grid(sticky='EW')
        self.valider2.focus_set()
        self.valider2.bind('<Return>', self.gedcom_map_pass)
        
    def return_dico_shapefile(self):
        """
        Looking through the SHAPEFILE folder of all the SHAPEFILE
        determined by a '*adm*.shp' terminaison typically from the GADM website
        and return a dictionnary with the key are le administration boundary level and the value the path of the SHAPEFILE
        If there is no SHAPEFILE corresponding to the level, the upper level SHAPEFILE will be used for that level

        output:
            dico_shapefile :
                key (integer) : administration boudary level (generally 0 to 5)
                value (list) : list of SHAPEFILE path
        """
        from sys import platform
        if platform == "linux" or platform == "linux2":
            sep = "/"
        elif platform == "darwin":
            sep = "/"
        elif platform == "win32":
            sep = "\\"
            
        set_racine = set()
        filelist = list()
        
        for root, dirs, files in os.walk(os.getcwd()+sep+'SHAPEFILE'):
            for f in glob.glob(root+sep+'*adm*.shp'):
                filelist += [f]
                set_racine.add(os.path.splitext(os.path.basename(f))[0][:-1])
        list_racine = list(set_racine)
        dico_shapefile = dict()
        
        for level in range(6):
            dico_shapefile[level] = []
            for racine in list_racine:
                #contruire le "fichier"
                shapefile = os.getcwd()+sep+'SHAPEFILE'+sep+racine+'_shp'+sep+racine+str(level)+'.shp'
                if shapefile in filelist:
                    dico_shapefile[level] += [shapefile]
                else:
                    control = None
                    cpt = 0
                    while control == None:
                        shapefile = os.getcwd()+sep+'SHAPEFILE'+sep+racine+'_shp'+sep+racine+str(level-cpt)+'.shp'
                        if level - cpt == 0:
                            dico_shapefile[level] += [shapefile]
                            control = True
                        elif shapefile in filelist:
                            dico_shapefile[level] += [shapefile]
                            control = True
                        else:
                            cpt+=1
        return dico_shapefile

    def point_inside_polygon(self,x,y,poly):
        """
        Return True if a coordinate (x, y) is inside a polygon defined by
        a list of verticies [(x1, y1), (x2, x2), ... , (xN, yN)].
        Reference: http://www.ariel.com.au/a/python-point-int-poly.html
        Principle
        http://alienryderflex.com/polygon/

        input :
            x (float) : latitude
            y (float) : longitude
            poly (list) : list of tuple with latitude (float) and longitude (float) coordinate

        output:
            inside (Boolean) :
                - if the point are inside the given polygon :True
                - if the point are not inside the polygon : False (default value)
        """
        n = len(poly)
        inside =False
        p1x,p1y = poly[0]
        for i in range(n+1):
            p2x,p2y = poly[i % n]
            if y > min(p1y,p2y):
                if y <= max(p1y,p2y):
                    if x <= max(p1x,p2x):
                        if p1y != p2y:
                            xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x,p1y = p2x,p2y
        return inside
    
    def found_polygon_list(self,x,y, geometry):
        """
        *!!!* RECURSIVE FUNCTION *!!!*
        In some situations, the geometry object of a shape file can be composed of sublists of coordinates
        to distinguish different independent elements belonging to a single set:
            Example: the coastal islands and the mainland.
        We must therefore analyze each of these elements to determine if the curent point (x,y) is contained in one of them.
        The function analyzes in the list if the first element is a tuple of coordinates (float) otherwise the
        function will go to a higher depth level.

        input :
            x (float) : x coordinate of the point
            y (float) : y coordinate of the point
            geometry (list) : list of tuple coordinate (or list of n-list depth of tuple coordinate)
        """
        if isinstance(geometry[0][0],float):
            inside = self.point_inside_polygon(x, y, geometry)
            if inside:
                return True
            else:
                return False
        else:
            for sub in geometry:
                inside = self.found_polygon_list(x,y, sub)
                if inside:
                    return True
            return inside
        
    def get_gps_group(self, dico_town, criteria):
        """
        According to the criterion chosen, converted, this criterion to choose the good shapefile
        Retrieves the shapefile files in the shapefile folder corresponding to a specific write
        And organizes them according to their hierarchical level:

        Shapefile files from www.gadm.com are organized as follows:
            NNN_adm # .shp with NNN the three letters of the country and # the level of the shapefile.

        There are several levels:

            0: Country
            1: Regions
            2: Department
            3: Rounding
            4: Township
            5: Town

        (These level can have different name according to their country)
        The criterion is based on the value of the index of one of the subdivisions imposed for the grouping
        Which are currently:

            0: Town
            2: Department
            3: Regions
            4: Country

        The correspondence between the index of the subdivision and the level of the corresponding shapefile file
        And the following:

            0 => 'Town' => 5
            2 => 'Department' => 2
            3 => 'Region' => 1
            4 => 'Country' => 0

        Shapefile files are all searched based on whether they have the corresponding spelling for:
        NNN_adm # .shp and filed in a dictionary with the self.return_dico_shapefile () function
        Depending on the criterion chosen, the file is analyzed and checks for each entity if one of our locations
        And contained in this polygon via the function self.point_inside_polygon (lon, lat, polygon)
        If the locality is in the polygon, the mean of the latitude and longitude forming the square of the
        polygon (bbox) are computed and used as a coordinate for the locality.
        Otherwise, if there is no shapefile file present that can contain the locality in
        Function of the selected grouping criterion,
        No changes are made to the latitude and longitude and the remaining locations are
        Added to the newly created dictionary
        At the same time, a geojson file and created with all the forms found to be able to be
        Used with the chloropleth module of folium
        """
        dict_conv = {0:5,2:2,3:1,4:0}
        criteria = dict_conv[criteria]
        dico_shapefile = self.return_dico_shapefile()
        #variable
        buffer = []
        new_dico_town = dict()
        for f in dico_shapefile[criteria]:
            self.update_virtual_console(text="lecture du fichier : "+f)
            a = time.time()
            # read the shapefile
            reader = shapefile.Reader(f)
            fields = reader.fields[1:]
            shapes = reader.shapes()
            field_names = [field[0] for field in fields]
            cpt = 0
            cpt2 = 1
            size_dico_town = len(dico_town)
            set_coordinate = set()
            nb_rec = len(reader.shapeRecords())
            b = time.time()
            seconds = b-a
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            self.update_virtual_console(text='Terminé en %d:%02d:%02d secondes' % (h, m, s))
            for sr in reader.shapeRecords():
                if cpt == 0:
                    self.update_virtual_console(label_title='Fichier : '+os.path.split(f)[-1]+" "+str(nb_rec-cpt)+" Communes restantes",label_prog=0, value=0)
                    
                if  float(cpt)/nb_rec*100 >= cpt2:
                    cpt2 += 1
                    self.update_virtual_console(label_title='Fichier : '+os.path.split(f)[-1]+" "+str(nb_rec-cpt)+" Communes restantes",label_prog=cpt2, value=cpt2)
                    
                #to avoid the end of the loop if all town are found
                if len(dico_town) == 0:
                    self.update_virtual_console(label_title='Fichier : '+os.path.split(f)[-1]+" "+str(nb_rec-cpt)+" Communes restantes",label_prog=cpt2, value=100)
                    break
                #to show the advancement
                if size_dico_town != len(dico_town):
                    self.update_virtual_console(text="Lieux restants : "+str(len(dico_town)))
                    size_dico_town = len(dico_town)
                #car les localité ont tous des nom différents ont se basera sur les coordonnées
                lon1, lat1, lon2, lat2 = shapes[cpt].bbox
                #upgrade counter for index
                cpt +=1
                #store the coordinate of polygon
                lon_mean = np.mean([lon1,lon2])
                lat_mean = np.mean([lat1,lat2])
                #make the dict for geojson
                atr = dict(zip(field_names, sr.record))
                geom = sr.shape.__geo_interface__
                dico_feature = dict(type="Feature", geometry=geom, properties=atr)
                for key, (lat, lon) in dico_town.items():
                    #I can put the polygon shape with shapes[cpt].points but if I have Islands it's not work
                    #So I take the first element of the tuple of tuple
                    inside = self.found_polygon_list(lon,lat, dico_feature['geometry']['coordinates'])
                    if inside:
                        #associate the list of attribute with their data if its not already do
                        if (lon1, lat1, lon2, lat2) not in set_coordinate:
                            set_coordinate.add((lon1, lat1, lon2, lat2))
                            buffer.append(dico_feature)
                        self.update_virtual_console(text="Nouvelles coordonées pour : "+key+' '+str(lat_mean)+', '+str(lon_mean))
                        new_dico_town[key] = (lat_mean, lon_mean)
                        del dico_town[key]
        self.update_virtual_console(text='Lecture des fichiers shapefiles terminé')
        self.update_virtual_console(text="Il n'y as pas de fichier Shapefile correspondant pour :")
        for i in dico_town.keys():
            self.update_virtual_console(text=i)
        new_dico_town = dict(new_dico_town.items() + dico_town.items())
        # write the GeoJSON file
        self.update_virtual_console(text="Ecriture du fichier 'data_tmp.json'")
        from json import dumps
        with open('data_tmp.json', "w") as geojson:
            geojson.write(dumps({"type": "FeatureCollection","features": buffer}, indent=2, encoding ='iso8859_15') + "\n")
        return new_dico_town
    
    def get_gps_of_group(self,ascdt,criteria):
        """
        Loop through the pedigree, take all the Places.
        Split them and get the subdivision at the given criterion
        Iterate over them to get the GPS coordinate for each with the get_gps_group function
        return the modified ascdt and the dico_town from get_gps_group function
        input :
            ascdt (dictionary) :
                key : ID
                value : [ID,name,birth_date,birth_place,[],[],[],death_date,death_place,ID_father,ID_mother]
            criteria (integer) : Index of subdivision selected for grouping

        output :
            ascdt, dico_town (get_gps_group function)
        """
        self.update_virtual_console(text="Recherche et regroupement des villes", label_title='Recherche et regroupement des villes')
        #get the correct index of the value
        criteria_town_org = criteria
        criteria = self.dico_index_subdivisions[self.town_org[criteria]]
        town_set = set()
        ID_set = set()
        for key in ascdt:
            ID = ascdt[key][0]
            if ID not in ID_set:
                ID_set.add(ID)
                liste = ascdt[key]
                for index in [3,6,8]:
                    if index == 6:
                        liste2 = liste[index]
                        if liste2:
                            for idx in range(len(liste2)):
                                if liste2[idx] != '' :
                                    c = liste2[idx].split(',')[criteria]
                                    town_set.add(c)
                                    liste2[idx] = c
                            liste[index]= liste2
                        else:
                            continue
                    else:
                        if liste[index] != '':
                            c = liste[index].split(',')[criteria]
                            town_set.add(c)
                            liste[index] = c
                        else:
                            continue
        dico_grouped = dict()
        for key, (x,y) in self.gedcom_town_list.items():
            town = key.split(',')[criteria]
            if town in town_set:
                dico_grouped[town] = (x,y)
        #get the gps coordinate by the shapefile
        self.update_virtual_console(text="Recherche des coordonnées GPS via les Shapefile", label_title="Recherche des coordonnées GPS via les Shapefile")
        dico_town = self.get_gps_group(dico_grouped, criteria_town_org)
        return ascdt, dico_town
    
    def gedcom_map_pass(self, *args):
        """
        Bridge to pass the self.shapefile to False
        Make the pedigree table and set_id
        And pass to the gedcom_map() function to draw the map
        """
        self.regroup.destroy()
        #start the progress bar
        self.progress_bar()
        self.update_virtual_console(text="Création de l'ascendance",label_title="Création de l'ascendance")
        
        self.shapefile = False
        #1 for ascendance
        if self.direction == 1:
            #make ascdt type object
            self.ascdt, set_id = self.ascendance(self.ID)
            self.gedcom_map()
        if self.direction == 2:
            #make ascdt type object
            self.ascdt, set_id = self.descendance(self.ID)
            self.gedcom_map()
                
    def gedcom_map_validate(self, *args):
        """
        Bridge to pass the self.shapefile to True and regroupe the Places
        Make the pedigree table and set_id with the modified GPS coordinate
        And pass to the gedcom_map() function to draw the map
        """
        self.regroup.destroy()
        
        #start the progress bar
        self.progress_bar()
        self.update_virtual_console(text="Création de l'ascendance", label_title="Création de l'ascendance")
        self.shapefile = True
        self.criteria = self.varchoice.get()
        #1 for ascendance
        if self.direction == 1:
            #make ascdt type object
            a = time.time()
            ascdt, set_id = self.ascendance(self.ID)
            #group
            self.ascdt , self.gedcom_town_list = self.get_gps_of_group(ascdt, self.criteria)
            b = time.time()
            seconds = b-a
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            self.update_virtual_console(text='Terminé en %d:%02d:%02d secondes' % (h, m, s))
            #go to the function
            self.gedcom_map()
        if self.direction == 2:
            #make ascdt type object
            a = time.time()
            ascdt, set_id = self.descendance(self.ID)
            #group
            self.ascdt , self.gedcom_town_list = self.get_gps_of_group(ascdt, self.criteria)
            b = time.time()
            seconds = b-a
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            self.update_virtual_console(text='Terminé en %d:%02d:%02d secondes' % (h, m, s))
            #go to the function
            self.gedcom_map()

    def create_annotation_text_gedcom(self, dico_file,dico_town,options):
        """
        extract information of interest to display in the annotate text box
        
        input :
            dico_file : the return of the import_ascendance() or import_descendance() function
            dico_town : the return of the import_town_gps_coord() function
            option : list of option, the keyword are :
                - Nombre de °,x,+' : to show the repartition of Birth (°) Wedding (x) and Death (+) for a town
                - Nombre total d'événement : sum of the precedent event (Birth, Wedding, Death)
                - Départ(s) :
                - Arrivée(s) :
                - Nom(s) : The familly name in the town
                - Dates extrèmes : The oldest and newest date in the town
            typ : integer equal to 1 or 2 :
                - 1 : ascendance
                - 2 : descendance
                
        output :
            dico_annotation (dictionnary) :
                key (string) : city name
                value (3th-element tuple) : text to add for the specified annotation, latitude and longitude
        """
        #Note : "texte en string"+string_du_fichier
        #dict to store the annotation
        dico_annotation = dict()
        #pre-traitment
        f_lol = list()
        dico_file2 = dict()
        for key, value in dico_file.iteritems():
            liste = list()
            for item in value:
                if isinstance(item,list):
                    liste.append("\x95 "+" \x95 ".join(item))
                else:
                    liste.append(item)
            f_lol+= [liste]
            #transfert des modif dans un nouveau dict
            dico_file2[key]=liste
        #ecrase la variable de l'ancien par le nouveau dict
        dico_file = dico_file2
        f_array = np.asarray(f_lol)
        f_transpose = np.transpose(f_array)

        #search the extreme date
        dico_date_extreme = dict()
        for i in range(len(f_transpose[0])):
            for j in 2,5,7:
                if "\x95" in f_transpose[j+1][i]:
                    continue
                else:
                    if f_transpose[j+1][i] not in dico_date_extreme.keys():
                        date = re.findall(r'[0-9]{4}',f_transpose[j][i])
                        if date:
                            dico_date_extreme[f_transpose[j+1][i]] = date
                    else:
                        date = re.findall(r'[0-9]{4}',f_transpose[j][i])
                        if date:
                            dico_date_extreme[f_transpose[j+1][i]] += date
        for key in dico_date_extreme.keys():
            if dico_date_extreme[key]:
                a,b = sorted(dico_date_extreme[key])[0], sorted(dico_date_extreme[key])[-1]
                dico_date_extreme[key] = a+' - '+b
            
        #count the number of event
        number_of_birth_by_town = collections.Counter(f_transpose[3])
        number_of_wedding_by_town = collections.Counter(f_transpose[6])
        number_of_death_by_town = collections.Counter(f_transpose[8])
        number_total = number_of_birth_by_town+number_of_wedding_by_town+number_of_death_by_town
        #get the departures and arrivals
        dico_departure = dict()
        dico_arrivals = dict()
        dico_familly_name = dict()
        popup_trajectory = dict()

        for sosa in dico_file.keys():
            if "\x95" in dico_file[sosa][4]:
                weddings = multiple_wedding_gedcom(dico_file[sosa])
                for wed in weddings:
                    n,d,t = wed
                    #for the name list
                    if n != '' and t != '':
                        if t not in dico_familly_name.keys():
                            name = set()
                            name.add(n)
                            dico_familly_name[t] = name
                        else:
                            name = dico_familly_name[t]
                            name.add(n)
                            dico_familly_name[t] = name
                    if t:
                        #add to the wedding and total event
                        wedding_counter = collections.Counter([t])
                        number_of_wedding_by_town += wedding_counter
                        number_total += wedding_counter
                    if d:
                        if t:
                            if t not in dico_date_extreme.keys():
                                dico_date_extreme[t] = d+' - '+d
                            elif not dico_date_extreme[t]:
                                dico_date_extreme[t] = d+' - '+d
                            else:
                                #verify extrem date
                                d_int = int(d)
                                a = int(dico_date_extreme[t][:4])
                                b = int(dico_date_extreme[t][7:])
                                hyphen_begin = dico_date_extreme[t][:7]
                                hyphen_end = dico_date_extreme[t][4:]
                                if d_int < a:
                                    dico_date_extreme[t] = d+hyphen_end
                                if d_int > b:
                                    dico_date_extreme[t] = hyphen_begin + d

            #get familly name
            #result = re.findall(ur"[A-ZÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.'-\(\)/]+$",unicode(dico_file[sosa][1].decode('iso8859-15')),re.UNICODE)
            self.update_virtual_console(text=dico_file[sosa][1])
            result = re.findall(ur"((?:(?: d'| de| des| la| DE| VAN| LE) )?[A-ZÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð,.'\-\(\)\?/]+\b)",unicode(dico_file[sosa][1].decode('iso8859-15')),re.UNICODE)
            
            if result:
                familly_name = result[0]
            else:
                familly_name = dico_file[sosa][1]
            #iterate over (3) birth, (6) wedding and (8) death town and store into a set
            for index in 3,6,8:
                if "\x95" in dico_file[sosa][index]:
                    continue
                if dico_file[sosa][index] not in dico_familly_name.keys():
                        
                    name = set()
                    name.add(familly_name)
                    dico_familly_name[dico_file[sosa][index]] = name
                else:
                    name = dico_familly_name[dico_file[sosa][index]]
                    name.add(familly_name)
                    dico_familly_name[dico_file[sosa][index]] = name
                    
                    
            #compute parents sosa
            cityB = dico_file[sosa][3] #ville de l'individue étudié (point d'arrivé)
            p = dico_file[sosa][9] #@id@ du père
            m = dico_file[sosa][10] #@id@ de la mère
            for prts in p,m:
                if dico_file.get(prts):
                    g = dico_file[prts][-1]
                    cityA = dico_file[prts][3]
                    if cityA != ''  and cityB != '':
                        if cityA != cityB:
                            if cityA not in dico_departure.keys():
                                a = "Depart :\nG"+str(g)+" "+dico_file[prts][1]+"\n"
                                dico_departure[cityA] = a
                            else:
                                a = "G"+str(g)+" "+dico_file[prts][1]+"\n"
                                dico_departure[cityA] = dico_departure[cityA] + a
                            if cityB not in dico_arrivals.keys():
                                a = "Arrive :\nG"+str(g)+" "+dico_file[prts][1]+"\n"
                                dico_arrivals[cityB] = a
                            else:
                                a = "G"+str(g)+" "+dico_file[prts][1]+"\n"
                                dico_arrivals[cityB] = dico_arrivals[cityB] + a
                            popup_traj = "G"+str(g)+" "+dico_file[prts][1]
                            #create a popup for the trajectory
                            if (cityA,cityB) in popup_trajectory.keys():
                                popup_trajectory[(cityA,cityB)] += " "+popup_traj
                            else:
                                popup_trajectory[(cityA,cityB)] = popup_traj
                    if cityA == '' and  cityB != '':
                        # get @id@ of the grand parents of 'i' (the parents 'ID' of 'i' must exist to this point)
                        liste_ID_before = list()
                        if dico_file[prts][9] != '':
                            liste_ID_before += [dico_file[prts][9]]
                        if dico_file[prts][10] != '':
                            liste_ID_before += [dico_file[prts][10]]
                        # if the liste_ID_before is empty, they are no grand parents, continue
                        # this control are in the case they are no parents in the generation g+1
                        if len(liste_ID_before) == 0:
                            continue
                        else:
                            #we have grand parents, go control their birth places
                            city = False
                            liste_ID_after = list()
                            while city == False:
                                #iterate through the liste_ID_before and get the parents-@id@ for each
                                for id_i in liste_ID_before:
                                    if dico_file[id_i][9] != '':
                                        #Store only if the father don't have any Place
                                        if dico_file[id_i][3] == '' and dico_file[dico_file[id_i][9]][3] == '':
                                            #store g_N-father ID
                                            liste_ID_after+=[dico_file[id_i][9]]
                                    if dico_file[id_i][10] != '':
                                        #Store only if the mother don't have any Place
                                        if dico_file[id_i][3] == '' and dico_file[dico_file[id_i][10]][3] == '':
                                            #store g_N-mother ID
                                            liste_ID_after+=[dico_file[id_i][10]]
                                #check point, for the first turn it's not blocked
                                if len(liste_ID_before) == 0:
                                    break
                                #analyse each Places for each founded ID
                                else:
                                    for prts_i in liste_ID_before:
                                        if prts_i != '':
                                            g=dico_file[prts_i][-1]
                                            cityA = dico_file[prts_i][3]
                                            if cityA != ''  :
                                                if cityA != cityB:
                                                    popup_traj = "G"+str(g)+" "+dico_file[prts_i][1]
                                                    #create a popup for the trajectory
                                                    if (cityA,cityB) in popup_trajectory.keys():
                                                        popup_trajectory[(cityA,cityB)] += " "+popup_traj
                                                    else:
                                                        popup_trajectory[(cityA,cityB)] = popup_traj
                                    #second check point, if they are no parents-@id@ in the generation g+1, break the loop
                                    if len(liste_ID_after) == 0:
                                        break
                                    else:
                                        #replace the liste_ID_before by the liste_ID_after and replace liste_ID_after by an empty list
                                        liste_ID_before = liste_ID_after
                                        liste_ID_after = []
        ##### END #####
                                        
        #transfert all town key (from multiple wedding (utf8) and ascdt / descdt (iso8859_15) file)
        for town in number_total.keys():
            if town != '' and "\x95" not in town:
                dico_annotation[town] = ''
        for town in dico_annotation.keys():
            text = str()
            ### CHECK THE OPTIONS ###
            if "Nombre de °,x,+" in options:
                b = number_of_birth_by_town[town]
                #descendance : don't divide by 2
                w = number_of_wedding_by_town[town]/2
                d = number_of_death_by_town[town]
                a = "Naissance(s) : "+str(b)+"\nMariage(s) : "+str(w)+"\nDeces : "+str(d)+"\n"
                text = codec(text,a)
                #text += a
            if "Nombre total d'événement" in options:
                a = "Nombre total d'evenement : "+str(number_total[town])+"\n"
                #text += a
                text = codec(text,a)
            
            if 'Départ(s)' in options:
                if town in dico_departure.keys():
                    #text += dico_departure[town]+"\n"
                    text = codec(text,dico_departure[town]+"\n")
            if 'Arrivée(s)' in options:
                if town in dico_arrivals.keys():
                    #text += dico_arrivals[town]+"\n"
                    text = codec(text, dico_arrivals[town]+"\n")
            if 'Nom(s)' in options:
                if town in dico_familly_name.keys():
                    n = ", ".join([i if isinstance(i, unicode) else unicode(i.decode('iso8859_15')) for i in dico_familly_name[town]])
                    for i in range(4,n.count(', '),3):
                        idx = find_nth_character(n, ', ', i)
                        if idx:
                            n = n[:find_nth_character(n, ', ', i)] + "\n" + n[2+find_nth_character(n, ', ', i):]
                    #n2 ="Noms :\n".encode('iso8859_15')+n
                    n2 = codec("Noms :\n", n)
                    text = codec(text, n2)
                    #text += n2
            if 'Dates extrêmes' in options:
                if town in dico_date_extreme.keys():
                    if dico_date_extreme[town]:
                        #date = '\nDate : '.encode('iso8859_15')+dico_date_extreme[town]
                        date = codec('\nDate : ',dico_date_extreme[town])
                        #text += date
                        text = codec(text, date)
            try:
                lat = dico_town[town][0]
                lon = dico_town[town][1]
                dico_annotation[town] = (text,lat,lon)
            except KeyError:
                lat = dico_town[town][0]
                lon = dico_town[town][1]
                dico_annotation[town] = (text,lat,lon)
        return dico_annotation, popup_trajectory
        
    def gedcom_map(self):
        """
        Wrapper function
        Create the trajectory list and the coordinate list
        Compute the x and y min and max
        Create the text for the town and trajectory
        And generate the OSM map
        """
        #compute the trajectory
        self.update_virtual_console(text="Calcul des trajectoires...", label_title="Calcul des coordonnée du cadre de la carte...")
        a = time.time()
        list_traj, list_coord = convert_to_trajectory_GEDCOM(self.ascdt,self.gedcom_town_list,self.dico_ID,self.update_virtual_console)
        b = time.time()
        seconds = b-a
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        self.update_virtual_console(text='Terminé en %d:%02d:%02d secondes' % (h, m, s))
       #find the min and max coordinate
        self.update_virtual_console(text="Calcul des coordonnée du cadre de la carte...", label_title="Calcul des coordonnée du cadre de la carte...")
        a = time.time()

        y_min, x_min, y_max, x_max, g_max = find_min_max_coordinate(list_coord)
        
        b = time.time()
        seconds = b-a
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        self.update_virtual_console(text='Terminé en %d:%02d:%02d secondes' % (h, m, s))
        #create annotation text
        self.update_virtual_console(text="Création des annotations de la carte...",label_title="Création des annotations de la carte...")
        a = time.time()
        
        dico_annotation, popup_trajectory = self.create_annotation_text_gedcom(self.ascdt,self.gedcom_town_list,self.choosen_options)
        
        b = time.time()
        seconds = b-a
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        self.update_virtual_console(text='Terminé en %d:%02d:%02d secondes' % (h, m, s))
        #generate the OpenStreetMap
        self.update_virtual_console(text="Création des cartes...",label_title="Création des cartes (patience, ceci peu prendre plusieurs minutes)")
        a = time.time()
        
        generate_map_gedcom(self.direction,y_min, x_min, y_max, x_max,g_max,list_traj,dico_annotation, popup_trajectory, self.filename, self.shapefile)
        
        b = time.time()
        seconds = b-a
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        self.update_virtual_console(text='Terminé en %d:%02d:%02d secondes' % (h, m, s))
        self.pb_gui.destroy()
        tkMessageBox.showinfo(title = "Terminé !", message='Terminé en %d:%02d:%02d secondes' % (h, m, s))

    def options(self):
        """
        Create Tkinter TopLevel() windows to show the option can be checked by the user
        Actual option are :
            - Nombre de °,x,+
            - Nombre total d'événement
            - Départ(s)
            - Arrivée(s)
            - Nom(s)
            - Dates extrêmes
        """
        self.liste_checkbox = list()
        #make the new window
        self.option = Tkinter.Toplevel()
        self.option.grab_set()
        self.option.focus_set()
        self.option.resizable(width=False, height=False)
        self.center(self.option)
        self.option.title("Options :")
        self.option.configure(bg="#f5deb3")
        self.option_list = ['Nombre de °,x,+',"Nombre total d'événement",'Départ(s)','Arrivée(s)','Nom(s)', 'Dates extrêmes']
        for text in self.option_list :
            var = Tkinter.IntVar()
            self.liste_checkbox += [var]
            c = Tkinter.Checkbutton(self.option, text=text, variable=var,bg="#f5deb3")
            c.grid()
        self.validate_button = Tkinter.Button(self.option,text="Valider",command=self.option_command,bg="#a0522d", fg="#f5deb3", font=('Sans','10','bold'))
        self.validate_button.grid()
        self.validate_button.focus_set()
        self.validate_button.bind('<Return>',self.option_command)
        

    def option_command(self,*args):
        """
        Saving the option choosen by the user in the List self.choosen_options
        """
        for i in range(len(self.option_list)):
            option = self.liste_checkbox[i].get()
            if option:
                self.choosen_options += [self.option_list[i]]
        self.option.destroy()

############
# AUTORUN #
############

icon='''R0lGODlhGwE4APcAAAAAAAAAMwAAZgAAmQAAzAAA/wArAAArMwArZgArmQArzAAr/wBVAABVMwBV
ZgBVmQBVzABV/wCAAACAMwCAZgCAmQCAzACA/wCqAACqMwCqZgCqmQCqzACq/wDVAADVMwDVZgDV
mQDVzADV/wD/AAD/MwD/ZgD/mQD/zAD//zMAADMAMzMAZjMAmTMAzDMA/zMrADMrMzMrZjMrmTMr
zDMr/zNVADNVMzNVZjNVmTNVzDNV/zOAADOAMzOAZjOAmTOAzDOA/zOqADOqMzOqZjOqmTOqzDOq
/zPVADPVMzPVZjPVmTPVzDPV/zP/ADP/MzP/ZjP/mTP/zDP//2YAAGYAM2YAZmYAmWYAzGYA/2Yr
AGYrM2YrZmYrmWYrzGYr/2ZVAGZVM2ZVZmZVmWZVzGZV/2aAAGaAM2aAZmaAmWaAzGaA/2aqAGaq
M2aqZmaqmWaqzGaq/2bVAGbVM2bVZmbVmWbVzGbV/2b/AGb/M2b/Zmb/mWb/zGb//5kAAJkAM5kA
ZpkAmZkAzJkA/5krAJkrM5krZpkrmZkrzJkr/5lVAJlVM5lVZplVmZlVzJlV/5mAAJmAM5mAZpmA
mZmAzJmA/5mqAJmqM5mqZpmqmZmqzJmq/5nVAJnVM5nVZpnVmZnVzJnV/5n/AJn/M5n/Zpn/mZn/
zJn//8wAAMwAM8wAZswAmcwAzMwA/8wrAMwrM8wrZswrmcwrzMwr/8xVAMxVM8xVZsxVmcxVzMxV
/8yAAMyAM8yAZsyAmcyAzMyA/8yqAMyqM8yqZsyqmcyqzMyq/8zVAMzVM8zVZszVmczVzMzV/8z/
AMz/M8z/Zsz/mcz/zMz///8AAP8AM/8AZv8Amf8AzP8A//8rAP8rM/8rZv8rmf8rzP8r//9VAP9V
M/9VZv9Vmf9VzP9V//+AAP+AM/+AZv+Amf+AzP+A//+qAP+qM/+qZv+qmf+qzP+q///VAP/VM//V
Zv/Vmf/VzP/V////AP//M///Zv//mf//zP///wAAAAAAAAAAAAAAACH5BAEAAPwALAAAAAAbATgA
AAj/AOe1mydsYLtk7AQmGyhs3rB2yNoNIzhwIruFw+Q9RPZQ2DCPHz9KGilMUklhmCSJOSMmTBg0
Z9CEueHSJRpJNjHdTCkJDZqUPjFlEiq0pKSUKJN6BDksWdNhT4dlgvo0mVOrV5Mpa+pUmVWvXMFq
pWqVq9OpmTJ91UpPmVe3V99qvZpW6ly3bolpdWtXGT1obb1Ccwt4sL7C+pQd/pt4cWHFyh4fHpZG
UiYxYuqiEeNzUiaVaCA3jqwYcWnGDuUdZJdxtUPXBRE6pLiwoUeNwy7mrp1MmNGRPFXaROMGk07i
mNxspikTx5mjPnveHDpdqFNhmTzStVw0O6aQIbM7/xUKdeqwT+e56h1b9uqwrW+51vWqt2+y+VbV
Uk0rV68yNJl4lhZaUkF1n133ZfIWXHv5FdlfkD0GYWIR+jUYYRD+xZ9amRCjzHxqfZhJYoYps8wy
Dxb214rQKATRQe00tJpsE8EYUWq7SaQRRBtBtRRVmIDEyzApzRSUcZhEotNRQP0k00/U7fSdSWh5
9N13RBooVSboSfVjb1qW5xR6Ckr1YXtVrWdgVu+dxVWBc2lF5ntTRZZMW+8lptUkkkxyk0rH3QRg
T2LQaRV6cjXllT7JAIahYSWS2Jak0FAoqWilpVjhaKNBg6Iy0UxImj44EqTQRRWZattqE+XY0DAc
Xf+0lFOsfSQMLyPlitOTbpwkFC/GAZcSkkQGG+RnlhHpG1RXZtldU1x+hx1K0lqZZVRYPSUXfGV5
lYx/bxZI4F5xuqWnotvSc9eAltXVZ098DqjtW2oR84ky9+IlqooRsqjppItqSqm/nfYrmWLLcOrV
QAm9qJFAET1c40IIVRyjQ6wR9FGMMTblkSQhBYtTTcUNxctJHwWr5FFLHeUySsAeNdWU2F3bbH6f
mCdML8eClAwm6HXLnnvZetsmVm4i7e22d36lj4JWqbt0U3iORS9aTkHF111YeQW1V88IxuLYcG01
V8GUWmjhPKSNreJjB4caqUKtzvYiRqpFtCreE73/GltsH/XWMZY7ByeTD8SxjAmui0sCbMuwimTU
tCIdaxxVH5kn7n0530dzlmdhF2JYbdJXNFb1nWWVXnWW3jRYYrqubld3vQeX7d9qZV6IDQ4Dyn0N
KsO2qJBthZ6H9JXoqKPPTNgopgO/7XY9b0MGm6mo5o3xbBtdnGNGTdUqDG4g+WalrsGGcUZxNym1
7I8m+caySSYFCbJlJjF7eW/ZOYueJ2kRylB8BqesGXAtozOaWQoIFrRgYhIPTIuAOKO6iYiFad5S
l14chUGntGhBDbrLvy5EDAUNBhoo1NZe8mGuEbYlUgYzGMESJhpTWYRiCanRq+ZxEVTJqDa0YU1E
/3zUt2GAjIjlE0lLjoS+pQQJO7k6CciEMYmkTOkz30HLULB2oLT8LC3W8kgmPJG1e3FtamvRxOqy
FhatRLBdBUrJZ8TwnTPFB4PlmQrXXidCrYmwW1/TiooUlbsVkcaLxCgRZJIRPca0rXppU1hioqFD
4xTkYQu5EfhWw6qH+a1VS9FYGCXiEfFBRRIsicmwfIOrpECFHbxYRCQYkStpGVFZIvEOU5SlH0zQ
5WdS6ZkeoyKWpqzHdE0J2oEMCDs2XoUYa2qTgbz1FbZB6y33Mia5hOcVdQ1mc7bDV+nwIifCRMZ2
1bugMlhYPArxy1Fpc5s8DSMQYbSBB2ZogyQgxv8O8y3LhjYU4sY4UhCCQkUjywKTKEPyMZbkhBFh
iFmuUoYJRhjrcUEaxuOGMglmZalml5sZeQQ4rWGySS5oEifwoGYXbMnJKqDw3VrkQo8uaZNbCpKa
0JrGRwrp7kFe81Ma6vSh8+glkSx6z/ImdSGlaoqFB4skpqQXDX3QsDEHEQYbeCAEG9zAJJdowxmE
wNV8BgljGKGIQ4YoyqyespRgCsl1GHqUmbgkEtMCVhheFsWjIDGjlSNLFrFzpQORFIyXM45+jjYW
9HROUdCyS13kNVktcgssfGlgVaaSSKat5S5sS9SdFpQJH/wgBwDK2TAuBJkMqXa1W4FGJl4IH8X/
aMVSLVQewabqthr65p5msEEMzsCD4hbXDD04rhmCVDHWgKlWHHnRUqZLRIIgJHBMkQQjZDKTlvTE
fro6w29YZsT6LctZ5vlZWWZWFbsEi0iWEaMaq+KUmKaHTFp8IICG0ic5AgdEUalLnDiErsD88S1s
E6Q19xK2t6ThBzj4wQ0yo6C3nFBtmdlvgC5T2c8gNapqi54y9tFaT/0FRSSyqq0kUdwbGPcGwo0B
TWDMVR48J387uk1uwJcyM5whJYEjJSlpNR7fYEIMOLEoTPBnxZHIpCdOXoQWtqASwhJWmE/Jjn68
qOXPtFLLXNGEiLZEHgkSZYuf2eu7/mQZNGw3/wwsbeBM+ygYvzTPLaFNsFYSHEi/3Em2P4BwDGKg
lue11sKEEgOfonOZzfgJQBB6p6g6xSIUncjSobiqYoaxV0yY4bhehcFel4UTSUSCB2zw6hQJgpSm
kNIhZ7CBDWDACLja5pU+uhVwdv2kn0wufi4LzhaoQAVRL26ARmTvmjLBEV8SCYwz+5KW0KJakcoM
S8GcxBgC0QUke4ZPI/kMGrL8raDpRWqE7CY3BZPgDspOkHPJRA5wEAM0EAMUZfNKIw7RiPcMQxNb
6tCAFDTZBzHyURaadIrakmloRMNEj/rLPEhiBrLGOAxikAjHwrCUHqQaDbUayUE/4hDfnCG4Mf8I
Q28wNnJhVMyjtyrShN3wsozmz4hXksSwVbCCTi9Fy9ZydhbPArIzP4vZu7sPFRX7QO4MSLGTOAQW
rnCFzCQIzcb8xFwIecY9LwgaXedm7V6H4Le8QcI4GEbYDKwMSgRCENyWxAk/ISqA3Se3C4cbwKrn
Kb47klRIFkaLZRwGTIQBfA4Jw2o8zQMbSAIhwsA4WpcS6xsMWhI6mghHNuajjl0rzWfwAc3tN63z
5WoRVNgCDGKA5KJvkbDguQpI0xOt84Zui2T+DH9HiubPXCEQU6+3s7YkJ0LGeesdvEtbzsi2Cnud
UXLJBA5wEAa8XOhejQhEIK7AhRsg1T8XulD/YpTaW+nBsDEohh71ILOPZCziO58Wdf5UgiOOY4Tx
N/hRJMDzEeKGAQZftTcZ8yoElTW6Fgm5skQ/8TIx0zLDRgWXZz8ZhRJToR1T8QnYcR/IMDPAFCDn
VSy1tEUCFCACBEfl4QhUZwXCNwmT0Ah1oXUwtUymExjzwDoFgi2RRTVjMU1nJDXydgM4gHzeognZ
dwUqSBrQ4B/qkhjstCCJMU+TkAa9cH5ugSKSYX7DIAZK0nisZxLtYHiYQEqFZxL9RFw2IAYlkVGq
ggk2gHK15ioU8RGxdDIMRSRDwhN7FRNSci0lwQjEpgIwQEcWdRQQxCz64XLtdSXU9jMpwSdB/wJB
kzADOdAIROEZ+IM/uqdFVCQGMiYUUncFh4AGc/E7CYI729Im4iYJbyAJaYAJlREvlsFNmdAIXdAI
kxAf/OEVbzB91Xd1+fIhk3ADX/WEYBdbCPcterc8yjAJVsACLJAGqwUhJPZwChNVGsN4MYAlpDRy
RDQenxYD4JFEwhBrqydervYqFcMLheAHhbAIj8ca9LNrPfESwWFEUoQTEAgAmGcci1AsQLIlGwg8
z2YZGLhF2mUFXMAFrTcDLjAAMxAG4GaQaQEcEKQ5ASRBv0d1hJYMQTMgS7MXyBNZAdInE/kTi0ZI
kkB1RjhumfADPjBUmeAGPkABDYADaXF2Of8wVOTiH+Z0Ti2kNlchSYoxCc7IAisgBpryKZRmfgIR
I8UVA5KQEDdSECT3ENclDGQVA/vnPQiFCWcQBrJWeAW1MTsSCYVACH8gah6BK4vQju2IZC8RE1PE
EyWxCIuwBVpAbGHgjiL3QIpFRHr0QGIwBgnJBWOAZNkhCV3ABdyXcmjQAgTQAgMgAwCibV0wAy0w
A10wBhPZLgEyBozwGVLxiVxQb8mgCZngCPtWix3yLdwyF+sBm9p2BV1Qm43Qb8B4BSygm+D4BjkA
YaflAw7QAz5gWsEJYTb5IW9wLwODL/QxDI1ACbcwCcQgZjIEGJRQlIOWF5kwBt45BtRZGNT/4y/7
YF1YOWv7BEqzcV24oRFmiIZz5ZVg0Hj0aQM8EAaXoGPgIwyFUAhTFgN2SQjsSAWFQKCEsAg2IZYD
VFF3SWwO6qB75VH+kzmSQJjch5AIyX0KeRncJwMpNwk5AJktEAMygJkEMAANKaIzMAZHwTOZ0AUt
0AJjMG7DMAkaGQNj0AhXIAgqCXygGCJ3NFPLOAZGWKRW0AK06YLDQKRXMGhpAZzT1wAzWZPT5wO/
SW+Z4QPEOW6DsRdS0QuOoH3a93va1wgeog8QgiLRsAxpYJQBcAPaVpRyKgNjkFvUY2lNiY1h+ENC
JBGCAxKXwIU7JgyXMJ+hJmNbcANgYJ/4/1mVrLEIfrAFW1AFaLkFg5ZykroFhLAFCJo4jYOXVKAC
KnCpg/aAWvB+hhgmYsAFCOmhJGp5XCADVtBtq9qk9XYZMSoDA9ACDckCHioDOCADIuqdadEIMdoC
LACVAZKCKmmEsioDjHkFWBAIHVUubQJNOmqEyZqs0MoCR2oF2pYDHhoaw/AGYmB5N1BaOHADB/AS
k+AG65qNaTABDuADDSAGgrSkLNAFKsmqshqtgcBvJrIMmRYKm7AMY+CMMSCnK7ACMbACMlCUXKAg
VmUioXCx86A3XQWVMxIbmccjCHFPNEF5PHADq9eFMWNEZmiOF8ELD0gFmzpoYYCA89Offv+wCEjG
E3kJgaM6s2h4Y2FQBamXUc1yZF1gBa7KGU6WaEe6qyuAA5jQC2NwrJLpqi8hM2gwBig6AGNgHDCK
rKz3os3amDTBGTfBCF2ABVYwVIqiZ8PAr8m6AhOWRVLRCGJwBTmQA1aajd6SCT7xHm/gAzJwA6Xz
GWnwIVrqAJZnO5kgpyrIep2xGYfwe4eQCZtgsBcbCmowpw57AwCyJQlrlApCsJi7DBIxD3rKMRTz
KjzGGvbEA6vXf1yYcgk1JKjilTawVwiBeg4qszfXMfxJCAWacsZRoDz7J3Yoj3m5BeMWUozQmIPG
kvx1EzU6Bi4QmQjQelSbrKwnFJ6RJWP/EJkEwAI40CcxenmzuJvNKGMURiY5Y6NGKAlmxBfEALcO
CyBxMiY1qrenhQOFYjXxlgMTtk3m5AaK267KEDaNIKcGUCiZ4Ch7oQmHsH1pULAHG7rJCgBi4Aad
BRiJQZS+mgkXS7qhkLExsrG8EBG8wTHR5REEQVwyJgxusKgxEIhA9iUeESNmOCS88KC0i0RZEgZ/
ILzEi3pbAAC0ixTekTIfMWxQaR2MAK0x0K5FV15w1J3iO6I3QaQxygJfVaPCYhliEKPjS2gvapSf
C7/cS3DvAYPnMQk8KgN6BBZEyr0s6R5t5JsQRhO8Ax/0cHZA+HykRQGWZ0LEMLkKuwIP/+xUJaIJ
Ybq2l3uxm+uwMfAGnUUh+HYiRPm0l9vJyyAQqItyYWgx4MMb0yUEZpBykmAGlke8GCctIJN5vuFV
HCcMqKcFDruna0UkfBkGqsd6fgiBNixyRtEzRBLMX6yYXOCwcFYgnyBHomO+2Nu9YoCZg5YZw3I/
wDEGOZCs6ToM5yuKOXOjongemGVGS2qE+FofNvq4okgfuZgoaTAD46pZxShv1LctdoK4DQCO+hYI
3HsAYtBgFQIYy0AJiMB9b1AMBhu6ByDCBLsMm+AgxBAKyqAJYFvBJLwaLMYD2ZgxVfkjgBOoNtCu
sWYDBrBXMyFy+TOBEnEJslYo6qh6Jv9hgKSELOfqEmeAejAQAKP2OMzyc4iIeipAuGKAtDJWzgM5
HR01EmkAo9FrGTEqAJ2mK9cmFNJRLzOQrJmxFdtnmloXSPdFDBrJO/x6v67THjqVDDaarCGCBn5S
F4E7uAKyFQJXrjjQz6s1DHAXvSD5Z/5CsG5nBTigCZJslDGgCZ18scXgcH+xD5qQsEe52J/8EZ8W
03ezjSjBUMKQXDIbazLbEp1q1VN0HWAQBjFQEn6gBandEdcRj4YHJZJAbDGcMvLjG4U4LUdmBZZ6
GV2AvldWSziXFryQkKqcEjQwAKxXLFh0FLzQPzyoCVegxfkRfHokYKRoNPxKmRjpzUf/o02F1i1t
7c/JQCgBggZpIMAx4CdtprRo8AY90M8Kkn0eKgke8hUnlKYXuwmbMMEykAYEm7AeatgFm3dusbnJ
CgcbjbrzOZ8w8HiZV3KOYz9tEFwGsAVhcNqrF1Ea1RIuQV4/0paEcKoz3dotbIc8QRPfwQilqQJo
qGuJaUvG8dwpyQVdcJQI2XO4p3uN+B1NjQldIAM9hyUzoNyZIS5bUjPyoRWasNWs9wnQxK/ZOCAz
xSFa0QiCwAKHhwl1vN6fpSZ1MhfMqIIhcomZwAhuMG/pij+bMShvoLj+7N8xgB7Q4FRqQ7CRHAqP
jAMGO8kHQOC5xSKJEbErUMEGW9nj/1hcXtWPOVaHKvuUKecHQxwDNnAGln4Gi6qol27pPmaWaFkI
kW6pOYyI5aMSN2AcjcCqXVAFU+bLWlAInGqXYQDrtL4FF+qhtsqSyuJf4WYsh1Ca+IodvGqaUkEM
lyMMynSB1YnRWnwemfDVk5AzKMU08JuuyXC0g4YJmPUVXhPWHGmjHhoiHFJCbvBgN8AFH1JCaeEh
mQDf8k0MXy0G+iBm0VgpkUG6JEwJgqCChh26N3CwSBhxgJGwAh3JyyAbgnfZ5mhkSeEyFQ67KSfi
fwAGwVXxPDCf9GmowcUDWiC8Ix4D/mniRBQyXzkUaGvjQvugKr/yVTCrXJCssTrlWf+iRROZEsCS
hVxN5AOwAuOmv+mBiGeRCXCgCU2e88vapJ8LQnJWQpNLaOns1rUzNRdoFePtb/cBLru4rulBTl4D
56cZCGTuNRiCFxKNuQzd301awZsbADGAb9YHhYitCRGtEILnVWR1BkoSEkOCSpdteRFlCx6/BaEm
a5Q+a4MPY5QuqakXA5paBdnYeQZVEhucEkeN7SugAqGK+TwnqqIKA4AIiIPmof76+AJEHthBc0A3
DMZ9eDnDkMIHg3hMF0NP9Gow3bfK1hoJMtzSJr/Tt8EHMtheKP5xYMCDL20NA+PSRT/Y1WqBHjEF
CvDtAIQG7006IpnFLR5SsJmrCTz/GgMALtmJrQz4dmEDowkKqwmGcZXfiJ/FZeltEAltcE8Wd6k5
K2WWCqBuJgYQ1RLeJQYAsYhRmDAxCN4wSGhLDF7DhDmEKCyTpDNoJEnCJKZKDINiwkiyeOZixoto
GIGUxEjMGTFXFkrKhCkTr0zDYk60iQmTwzEsYojZOWzGgJ/JhhlN9ukoUpuZND3VNIPFATEwJ125
EgPNzUyZknm12XTYoaxiMnW5siLM12HKkilzG/dtV2KZrvjs+qnrMKWZ3uTAcePtW2Kf3H6lgHCY
pkNWYmTSpyxyW2iS4YYKtWlZ5k2NY6TZpIaFT02YQ8G1rG9ZZGjERj+GRg/avGHy/zDx4BFDmDBM
Z3iYwc3Dhg2EMW6EwUSQkW8bMSQJ47XbIS/qkng9f3j95Mcwf7Q43/lQ/DBMIHWWX0RlBXiMvMrz
hp9pNyb4OhtxkaF12P6JmCZhjOm5YZDJ5BAuDDpqGBpaQECSo9zaDymknHoKFEpaaMEgUCQZ44ou
YsChKjSq8qqmwZTJpBEsWAjjk0NakAGHB+lRZh636DkRKUqs8GmnEgdL5g0ccAjDq7hQgyaTBhBK
hphAsoLMstj2kSyaYkzLbBlNnvwslJ442gSzZTSLDZrIziRGhqkmUWa1duZpRxg2mnMwTkkOugEh
ggRMKYxhJAGDzmGiuy467Bysbv+5MyJJaRGFjrtopIuEuagi+jBhRAsqYmCU0UgvsknAnRplJCYu
DgTKJolyymQSnQasSQwrqErmqxaIEoOpWms1kT9ilHmqCxZWwAGmNLgk0dVMlLFJrrcaucIKHJKZ
xArHlk0GmhyVwdGtZe3CK0fDgvxBhhviqgyadDPxYcllDwkkBjapLFOZaGhUBrMrMXMkEMfSCEW0
qUoLM7NopJQNLi5YCECMzZahbZ7bcsOkHWTe3A86iR6qqTyPrjOjuUUwoYmXRRapTpJIKH0ODOFs
CGMRMQjZSIxFPsVoEmHQQG4kYaigAgYx5ht5JPJgQjoMoKn4qAvHxFAVJ/li2gn/E6RORfCrBbV6
iy+bJPRaE1A00RLDz6DCiusSvdoVQrccueLAxaLVry0bazzyK6+uwotZuGo9Skgil3UrMtnoySSx
GOBqRBAr0DiT22WWsXezgjkj68DSelrhhjA3wwzhuNL0CQfThplntzZsgEESOJNpJxl29tvvopIz
4Zk65m7oZTfrGtqN5V1UPsMG4IRepJDvrPtdZowo2oq3i5RWIYyH3lMZUezII2TpziVx+oac+QtL
WWT2m2SGDM3a71YZoAacLaNqsukpYKPyKQ2xKUFL3mFAmR+2mHWiq1zhBl7pEAvMkqO32GgwNkkD
YB7ziaTIBRSZyMENpqWMepXp/xM4aEAMhtGaJ8lghAmDxuT2ZbnNUIJLONhEMUQTgBiUJjOhmBwH
3fKUzPSkYVmCUztu05yKCSNitXGIRD7FszD0jiLEGRkjSEaf3x2KF8AhDgxukLzvoEwYvXAII26G
BjS4gSIq+0ghqKCCqjxHUjpxo0O2sDQDhGESYsCPn6b2kKPR5yhjaAEBWiCAIknkVkUxilIoSLvz
UQhtGdLfMiiBhaygoVaa+IqPKKgMpSSjcfk5il2yIgm5xGWTb/lEBH2QQahBaFzkukGuuMWteiUO
IahphL/QcLgUYulyodAEIuLWJS+9xoamSdhlMLMJNYGoYLJLhjCA4xx2wE52Gf/DZtXu9BE3hiwM
YogEIygVneDZzg2BugEMYnASP7xEZdRh2UjIeB43Ag0MUgSV0WCyE6VtSgX6OYsVZPAc+tVkn+QR
xhgI4IIBZEgmmJiBC35SogSFMpEUgosmaDAsNACTMVnR39f0ZhSvGYUSdMNWAWXANrecslbM+oEP
fgCYIiUDgHLBoAzCQMtspeaDIXyLPoiBCH9lIpnLBN2VgukvYtlQNBwpzZWuhBpghWJfnLuBmOCE
DGHgJgYVQyI02+EQnElCDIwwGSMiEQbc9MyNb6VU8YhTvYtwkSGUgg4v0BopTLhhRGiIxE7SQ4Ut
YCR48kHoQICmggN8hDzDYMT/qcSAhpzwZ2PDmASGBJkf+UxiAESh7ITYlqCviI0YTzFbGogRipNC
aWxd6cpO9MKXpOSSs4lshBWuYBZOQmguX+lCF3IAmFtuSxlv8EFgbhQbDsrGliJk7iSe1AWjsnCZ
mKGEMLNyA4BdqSdT+aWYbmiaTQirYQWLnRC92hB5oA514zHoRLaJMutQ6jc2WOt1fEcRlw3ne9BZ
hHcKqzE3RkKvmDqDG5JjEd5sQVOEFZB7GvXgf/opfpjlQhe44CDy3EQYd8SPDMzmnEwAUpBFCstO
SNqX+o2NDGYbw9hUFC39MesTmjxKJydxCEo+Jik26ZCH7jiJZGjCJpOA1l1k/yAs/XDrLRCKYIiS
kTAbRUYZPmjXDTQhG31AwxeCCMQhJrFa8gLTEfBySQzGYBpKSIU0WLpSwVgosKbicB7skNNveCCG
i6VurMIwCnQklYlvisc912GrcM6waLb2N50deYijCFGILTg2eBozcEkS/LzyKBZoW6j0HB+8qcYG
RVWhOpWGxdCISahEw1Y4UAxYgKpWuUCQAxCf1UpEIKsBGraayCyGWoADTUxyusT2lt5sohQUwU0Q
0VrgYRrhNKwEN8NYaQGPZM0j8bE0Lsj9wZAw8bfKyAYTDuiBA25AWbjIphc8DrMj5E2JRhD1SY7p
0piKORpiWRVLljONJtT0GgGA/4WCNsMwgxC8+pzYIXGsUbuIR8SpX/fsJhI3CNnLXhYDdYpBwsII
cCH8wBHpMM9B1sm0ytCQEUrRZxFzXJr3YBCALdLPavupWiYYIYNTwboFXBBoDDonhjE4BgdbUZ8g
tZLzVXUymk1Jwwyu0AIWqEB/XrgCFv6FmkXCNhMUnMSz73LAr3gLDUXPNlaskG2fcES3d7FkXXBE
Iwz+4AcgerJs5kIBHyjuE78iRpGVkcsrPCkQh3/SMHEAsMsJrO3HjLNp4iys0ZwXYgM6A3DS6Tok
Dggi5XHQRPxUKDc2ZFCSuEFzmsMR8QXvOmFcxHd0I6AkUmo/1xljJM4A+odsc/8L/1SnQRw7oaNg
SoqwFYMYYpAf1nebF/iZaIl1wIL8WPKxXvHRV5IRlEyQQVj5mUSxG5MfTWwCFMwCYGxr0pVpW+E4
tNVbifAogxUw/ydoKKBAodZJbCUjDUMqCskIKptwg8AwDmJQl7+BixShNi64AubDgTGwIRbSBDKg
vwCAIX8Tr33BDE34kgMoOIeIE0zQE4e7JoeYiU8JA7TqvZ2IjiRKiYsQoztBq4yBmvryiBUUtAgj
j+t4q0WYJ07TiUgIiTbiNEDbmDuygi5IFRSEo+eZhJpAA6f5ifBbDDQIkY5Zipr4BIlQtgkRgxAB
hWIYmzQQA/3xqJYKIC6MieT/Gy3AqQlviYn/6Iq5YAGs6JsnQxEUyYgbwITAQ40mMZNMyMLY0IeE
MYr7UQM0yIHkGwM4mMDxWiZN+AExOKaCCa8w2QQzREOICZ5BCY/YEYaGux7+oIgtQIObObTnmAQf
NJQ4SaI/SQm1iohhiBOW2cFFGCeSEYaTeI4w4JknvBSkKY/Tcw/+8A8HBDo/PLWm8DrICjqzyARi
eK2neEOjkImNoSCkQBGoAIVNqJDSUAbz0wRm0QRF+jpnpKDC+Ba9eKmuebITmba2G7e/iYyu+Tub
Cosnq4xsCSodYo3KwJJ/00Tx+qXLCROCmURJZMiDS6IXvBj36r1PyYgwaIhO/+Mw33nBipMO8Yin
SSGr/dKvSYmUHozBkrAIMxoVlqmanYjC9ZMEoPsQ/ZCJpTitsMgEMZjJraALCnEKLuSPaALKXnmp
p6DGZQCFUFit0mDK88Ok9dOLm2gLZYMtZ8GkeHSLityKt8gHuGCuykASJHmLZwjLMjkcGnkYzdBA
MSlIHPI3FoIDcIyD8iuNuKRLuSSYZRBBPpqO8RiPKeoTceqF6MAERika6ymiSCEUvKqK7Hgn7DAZ
F2QZsoqIQhEnjLAUnZiID3PJvfALSUiDSTiV7+kYo9AErzjNiQA6juiKKLRGo5QfwFkk2ZzKHeKh
p0BKzRjDsQEmYLmgm6hJ/v/zkQfpmpsyLkVqlsGgkdkQwG4pt0DUllmql8kBuIHkQLdkyMvRhDiI
y7jkDDiYS+6Uy9OJJtiRh4ZLovBAQVkMgzNgwb4ESduJFEagnY10I3EKSb3CK0q5TJL0lPZ4jlrA
CDKKCUG7SNzxi0kIzVYpuvwAEGf8yUk4O1ijCvrxm9f0ukBbP4mIiQTZobEpv6piSmDyqLE5rb2g
IOSEraToir8JJSM5JRtrilLiID2MTn9UBrLUocqwsnwZSH/7pX35HM2QsxtSSBv6xhvCRCAyIocI
D75suYuYCJsZFNMjFJLJmHYgSZUJj/oqj8UklPbYjerovZOAjunAmVpYhFr/QIPdg6NMg6004MnU
FE3OgglnTAO/yFMNkwEVoCwjW5bTFJvUDI9kiLgAiZSJGAxvfIpNGMfdJENHpcbUXD/YwskA4ou4
4EJxWRZnLDvj0kMdcotyq5fLCBMhNUjQyZKB1LcfvS5XvZxlsKbZ8R28wog/qQqCUA6z8h1T+8T9
NFAnHQZbWIRdaAj9ErRdZJnrwBS+qjjFXEWUkIlMcIOXVFDYisJJKLqJ2go0CM08dYoxWBjjmMZL
1YS6ONdMMiiVkS+LmCwxIDLfZFQSZUotGZt7rQugjMpOOoy+QBHAaSln+QrkjFFUOowcHVUdmgdS
bRPsdMvqRCrygthTVVKJ/11SfcEM2qimscIY6XCIHFTMHZwULR0nxXSQ9zBQSTgZlHNMj4VFknGj
ZT004HkeH3yoaYXQrUhNm7gP/DAW/HsDCulZjhADdmzNn4SKveCVi5gEbkKJlXsQsSHHES0/3lzK
pUSRvOjQZVEKUGgLSzUMf32yqGwLw/i6wtjDE8kbGr1HZUjSik3VJQUdtXTYh11LHKJb07i8rRLF
h6NVGqwiPirZcaq92ZHBUcSI9NoNWqw4+rTVmDVZlbVInMHFGASK8nCDieiKBR0GYigfp8GBRsAd
19TW1WwYbIWJujhRn0wQjvmT9eswbhSbSG3UQSVHR23KcgTUZqEgpVUKmf94x3/FqYD9LbBAx1Ma
l7joMq9s2M9hS4YUL0mMPLVsy+fVWyI1uCa9s1lliuRguEGJCOl4QegoxnlAuS51vUmxPcMaBm76
z1rNjpPRxef4OAcRtEmQ0FYJWqaF3cBrlZbggjEYA0YQ157Lj3WDV7OS0q5I2p2NHzhUihd9i9vM
l2+04Nv8RmAJk3ttiviLyqpkIG9JtrnYpHHx2tk6v0Vi3nLTUdCBWOzcl8irW4d13iy5HBkWE9Sx
mPSKyIspU174M9uhlJnoSFsdBna4iHAap2S1T1fMHknonR10YrIqydfjk5v5sHmSUGn0upqoCzyC
tbiBNRk4gJ9ghDSgyDPWcM2uCFpIPM0IsaiOScevocZH3YTVWkrzc9Q9Pg2ycdRQyItQgtCwPZKs
HQwuTLb0k1FOOhFtMcvmSqGLBVIN/CV9o1i5jVjJ+9F9oY32gsVOjhBKWYSH7EgfBN/xeCtP8UHm
EdyTfUG+EjQ/wqtYpEj5lBTbaZX/zVP89cz98NycLI4DBoqukE8Js8JzhYqk3ZVQ0jWO6aS2IMdQ
SMrblGbz62NgsuBiMEp3vIk7fSmcmouvcYsTbpJNUkCbYt7IsbJe0sBW/TeMfedUfVXovRJ3XoaA
AAA7
'''

if __name__ == '__main__':
    app = Peregrination()
    app.run()
