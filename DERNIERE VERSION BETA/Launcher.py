#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
(c) Copyright Yoan BOUZIN

  This file is part of Pérégrination v1.0.

    Pérégrination v1.0 is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Pérégrination v1.0 is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Pérégrination v1.0.  If not, see <http://www.gnu.org/licenses/>. 2

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
        self.main.title("Pérégrination v1.5")
        #self.main.geometry("176x145")
        #self.main.resizable(width=False, height=False)
        self.main.configure(bg="#a0522d")
        self.label1 = Tkinter.Label(self.main,text="Pérégrination v 1.0", font=(font, 12), bg="#f5deb3")
        self.label1.grid(sticky='EW', padx=10, pady=5)
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
                if line.startswith('1 PLAC'):
                    town_sub = 1
                if line.startswith('2 FORM ') and town_sub == 1:
                    town_org = line.replace('2 FORM ','').replace('\n','').replace(' ','').split(',')
                    town_sub = None
                if line.startswith('2 PLAC '):
                    town_set.add(line.replace('2 PLAC ',''))
        return town_set, town_org

    def get_gps_GoogleMapHTMLRequest(self, adress):
        adress = adress.decode('iso8859_15')
        adress = adress.encode('utf8')
        adress = urllib2.quote(adress)
        r = requests.get(u'https://www.google.fr/maps/place/'+adress)
        text = r.text
        try:
            lat, lon = eval(re.findall(ur'\[[-+]?\d+\.\d+,[-+]?\d+\.\d+\]',r.text)[0])
            return lat,lon
        except:
            return None, None
        
        
    def nominatim(self, adress):
        geolocator = Nominatim()
        lat = None
        lon = None
        for i in adress:
            if i != '':
                print("Essaie avec : "+i)
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
            lat, lon = None, None
            town_string = town.replace('\n','')
            
            self.pb['value'] = int(cpt/len(towns)*100)
            self.pb.update_idletasks()
            self.label_pb['text'] = str(round(cpt/len(towns)*100,2))+" %"
            self.label_pb.update_idletasks()
            self.label_pb.update()       
            self.label_town_pb['text'] += "\nRecherche : "+town_string
            self.label_town_pb.update_idletasks()
            self.label_town_pb.update()
            self.pb_gui.update()
            
            town_list = town_string.split(',')
            if town_string not in town_set:
                #print("not in town set")
                town_set.add(town_string)
                city = town_list[self.dico_index_subdivisions['Town']]
                code = town_list[self.dico_index_subdivisions['Areacode']]
                sub = town_list[self.dico_index_subdivisions['Subdivision']]
                country = town_list[self.dico_index_subdivisions['Country']]
                adresse1 = sub+" "+city+" "+code+" "+country
                adresse2 = city+" "+code+" "+country
                adresse3 = city
                #loop the adress
                for adre in adresse1,adresse2,adresse3:
                    #print(adre)
                    #check if the address already done
                    #if not
                    if adre not in town_set:
                        #print("adress not in town set")
                        #get gps coordinate through the google map html request for the given adress
                        result = self.get_gps_GoogleMapHTMLRequest(adre)
                        #print("gps result google map",result)
                        lat, lon = result
                        #we have the gps coordinate for the i-th adress
                        if lat:
                            #print("we have gps from gmap")
                            self.label_town_pb['text'] = town_string+' : '+str(lat)+','+str(lon)
                            self.label_town_pb.update_idletasks()
                            self.label_town_pb.update()
                            self.pb_gui.update()
                            
                            dico_gps_adre[adre] = (lat,lon)
                            dico_gps[town_string] = result
                            #we add the working adress to the set (because we have the corresponding key in dict)
                            town_set.add(adre)
                            #we have the result, break the loop and continue to next  iterationert-for loop
                            #print("break loop")
                            break
                        #if not, continue the loop
                    #else, the address already done
                    else:
                        #print("adre already in town set")
                        #print("town_string",town_string)
                        #print("adre",adre)
                        #get the GPS coordinate of the i-th adress
                        lat, lon = dico_gps_adre[adre]
                        dico_gps[town_string] = dico_gps_adre[adre]
                        #exit the loop (because we have the gps coordinate)
                        #print("break")
                        break
                    #END if/else
                #END nested adress loop
                #if lat (or lon) are ever None after the adress loop try to get the gps with other technique
                #print("current lat,lon after loop adress",lat,lon)
                if lat == None:
                    self.label_town_pb['text'] += "\n### Echec lors de la recuperation des donnees GPS\n### Essai de recuperation avec Nominatim (OpenStreetMap) :"
                    self.label_town_pb.update_idletasks()
                    self.label_town_pb.update()
                    self.pb_gui.update()
                    #last chance to retrieve None result with nominatin
                    lat, lon = self.nominatim(town_list)
                    self.label_town_pb['text'] += "\nOpenStreetMap GPS : "+str(lat)+", "+str(lon)
                    self.label_town_pb.update_idletasks()
                    self.label_town_pb.update()
                    self.pb_gui.update()
                    
                    if lat:
                        dico_gps[town_string] = (lat,lon)
                    else:
                        self.label_town_pb['text'] += "\n### La commune n as pas ete retrouve"
                        self.label_town_pb.update_idletasks()
                        self.label_town_pb.update()
                        self.pb_gui.update()
                        fail += 1
                #END If lat == none
            #END if town_string not in town_set
        #End towns loop
        writer = csv.writer(output, delimiter=',', lineterminator='\n')
        for i in dico_gps.keys():
            row = [i,dico_gps[i][0],dico_gps[i][1]]
            writer.writerow(row)
        b = time.time()
        seconds = b-a
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        self.pb_gui.destroy()
        tkMessageBox.showinfo(title="Terminé",message=str(len(town_set)-fail)+" ont été retrouvé(s)\n"+str(fail)+" n'ont pas été retrouvé(s)\nRéalise en %d:%02d:%02d secondes" % (h, m, s))
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
        self.question = tkMessageBox.askquestion('Ordre des subdivisions des lieux', "Valider l'ordre ?\n"+",".join(self.town_org))
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
        nb_col = len(town_org)
        self.label_titre.grid(row=0,columnspan = 10)
        
        #create a frame/canvas/frame to see the first 10th city
        #====== FRAME CONSOLE ======
            #first frame
        
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
            self.fields = ttk.Combobox(self.subdivision, textvariable = self.field, values = town_org, width=len(max(self.town_org, key=len)))
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
        
    def ascendance(self, ID, sosa=1, generation=10, liste = dict()):
        """
        return the ascendance of the given ID
        """
        liste_data = self.dico_data_list[ID]
        liste[sosa]=liste_data
        id_father = liste_data[-2]
        if id_father != '':
            liste = self.ascendance(id_father, sosa=sosa*2, liste=liste)
        id_mother = liste_data[-1]
        if id_mother != '':
            liste = self.ascendance(id_mother, sosa=sosa*2+1, liste=liste)
        return liste
    
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
            if self.town_org[item] == 'Areacode':
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
        self.pb_gui.destroy()
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
            self.ascdt = self.ascendance(self.ID)
            self.gedcom_map()
                
    def gedcom_map_validate(self):
        self.regroup.destroy()
        self.criteria = self.varchoice.get()
        if self.direction == 1:
            #make ascdt type object
            ascdt = self.ascendance(self.ID)
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

if __name__ == '__main__':
    app = Peregrination()
    app.run()
