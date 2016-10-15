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

For Linux User
Installation des bibliothèque géospatial nécéssaire à Basemap:
https://docs.djangoproject.com/fr/1.10/ref/contrib/gis/install/geolibs/

Installation de Basemap
http://matplotlib.org/basemap/users/installing.html

Dicdacticiel à la base de ce script :
http://www.xavierdupre.fr/app/actuariat_python/helpsphinx/notebooks/seance6_graphes_enonce.html

Tutorial de Basemap pour ouvrir et manipuler les fichier SHAPEFILE


Source des fichier shapefile belgique et france
http://www.gadm.org/country

API KEY GOOGLE :
 AIzaSyANZgWdIaN4IhFVPVAmi74SO1LD8RtYMPk 
"""

#############
# VARIABLES #
#############

fichier_ascendance = 'ascendance_bouzin.txt'
fichier_lieux = 'Lieux_famille_bouzin.csv'

##########
# IMPORT #
##########

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.patches import PathPatch
from matplotlib import cm
import matplotlib.patches as mpatches
import os
import csv
from operator import itemgetter
"""
import random
from geopy.geocoders import Nominatim
geolocator = Nominatim()
from geopy import geocoders
gl = geocoders.GoogleV3(api_key='AIzaSyANZgWdIaN4IhFVPVAmi74SO1LD8RtYMPk')
"""

#############
# FONCTIONS #
#############

def import_heredis_file(f):
    """
    import the txt file generated by Heredis
    it's important to note than the heredis file are encoded in the iso8859_15 format
    read by the csv library to a list of list with
        0 - Sosa-stradonitz-Number
        1 - First Name
        2 - Date of Birth
        3 - Town of Birth
        4 - Wife
        5 - Wedding Date
        6 - Wedding City
        7 - Date of Death
        8 - Town of Death
        9 - Age
    convert each element of the table into a dict :
        key are Sosa stradonitz number, value are the list
        we replace all the extra elements : '(' , '+', '\xc2\xa0' and convert into integer
    """
    lol = list(csv.reader(open(f, 'r'), delimiter='\t'))
    #print(lol)
    
    ascdt = dict()
    for i in lol:
        key = i[0]
        key = key.decode('iso8859_15').replace(u'\xa0','')
        if "(" in key:
            key = int(key.split()[0])
        elif "+" in key:
            key = int(key.replace("++",""))
        else:
            key = int(key)
        ascdt[key] = i
    return ascdt
    
def import_town_gps_coord(town_file):
    """
    input : town_file : The file generated by Heredis and SQLite Manager
    see the documentation to how have the file
    return dictionary of town with latitude and longitude
    key = town_name value = (latitude,longitude)
    """
    lol = csv.reader(open(town_file, 'r'), delimiter=',')
    dico_town = {rows[0]:[float(rows[1]),float(rows[2])] for rows in lol}
    return dico_town

def check_generation(sosa):
    """
    return the number of the generation by the given sosa number
    """
    i = 0
    generation = None
    while generation == None:
        if sosa < pow(2,i):
            generation = i
        i+=1
    return generation

def convert_to_trajectory(ascdt,town_list):
    """
    convert the dictionnary into a list of trajectory
    """
    list_traj = list()
    list_coord = list()
    for i in ascdt.keys():
        p = i*2
        m = i*2+1
        for prts in p,m:
            if prts in ascdt.keys():
                g = check_generation(prts)
                cityA = ascdt[prts][3].decode('iso8859_15').encode('utf8')
                cityB = ascdt[i][3].decode('iso8859_15').encode('utf8')
                if cityA != ''  :
                    if cityB != '' :
                        if cityA != cityB:
                            print("sosa n° ".decode('utf8')+str(i))
                            print(i, cityA.decode('iso8859_15'),cityB.decode('iso8859_15'))
                            traj = (town_list[cityA][0],town_list[cityA][1],
                                    town_list[cityB][0],town_list[cityB][1],
                                    cityA.decode('utf8'), cityB.decode('utf8'),g)
                            coo = (town_list[cityA][0], town_list[cityA][1],
                                   town_list[cityB][0],town_list[cityB][1])
                            list_traj += [traj]
                            list_coord += [coo]
    return list_traj, list_coord
            
def find_min_max_coordinate(list_coord):
    """
    find the minimum and maximum coordinate to trace the map
    and add a value to have a margin on the map
    """
    array = np.asarray(list_coord)
    minimums = array.min(axis=0)
    x1_min, y1_min, x2_min, y2_min = minimums
    x_min = min(x1_min, x2_min)
    y_min = min(y1_min, y2_min)
    
    maximums = array.max(axis=0)
    x1_max, y1_max, x2_max, y2_max = maximums
    x_max = max(x1_max, x2_max)
    y_max = max(y1_max, y2_max)
    #after found the min and max I had an extra value to have a margin in the map
    return x_min-0.5, y_min-0.5, x_max+0.5, y_max+0.5
    
    

def carte_france(x_min, y_min, x_max, y_max):
    """
    llcrnrlon : longitude of lower left hand corner of the desired map domain (degrees).
    llcrnrlat : latitude of lower left hand corner of the desired map domain (degrees).
    urcrnrlon : longitude of upper right hand corner of the desired map domain (degrees).
    urcrnrlat : latitude of upper right hand corner of the desired map domain (degrees).
    """
    fig, axes = plt.subplots(1, 1, figsize=(9,9))
    m = Basemap(llcrnrlon=y_min,llcrnrlat=x_min, urcrnrlon=y_max,urcrnrlat=x_max,
                resolution='h',projection='cass',lon_0=3.0585800,lat_0=50.6329700,
               ax=axes)
    m.drawcoastlines()
    #looking for all the SHP files in the SHAPEFILE directory

    for root, dirs, files in os.walk(os.getcwd()+"\\SHAPEFILE"):
        for f in files:
            if f.endswith('.shp'):
                name = os.path.splitext(f)[0]
                print('draw limit border of '+name)
                m.readshapefile(root+'\\'+name, name)
        
    m.fillcontinents(color='lightgrey', lake_color='#AAAAFF')
    print('draw rivers')
    m.drawrivers(color='b')
    #m.bluemarble()
    m.drawparallels(np.arange(-40,61.,2.))
    m.drawmeridians(np.arange(-20.,21.,2.))
    m.drawmapboundary(fill_color='#BBBBFF')
    fig.show()
    return m, axes

def trajectoire(list_traj,m,ax):
    """
    input :
    list_traj : list of the trajectory computed by convert_ti_trajectory function
    m, ax : basemap and axis computed by carte_france function
    to dont have cover of the last generation to the first,
    we sort the list in reverse order by the number of generation
    """
    list_traj = sorted(list_traj, key=itemgetter(6), reverse=True)
    for vecteur in list_traj:
        lat1,lon1,lat2,lon2,name1,name2,g = vecteur
        size = g*3

        x1,y1 = m(lon1, lat1)
        m.plot(x1, y1, 'o', markersize=size,markeredgewidth=0.0,color=cm.Paired(1.*g/10))
        ax.text(x1, y1, name1)

        x2,y2 = m(lon2, lat2)
        m.plot(x2, y2, 'o', markersize=size,markeredgewidth=0.0,color=cm.Paired(1.*g/10))
        m.drawgreatcircle(lon1,lat1,lon2,lat2,linewidth=2,color=cm.Paired(1.*g/10))
        ax.text(x2, y2, name2)









