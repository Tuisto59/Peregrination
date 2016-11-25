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

pour mettre enter à un bouton
bouton.bind("<key>",parent)
bouton.focus() #pré-selctionne
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

### NON NATIVE PACKAGE ###

import gedcom
from geopy.geocoders import Nominatim

### variable for testing ###

gedcom_parsed = None

######
# GUI #
######


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
        #self.main.geometry("176x145")
        #self.main.resizable(width=False, height=False)
        self.main.configure(bg="#a0522d")
        iconImage=Tkinter.PhotoImage(master=self.main, data=icon)
        self.label1 = Tkinter.Label(self.main,image=iconImage)
        self.label1.image = iconImage # keep a reference!
        #self.label1 = Tkinter.Label(self.main,text="Pérégrination v 1.0", font=(font, 12), bg="#f5deb3")
        self.label1.grid(sticky='EW', padx=10, pady=5)
        #self.label1.grid()
        self.bouton0 = Tkinter.Button(master=self.main,text="Charger le fichier GEDCOM",command=self.gedcom_step,bg="#f5deb3")
        self.bouton0.grid(sticky='EW')
        #self.bouton1 = Tkinter.Button(master=self.main,text="Selectionner une personne dans le GEDCOM",command=self.search_engine_gui,bg="#f5deb3")
        #self.bouton1.grid(sticky='EW')
        self.bouton2 = Tkinter.Button(master=self.main,text="Charger la liste d'ascendance", command=self.load_ascdt_txt,bg="#f5deb3")
        self.bouton2.grid(sticky='EW')
        self.bouton3 = Tkinter.Button(master=self.main,text="Charger la liste de descendance", command=self.load_descdt_txt,bg="#f5deb3")
        self.bouton3.grid(sticky='EW')
        self.bouton4 = Tkinter.Button(master=self.main,text="Charger le fichier de lieux", command=self.load_csv,bg="#f5deb3")
        self.bouton4.grid(sticky='NSEW')
        self.bouton5 = Tkinter.Button(master=self.main,text="Options d'affichage", command=self.options,bg="#f5deb3")
        self.bouton5.grid(sticky='NSEW')
        self.bouton6 = Tkinter.Button(master=self.main,text="Créé la carte", command=self.mapping,bg="#f5deb3")
        self.bouton6.grid(sticky='NSEW')
        self.bouton7 = Tkinter.Button(master=self.main,text="Quitter",command=self.main.destroy,bg="#f5deb3")
        self.bouton7.grid(sticky='NSEW')
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
        
    def run(self):
        """
        function to keep the GUI in live
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
        self.pb_gui = Tkinter.Toplevel()
        
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
        self.frameConsole.grid(row=9, columnspan=10,rowspan=10,sticky='W')
        
            #first canvas
        self.canvasConsole = Tkinter.Canvas(self.frameConsole, height=130, width=500, bg="black")
        self.canvasConsole.grid(row=0)
            #second frame
        self.console = Tkinter.Frame(self.canvasConsole)
        self.console.config(relief='sunken', bg="black", height=130, width=500)
        self.console.grid(row=0)
        
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

    def update_virtual_console(self, text,fg='white'):
        """ display the message in the progress bar console """
        #create the second label in the console
        label = Tkinter.Label(self.console,text=text,bg='black',fg=fg, justify='left')
        label.grid(row=self.row,sticky="W")
        # update the row increment
        self.row = self.row+1
        # adapt and update the canvas content to the scroll bar
        self.canvasConsole.config(scrollregion=self.canvasConsole.bbox("all"))
        self.canvasConsole.yview_moveto(1.)
        self.pb_gui.update() ##update the GUI
        

    def gedcom_step(self):
        """
        TopLevel Windows for gedcom step
        """
        self.gs = Tkinter.Toplevel()
        self.gs.grab_set()
        self.gs.focus_set()
        self.gs.title("GEDCOM Manager")
        self.gs.config(bg="#f5deb3")
        self.step1 = Tkinter.Button(self.gs, text="Etape 1:\nImport du fichier\nGEDCOM",command=self.gedcom_step1, bg="#f5deb3")
        self.step1.grid(row=0,column=0, sticky="NS")
        self.step2 = Tkinter.Button(self.gs, text="Etape 2:\nCorrespondance\ndes lieux",command=self.gedcom_step2, bg="#f5deb3")
        self.step2.grid(row=0,column=1, sticky="NS")
        self.step2.config(state='disabled')
        self.step3 = Tkinter.Button(self.gs, text="Etape 3:\nRecherche des\ncoordonées GPS",command=self.gedcom_step3, bg="#f5deb3")
        self.step3.grid(row=0,column=2, sticky="NS")
        self.step3.config(state='disabled')
        self.step4 = Tkinter.Button(self.gs, text="Etape 4:\nSélection de la\npersonne",command=self.gedcom_step4, bg="#f5deb3")
        self.step4.grid(row=0,column=3, sticky="NS")
        self.step4.config(state='disabled')
        self.step5= Tkinter.Button(self.gs, text="Etape 5:\nOptions\nd'affichage",command=self.gedcom_step5, bg="#f5deb3")
        self.step5.grid(row=0,column=4, sticky="NS")
        self.step5.config(state='disabled')
        self.step6= Tkinter.Button(self.gs, text="Etape 6:\nCréer la carte des\npérigrinations",command=self.gedcom_step6, bg="#f5deb3")
        self.step6.grid(row=0,column=5, sticky="NS")
        self.step6.config(state='disabled')
        self.step7= Tkinter.Button(self.gs, text="Quitter",command=self.gs.destroy, bg="#f5deb3")
        self.step7.grid(row=0,column=6, sticky="NS")
        
    def get_place(self,ged_file):
        """
        input : GEDCOM File
        Output : Set of town, org
        """
        #variable
        town_set = set()
        town_org = None
        #variable for if statement
        town_sub = None
        with open(self.fichier_gedcom, 'r') as ged:
            for line in ged:
                #if line.startswith('1 PLAC'):
                    #town_sub = 1
                #if line.startswith('2 FORM ') and town_sub == 1:
                    #town_org = line.replace('2 FORM ','').replace('\n','').replace(' ','').split(',')
                    #town_sub = None
                if line.startswith('2 PLAC '):
                    town_set.add(line.replace('2 PLAC ',''))
        #In case it's not heredis file
        if not town_org:
            town_org = ['Subdivision','Commune','Code Postal','Departement','Region','Pays','Ignorer']
        return town_set, town_org

    def verify_location(self, lat, lon, ad, town_list, n):
        """
        Check if the given coordinate match the correct town
        Note : Nominatim looking for the nearest address from the given GPS coordinate
        The verification can be false depending how the adress it's construct and the location
        of the returning adress by nominatim

        comparaison de string

        >>> from difflib import SequenceMatcher
        >>> SequenceMatcher(None,a,b)
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

    def get_gps_GoogleMapHTMLRequest(self, adress):
        adress = adress.decode('iso8859_15')
        adress = adress.encode('utf8')
        adress = urllib2.quote(adress)
        r = requests.get(u'http://maps.google.com/?q='+adress+'&hl=fr')
        text = r.text
        try:
            lat, lon = eval(re.findall(ur'\[[-+]?\d+\.\d+,[-+]?\d+\.\d+\]',r.text)[0])
            # I remove the "u" for the regex to avoid unequal comparaison by difflib.SequenceMatcher
            addresse = re.findall(ur'\[\[".*?","(.*?)",\[',r.text)[0]
            return lat,lon, addresse
        except:
            return None, None, None
        
        
    def nominatim(self, adress):
        geolocator = Nominatim()
        lat = None
        lon = None
        for i in adress:
            if i != '':
                #print("Essaie avec : "+i)
                result = geolocator.geocode(i.decode('iso8859_15'))
                if result:
                    lat, lon = (result.latitude, result.longitude)
                    return lat,lon
                else:
                    #continue to the next i-th iteration
                    continue
        return lat,lon
        
    
    def get_gps_town_2(self, towns):
        """
        Use google geocoder from geocoder libray to found the corresponding gps coordinate
        input (set) : set of town
        output (csv file) : file with the data
        """
        try:
            output = tkFileDialog.asksaveasfile(title="Sauvegarder le fichier de lieux", mode='w', defaultextension=".csv")
        except IOError:
            tkMessageBox.showerror(title="Document déjà ouvert", message="Le document gps-coordinate.csv et ouvert\nVeuillez le fermer et recommencé")
        a= time.time()
        town_set = set()
        dico_gps = dict()
        dico_gps_adre = dict()
        fail = 0
        cpt = 0
        self.progress_bar()
        for town in towns:
            cpt+=1
            #Set variable to lat and lon
            town_string = town.replace('\n','')
            self.label_town_pb['text'] = str(cpt)+"/"+str(len(towns))+' : '+town_string
            self.pb['value'] = int(cpt/len(towns)*100)
            self.pb.update_idletasks()
            self.label_pb['text'] = str(round(cpt/len(towns)*100,2))+" %"
            self.label_pb.update_idletasks()
            self.label_pb.update()
            self.update_virtual_console(str(cpt)+"/"+str(len(towns))+' : '+town_string)
            
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
                adresse2 = self.code+' '+self.city+' '+self.country
                adresse3 = self.city+' '+self.country
                adresse4 = 'Mairie '+self.city
                adresse5 = self.city
                for adre, n in (adresse0,0),(adresse1, 1), (adresse2,2), (adresse3,3), (adresse4,4), (adresse5,5) :
                    if adre not in town_set or adre == town_string:
                        #get gps coordinate from Google Map
                        lat, lon = None, None
                        self.update_virtual_console('Combinaison #-'+str(n+1)+' : '+adre)
                        result = self.get_gps_GoogleMapHTMLRequest(adre)
                        lat, lon, ad = result
                        if lat:
                            self.update_virtual_console('resultat :\n\t- '+str(lat)+', '+str(lon)+'\n\t- '+ad)
                        
                        if lat != None:
                            #verification
                            self.update_virtual_console('Controle de la geolocalisation')
                            ratio = SequenceMatcher(None,ad.lower().replace(', ',' '),adre.lower()).ratio()
                            if ratio > 0.6:
                                verif = True
                                self.update_virtual_console('ratio : '+str(ratio), fg = 'green')
                            else:
                                self.update_virtual_console('ratio : '+str(ratio), fg = 'red')
                                verif = self.verify_location(lat, lon, ad, town_list, n)
                            if verif:
                                self.update_virtual_console(str(cpt)+"/"+str(len(towns))+' - '+town_string+' : '+str(lat)+','+str(lon))
                                
                                dico_gps_adre[adre] = (lat,lon)
                                dico_gps[town_string] = result
                                town_set.add(adre)
                                break
                            else:
                                self.update_virtual_console('Echec controle', fg='red')
                                #the control fail, but gps coordinate have been found
                                if n ==4:
                                    dico_gps[town_string] = (lat,lon)
                        else:
                            self.update_virtual_console('Echec geolocalisation', fg='red')
                            if verif == False and n == 4:
                                self.update_virtual_console('### Echec lors de la recuperation des donnees GPS\n### Essai de recuperation avec Nominatim (OpenStreetMap) :')
                                #last chance to retrieve None result with nominatin
                                lat, lon = self.nominatim(town_list)
                                self.update_virtual_console("OpenStreetMap GPS : "+str(lat)+", "+str(lon))
                                
                                if lat:
                                    dico_gps[town_string] = (lat,lon)
                                else:
                                    self.update_virtual_console("### La commune n as pas ete retrouve", fg='red')
                                    dico_gps[town_string] = (lat,lon)
                                    fail += 1
                    else:
                        self.update_virtual_console('Lieux deja localise',fg='green')
                        lat, lon = dico_gps_adre[adre]
                        dico_gps[town_string] = dico_gps_adre[adre]
                        break
                
        writer = csv.writer(output, delimiter=',', lineterminator='\n')
        for i in dico_gps.keys():
            row = [i,dico_gps[i][0],dico_gps[i][1]]
            writer.writerow(row)
        b = time.time()
        seconds = b-a
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        self.pb_gui.destroy()
        tkMessageBox.showinfo(title="Terminé",message=str(len(towns)-fail)+" ont été analysé(s)\n"+str(fail)+" n'ont pas été retrouvé(s)\nRéalise en %d:%02d:%02d secondes" % (h, m, s))
        return output.name
    
    def town_custom(self):
        """
        Get the choosen order of subdivision
        """
        self.var_value = list()
        for i in self.var:
            self.var_value += [i.get()]
        self.text = ",".join(self.var_value)
        self.town_org_now['text'] = "Séléction choisis :"+self.text
        self.Button_validate.config(state="active")

    def town_validate(self):
        """
        fonction that get the modification in the organisation of the town in the toplevel window Subdivision
        """
        self.town_custom()
        self.question = tkMessageBox.askquestion('Ordre des subdivisions des lieux', "Valider l'ordre ?\n"+self.town_org_now['text'])
        if self.question == 'yes':
            self.dico_index_subdivisions = dict()
            for i in range(len(self.var_value)):
                self.dico_index_subdivisions[self.var_value[i]]=i
            self.subdivision.destroy()
            self.step3.config(state="active")
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
        self.subdivision.config(bg="#f5deb3")
        self.label_titre = Tkinter.Label(self.subdivision, text="Liste des 10 premiers lieux du GEDCOM", bg="#f5deb3")
        self.label_titre.grid(row=0,columnspan = 10)
        
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
        self.space = Tkinter.Frame(self.subdivision, height=25, bg="#f5deb3")
        self.space.grid(row=2, columnspan = nb_col)
        self.label_field = Tkinter.Label(self.subdivision, text = "Ordre des lieux actuel : "+",".join(town_org), bg="#f5deb3").grid(row=3,columnspan =nb_col)

        #combobox loop
        self.var = list()
        for i in range(nb_col):
            self.label_field = Tkinter.Label(self.subdivision, text = "Champ "+str(i+1), bg="#f5deb3")
            self.label_field.grid(row=4, column=i)
            self.field = Tkinter.StringVar()
            self.var += [self.field]
            self.fields = ttk.Combobox(self.subdivision, textvariable = self.field, values = town_org, state = 'readonly', width=len(max(self.town_org, key=len)))
            self.fields.current(i)
            self.fields.grid(row=5, column=i)
        #dynamic label
        self.town_org_now = Tkinter.Label(self.subdivision, bg="#f5deb3")
        self.town_org_now.grid(row=6,columnspan = nb_col)
        #button
        self.Button_validate = Tkinter.Button(self.subdivision, text="Enregistrer vos choix", command=self.town_custom, bg="#f5deb3")
        self.Button_validate.grid(row=7, column=0, columnspan=int(nb_col/2))
        self.Button_validate = Tkinter.Button(self.subdivision, text="Quitter", command=self.subdivision.destroy, bg="#f5deb3")
        self.Button_validate.grid(row=7, column=int(nb_col/2), columnspan=int(nb_col/2), rowspan=2, sticky = "NS")
        self.Button_validate = Tkinter.Button(self.subdivision, text="Valider", command=self.town_validate, bg="#f5deb3")
        self.Button_validate.grid(row=8, column=0, columnspan=int(nb_col/2))
        self.Button_validate.config(state="disabled")
        self.subdivision.update()
        
    def get_data_gedcom(self):
        """Gedt data from GEDCOM"""
        self.dico_data_list = dict()
        self.dico_ID = dict()
        for ind in self.parsed_gedcom.individuals:
            data_liste = list()
            ID = ind.id
            name = " ".join(ind.name)
            try:
                birth_date = ind.birth.date
            except IndexError:
                birth_date = ''
            try:
                birth_place = ind.birth.place
            except IndexError:
                birth_place = ''
            try:
                death_date = ind.death.date
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
            data_list = [ID,name,birth_date,birth_place,[],[],[],death_date,death_place,ID_father,ID_mother]
            self.dico_data_list[ID] = data_list
            self.dico_ID[ID] = name

        self.dico_descendant = dict()
        self.dico_husb_wife = dict()

        for fam in self.parsed_gedcom.families:
            husb_id = None
            wife_id = None
            date = ''
            place = ''
            childs = list()
            for e in fam.child_elements:
                if e.tag == 'MARR':
                    try:
                        date = e.date
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
                self.dico_data_list[husb_id] = liste_husb
                
                liste_wife = self.dico_data_list[wife_id]
                liste_wife[4].append(self.dico_ID[husb_id])
                liste_wife[5].append(date)
                liste_wife[6].append(place)
                self.dico_data_list[wife_id] = liste_wife
                
            self.dico_descendant[(husb_id,wife_id)]=childs

    def search_engine_gui(self):
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
        
        #self.label_surname = Tkinter.Label(self.search_engine, text="Prénoms :", bg="#f5deb3")
        #self.label_surname.grid(column=2, row=0)
        #self.var_surname = Tkinter.StringVar()
        #self.entry_surname = Tkinter.Entry(self.search_engine, textvariable= self.var_surname)
        #self.entry_surname.grid(column=3, row=0)
        self.button_search = Tkinter.Button(self.search_engine, text='Rechercher',command = self.search_engine_function, bg="#f5deb3")
        self.button_search.grid(column = 4 , row=0)
        #label listbox
        self.labelbox = Tkinter.Label(self.search_engine, text="resultats :",  bg="#f5deb3")
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
                self.rb = Tkinter.Radiobutton(self.search_engine, text='Descendance',value=item,variable=self.arbre, state='disabled', bg="#f5deb3")
                self.rb.grid(row=3, column=1)
        #button
        self.button_validate = Tkinter.Button(self.search_engine, text="Validez",command=self.search_engine_validate, bg="#f5deb3")
        self.button_validate.grid(row=4, column=0)
        #button
        self.button_validate = Tkinter.Button(self.search_engine, text="Quitter",command=self.search_engine.destroy, bg="#f5deb3")
        self.button_validate.grid(row=4, column=1)

    def search_engine_validate(self):
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
                tkMessageBox.showinfo(title = "Personne", message="Personne choisis:\n"+self.dico_data_list[self.ID][1])
            self.search_engine.destroy()
            self.step5.config(state="active")

    def search_engine_function(self):
        """function search"""
        self.listeBox.delete(0, 'end')
        name = self.var_name.get()
        if not name:
            tkMessageBox.showerror(title = "Erreur", message="Vous n'avez rien insrit")
        surname = None
        if name:
            if surname:
                for key in self.dico_ID.keys():
                    if name in self.dico_ID[key] and surname in self.dico_ID[key]:
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
                            else:
                                item = item + " " + a[i]
                        self.listeBox.insert('end', item)
            else:
                for key in self.dico_ID.keys():
                    if name in self.dico_ID[key]:
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
                            else:
                                item = item + " " + a[i]
                        self.listeBox.insert('end', item)
        else:
            for key in self.dico_ID.keys():
                if surname in self.dico_ID[key]:
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
                        else:
                            item = item + " " + a[i]
                    self.listeBox.insert('end', item)
        self.search_engine.update()
        
    def ascendance(self, ID, sosa=1, generation=10, liste = dict(), set_id = set()):
        """
        return the ascendance of the given ID
        """
        if ID not in set_id:
            liste_data = self.dico_data_list[ID]
            liste[sosa]=liste_data
            id_father = liste_data[-2]
            if id_father != '':
                liste, set_id = self.ascendance(id_father, sosa=sosa*2, liste=liste, set_id=set_id)
            id_mother = liste_data[-1]
            if id_mother != '':
                liste, set_id = self.ascendance(id_mother, sosa=sosa*2+1, liste=liste, set_id=set_id)
            set_id.add(ID)
            return liste, set_id
        else:
            return liste, set_id
    
    def gedcom_step1(self):
        """
        Open and parse Gedcom File
        """
        self.fichier_gedcom = tkFileDialog.askopenfilename(title="Ouvrir le fichier GEDCOM:", initialdir=os.getcwd(), \
                                                               initialfile="", filetypes = [("Fichiers GEDCOM","*.ged"),("Tous", "*")])
        if not self.fichier_gedcom:
            return
        else:
            a = time.time()
            #parsing gedcom
            self.progress_bar()
            self.pb['value'] = int(1./3*100)
            self.pb.update_idletasks()
            self.label_town_pb['text'] = "Lecture du GEDCOM..."
            self.label_town_pb.update_idletasks()
            self.label_town_pb.update()
            self.pb_gui.update()

            self.parsed_gedcom = gedcom.parse(self.fichier_gedcom)

            self.pb['value'] = int(2./3*100)
            self.label_town_pb['text'] = "Extraction des données..."
            self.label_town_pb.update_idletasks()
            self.label_town_pb.update()
            self.pb_gui.update()
            
            self.get_data_gedcom()
            #iteration

            self.pb['value'] = int(3./3*100)
            self.label_town_pb['text'] = "Extraction des lieux..."
            self.label_town_pb.update_idletasks()
            self.label_town_pb.update()
            self.pb_gui.update()
            
            self.town_set, self.town_org = self.get_place(self.fichier_gedcom)

            self.pb_gui.destroy()
        b = time.time()
        seconds = b-a
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        tkMessageBox.showinfo("Terminé !", message="Traitement du GEDCOM terminé\nRéalise en %d:%02d:%02d secondes" % (h, m, s))
        self.step2.config(state="active")

    def gedcom_step2(self):
            #Toplevel window
            self.choose_correct_subdivision(self.town_set, self.town_org)

    def gedcom_step3(self):
            """
            Next step after the top level town
            """
            file_exist = tkMessageBox.askyesno("Fichier de Lieux GPS", message="Le fichier de lieux du GEDCOM existe il déjà ?")
            if file_exist:
                fichier_lieux = tkFileDialog.askopenfilename(title="Ouvrir le fichier CSV des Lieux (GEDCOM) :", initialdir=os.getcwd(), \
                                initialfile="", filetypes = [("Fichiers CSV","*.csv"),("Tous", "*")])
                if fichier_lieux:
                    self.gedcom_town_list = import_town_gps_coord(fichier_lieux)
                    tkMessageBox.showinfo(title = "Terminé !", message="Lieux chargés")
                    self.step4.config(state="active")
                else:
                    return
            else:
                fichier_lieux = self.get_gps_town_2(self.town_set)
                if fichier_lieux:
                    self.gedcom_town_list = import_town_gps_coord(fichier_lieux)
                    tkMessageBox.showinfo(title = "Terminé !", message="Lieux chargés")
                    self.step4.config(state="active")
                else:
                    return
    def gedcom_step4(self):
        self.search_engine_gui()
        self.step5.config(state="active")

    def gedcom_step5(self):
        self.options()
        self.step6.config(state="active")
        
    def gedcom_step6(self):
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
            self.rb = Tkinter.Radiobutton(self.regroup, text=self.town_org[item],value=item,variable=self.varchoice, bg="#f5deb3")
            self.rb.grid()
        self.valider = Tkinter.Button(self.regroup, text= 'Valider',command=self.gedcom_map_validate, bg="#f5deb3").grid(sticky="EW")
        self.valider = Tkinter.Button(self.regroup, text= 'Passer',command=self.gedcom_map_pass, bg="#f5deb3").grid(sticky='EW')
        
    def get_gps_group(self, towns):
        """
        Use google geocoder from geocoder libray to found the corresponding gps coordinate
        input (set) : set of town
        output (csv file) : file with the data
        """
        a= time.time()
        town_set = set()
        dico_gps = dict()
        fail = 0
        cpt = 0
        lat, lon = None, None
        self.progress_bar()
        for town in towns:
            cpt+=1
            self.pb['value'] = int(cpt/len(towns)*100)
            self.pb.update_idletasks()
            self.label_pb['text'] = str(round(cpt/len(towns)*100,2))+" %"
            self.label_pb.update_idletasks()
            self.label_pb.update()       
            self.label_town_pb['text'] += "\nRecherche : "+town
            self.label_town_pb.update_idletasks()
            self.label_town_pb.update()
            self.pb_gui.update()

            result = self.get_gps_GoogleMapHTMLRequest(town)
            lat, lon = result

            if lat:

                self.label_town_pb['text'] = town+' : '+str(lat)+','+str(lon)
                self.label_town_pb.update_idletasks()
                self.label_town_pb.update()
                self.pb_gui.update()
                dico_gps[town] = result
                continue

            if lat == None:
                self.label_town_pb['text'] += "\n### Echec lors de la recuperation des donnees GPS\n### Essai de recuperation avec Nominatim (OpenStreetMap) :"
                self.label_town_pb.update_idletasks()
                self.label_town_pb.update()
                self.pb_gui.update()

                lat, lon = self.nominatim(town)
                self.label_town_pb['text'] += "\nOpenStreetMap GPS : "+str(lat)+", "+str(lon)
                self.label_town_pb.update_idletasks()
                self.label_town_pb.update()
                self.pb_gui.update()
                
                if lat:
                    dico_gps[town] = (lat,lon)
                else:
                    print(town)
                    self.label_town_pb['text'] += "\n### La subdivision n as pas ete retrouve"
                    self.label_town_pb.update_idletasks()
                    self.label_town_pb.update()
                    self.pb_gui.update()
                    fail += 1
                    dico_gps[town] = (lat,lon)

        b = time.time()
        seconds = b-a
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        #self.pb_gui.destroy()
        tkMessageBox.showinfo(title="Terminé",message=str(len(town_set)-fail)+" ont été retrouvé(s)\n"+str(fail)+" n'ont pas été retrouvé(s)\nRéalise en %d:%02d:%02d secondes" % (h, m, s))
        return dico_gps
    
    def get_gps_of_group(self,ascdt,criteria,dico_ID):
        """
        foobar
        [ID,name,birth_date,birth_place,[],[],[],death_date,death_place,ID_father,ID_mother]
        """
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
                                    c = liste2[idx].split(',')[criteria].replace(' ','')
                                    town_set.add(c)
                                    liste2[idx] = c
                            liste[index]= liste2
                        else:
                            continue
                        
                    else:
                        if liste[index] != '':
                            c = liste[index].split(',')[criteria].replace(' ','')
                            town_set.add(c)
                            liste[index] = c
                        else:
                            continue
        dico_town = self.get_gps_group(town_set)
        return ascdt, dico_town
    def gedcom_map_pass(self):
        self.regroup.destroy()
        if self.direction == 1:
            #make ascdt type object
            self.ascdt, set_id = self.ascendance(self.ID)
            self.gedcom_map()
                
    def gedcom_map_validate(self):
        self.regroup.destroy()
        self.criteria = self.varchoice.get()
        if self.direction == 1:
            #make ascdt type object
            ascdt, set_id = self.ascendance(self.ID)
            self.ascdt , self.gedcom_town_list = self.get_gps_of_group(ascdt, self.criteria, self.dico_ID)
            self.gedcom_map()
        
    def gedcom_map(self):
            #compute the trajectory
            list_traj, list_coord = convert_to_trajectory_ascdt_GEDCOM(self.ascdt,self.gedcom_town_list,self.dico_ID)
           #find the min and max coordinate 
            y_min, x_min, y_max, x_max, g_max = find_min_max_coordinate(list_coord)
            #create annotation text
            dico_annotation = create_annotation_text_gedcom(self.ascdt,self.gedcom_town_list,self.choosen_options,self.direction)
            #generate the OpenStreetMap
            generate_map_gedcom(self.direction,y_min, x_min, y_max, x_max,g_max,list_traj,dico_annotation)
            
    def load_ascdt_txt(self):
        """
        Saving the ascendance file generated by Heredis (see the User Manual) in the variable self.fichier_ascendance variable
        """
        self.bouton2.config(state="disabled")
        self.fichier_ascendance = tkFileDialog.askopenfilename(title="Ouvrir le fichier d'ascendance:", initialdir=os.getcwd(), \
                                initialfile="", filetypes = [("Fichiers txt","*.txt"),("Tous", "*")])
        if not self.fichier_ascendance:
            self.bouton2.config(state="active")
        self.type = 1
    def load_descdt_txt(self):
        """
        Saving the descendance file generated by Heredis (see the UserManuel) in the variable self.fichier_descendance
        """
        self.bouton1.config(state="disabled")
        self.fichier_descendance = tkFileDialog.askopenfilename(title="Ouvrir le fichier de descendance:", initialdir=os.getcwd(), \
                                initialfile="", filetypes = [("Fichiers txt","*.txt"),("Tous", "*")])
        if not self.fichier_descendance:
            self.bouton1.config(state="active")
        self.type = 2
    def load_csv(self):
        """
        Saving the town file generated by SQLite Manager (Firefox, see the UserManual) in the variable self.fichier_descendance
        """
        self.fichier_lieux = tkFileDialog.askopenfilename(title="Ouvrir le fichier CSV des Lieux:", initialdir=os.getcwd(), \
                                initialfile="", filetypes = [("Fichiers CSV","*.csv"),("Tous", "*")])
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

    def option_command(self):
        """
        Saving the option choosen by the user in the List self.choosen_options
        """
        for i in range(len(self.option_list)):
            option = self.liste_checkbox[i].get()
            if option:
                self.choosen_options += [self.option_list[i]]
        self.option.destroy()


    def mapping(self):
        """
        Generate the map
        """
        if not self.fichier_lieux or self.type == None:
            tkMessageBox.showwarning(message="Vous n'avez pas charger de fichier d'ascendance / descendance ou de fichier de lieux")
            return
        else:
            if len(self.choosen_options) == 0:
                self.choosen_options = ['Départ(s)','Arrivée(s)']
            if self.type == 1:
                print("import the ascendance file")
                #import ascendance
                ascdt = import_ascendance(self.fichier_ascendance)
                #import the town file
                town_list = import_town_gps_coord(self.fichier_lieux)
                #create annotation text
                dico_annotation = create_annotation_text(ascdt,town_list,self.choosen_options,self.type)
                #compute the trajectory
                list_traj, list_coord = convert_to_trajectory_ascdt(ascdt,town_list)
                #find the min and max coordinate
                y_min, x_min, y_max, x_max, g_max = find_min_max_coordinate(list_coord)
                #generate the OpenStreetMap
                generate_map(self.type,y_min, x_min, y_max, x_max,g_max,list_traj,dico_annotation)
                #mapping the map
                print("mapping the map")
                fig, m, ax = carte(y_min, x_min, y_max, x_max)
                #mapping the trajectories (no return variable)
                print("mapping the trajectories")
                points_with_annotation, list_text_point = mapping_trajectory(list_traj,m,ax, g_max,self.type,dico_annotation)
                
            if self.type == 2:
                print("import the descendance file")
                #import descendance
                descdt = import_descendance(self.fichier_descendance)
                #import the town file
                town_list = import_town_gps_coord(self.fichier_lieux)
                #create annotation text
                dico_annotation = create_annotation_text(descdt,town_list,self.choosen_options,self.type)
                #compute the trajectory *** !!! ***
                list_traj, list_coord = convert_to_trajectory_descdt(descdt,town_list)
                #find the min and max coordinate
                y_min, x_min, y_max, x_max, g_max = find_min_max_coordinate(list_coord)
                #generate the OpenStreetMap
                generate_map(self.type,y_min, x_min, y_max, x_max,g_max,list_traj,dico_annotation)
                #mapping the map
                print("mapping the map")
                fig, m, ax = carte(y_min, x_min, y_max, x_max)
                #mapping the trajectories (no return variable)
                print("Compute the trajectories")
                points_with_annotation, list_text_point = mapping_trajectory(list_traj,m,ax, g_max, self.type,dico_annotation)

        print('showing')

        def on_move(event):
            """
            show dynamical annotation when the mouse pass over the point
                1- get the current axis extremity coordinate and divide them by 20
                2- get the looked point position and the position of his annotation
                3- add the 1/20e of the scale lenght of the curent figure to the xytext coordinate annotation
                4- check all the points if they are outer of the figure and set the text not visible
            """
            #get tuple of limit axis during the time
            x_lim = ax.get_xlim()
            y_lim = ax.get_ylim()
            x = x_lim[0]
            y = y_lim[0]
            x2 = x_lim[1]
            y2 = y_lim[1]
            x10 = (x2-x)/20.
            y10 = (y2-y)/20.
            
            for text in list_text_point:
                x_txt, y_txt = text.get_position()
                
                if x <= x_txt <= x2 and y <= y_txt <= y2:
                    text.set_visible(True)
                else:
                    text.set_visible(False)
                plt.draw()

            visibility_changed = False
            
            for point, annotation in points_with_annotation:
                #get position of the point
                p_xy = point.get_xydata()
                p_x = p_xy[0][0]
                p_y = p_xy[0][1]
                #and set the anotation with add 1/10 of y and x spaces
                annotation.set_position((p_x+x10,p_y+y10))
                
                should_be_visible = (point.contains(event)[0] == True)

                if should_be_visible != annotation.get_visible():
                    visibility_changed = True
                    
                    annotation.set_visible(should_be_visible)

            if visibility_changed:        
                plt.draw()
            
        on_move_id = fig.canvas.mpl_connect('motion_notify_event', on_move)
        plt.show()
            
        self.bouton1.config(state="active")
        self.bouton2.config(state="active")
        self.fichier_descendance = None
        self.fichier_lieux = None
        self.type = None

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
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
AAA7
'''

if __name__ == '__main__':
    app = Peregrination()
    app.run()
