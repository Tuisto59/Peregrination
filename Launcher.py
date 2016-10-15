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
"""

###########
# IMPORTS #
###########

from peregrination import *
import Tkinter
import tkFileDialog
import tkMessageBox

######
# GUI #
######

class Peregrination():
    #principal application
    def __init__(self):
        """
        initialize GUI
        """
        self.main = Tkinter.Tk()
        self.main.title("")
        #self.main.geometry("176x145")
        #self.main.resizable(width=False, height=False)
        self.main.configure(bg="#a0522d")
        self.label1 = Tkinter.Label(self.main,text="Pérégrination v 1.0", font=("Segoe Script", 12), bg="#f5deb3")
        self.label1.grid(sticky='EW', padx=10, pady=5)
        self.bouton1 = Tkinter.Button(master=self.main,text="Charger le fichier d'ascendance", command=self.load_txt,bg="#f5deb3")
        self.bouton1.grid(sticky='EW')
        self.bouton2 = Tkinter.Button(master=self.main,text="Charger le fichier de lieux", command=self.load_csv,bg="#f5deb3")
        self.bouton2.grid(sticky='NSEW')
        self.bouton3 = Tkinter.Button(master=self.main,text="Créé la carte", command=self.mapping,bg="#f5deb3")
        self.bouton3.grid(sticky='NSEW')
        self.bouton4 = Tkinter.Button(master=self.main,text="Quitter",command=self.main.destroy,bg="#f5deb3")
        self.bouton4.grid(sticky='NSEW')
        self.label1 = Tkinter.Label(self.main,text="© Yoan BOUZIN - Licence GNU", font=("Segoe Script", 12), bg="#f5deb3")
        self.label1.grid(sticky='EW', padx=10, pady=5)
        self.fichier_ascendance = None
        self.fichier_lieux = None
    def run(self):
        """
        function to keep the windows in live
        """
        self.main.mainloop()
    def load_txt(self):
        self.fichier_ascendance = tkFileDialog.askopenfilename(title="Ouvrir le fichier d'ascendance:", initialdir=os.getcwd(), \
                                initialfile="", filetypes = [("Fichiers txt","*.txt"),("Tous", "*")])
    def load_csv(self):
        self.fichier_lieux = tkFileDialog.askopenfilename(title="Ouvrir le fichier CSV des Lieux:", initialdir=os.getcwd(), \
                                initialfile="", filetypes = [("Fichiers CSV","*.csv"),("Tous", "*")])
    def mapping(self):
        if self.fichier_ascendance == None or self.fichier_lieux ==  None:
            tkMessageBox.showwarning(message="Vous n'avez pas charger de fichier d'ascendance ou de lieux")
            return
            
        print("import the file")
        ascdt = import_heredis_file(self.fichier_ascendance)
        town_list = import_town_gps_coord(self.fichier_lieux)
        print("compute gps coordinate and trajectory")
        list_traj, list_coord = convert_to_trajectory(ascdt,town_list)
        x_min, y_min, x_max, y_max = find_min_max_coordinate(list_coord)
        print("mapping the map")
        m, ax = carte_france(x_min, y_min, x_max, y_max)
        print("mapping the trajectories")
        trajectoire(list_traj,m,ax)
        print("legend")
        #plot legend
        #check the maximum generation
        g_max = check_generation(max(ascdt.keys()))
        patch_list = list()

        for i in range(1,g_max+1):
            patch_list.append(mpatches.Patch(color=cm.Paired(1.*i/g_max), label='Gen. '.decode('utf8')+str(i)))
        plt.legend(handles=patch_list, loc='upper center', bbox_to_anchor=(0.5, 0.0),fancybox=True, shadow=True, ncol=5)

        plt.show()

############
# AUTORUN #
############

if __name__ == '__main__':
    app = Peregrination()
    app.run()
