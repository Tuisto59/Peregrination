# Peregrination
%% LyX 2.2.1 created this file.  For more info, see http://www.lyx.org/.

%% Do not edit unless you really know what you are doing.

\documentclass[oneside,english,oldfontcommands]{memoir}

\usepackage[T1]{fontenc}

\usepackage[latin9]{inputenc}

\usepackage{geometry}

\geometry{verbose,tmargin=2cm,bmargin=2cm,lmargin=2cm,rmargin=2cm}

\setcounter{secnumdepth}{3}

\setcounter{tocdepth}{3}

\usepackage{color}

\usepackage{babel}

\usepackage{graphicx}

\PassOptionsToPackage{normalem}{ulem}

\usepackage{ulem}

\usepackage[unicode=true]

 {hyperref}

\usepackage{breakurl}

\begin{document}

\title{{\Huge{}MODE D'EMPLOI}}

\author{Yoan BOUZIN}

\maketitle

\begin{center}

\includegraphics{\string"C:/Users/Yoan/Desktop/fichier heredis eeepc genealogie/mode d'emplois geolocalisation/Peregrination2\string".eps}

\par\end{center}

\begin{center}

\includegraphics[scale=0.6]{figure_3}

\par\end{center}

\chapter{Logiciels}

\section{Logiciel de G�n�alogie:}

\begin{itemize}

\item H�r�dis (Bleu) (ou sup�rieur)

\end{itemize}

\section{Navigateur \& Add-on :}

\begin{itemize}

\item Firefox

\begin{itemize}

\item Add SQLite Manager

\end{itemize}

\end{itemize}

\section{Utilisateur Windows:}

Si vous utilisez Windows et que vous n'avez pas install� le language

de programmation Python. Pour vous �viter une installation manuel

de Python et de toute ses librairie (matplotlib, numpy, ...) je vous

invite � suivre ces �tapes

\subsection{Installation du langage de programmation Python : l'IDE Python X,Y}

Python

Comme expliquer sur ce PDF : \href{http://prepas.org/2013/Info/DocumentsIG/install-python-windows.pdf}{http://prepas.org/2013/Info/DocumentsIG/install-python-windows.pdf},

Python est un language de programmation et non un programme avec un

``.exe'' que l'ont clique dessus. 

Sur les syst�mes d'exploitations de type Linux, ce dernier et d�j�

disponible (g�n�rallement la version 2.7) actuellement la derni�re

version et la 3.5. Sur windows nous devons l'installer. 

Pour pouvoir l'utilis� il faut installer un IDE (Environnement de

d�velloppement) qui vous permettra d'ouvrir, cr�� et ex�cuter vos

script. Nous allons installer un IDE appell� Python X,Y disponible

ici en t�l�chargement : http://python-xy.github.io/downloads.html

\begin{enumerate}

\item T�l�charger Python X,Y \href{http://www.mirrorservice.org/sites/pythonxy.com/Python(x,y)-2.7.10.0.exe}{http://www.mirrorservice.org/sites/pythonxy.com/Python(x,y)-2.7.10.0.exe}

\item Installez Python X,Y , l'installation et longue, je vous propose de

regarder une video ou de faire une recherche g�n�alogique ;)

\end{enumerate}

\subsection{Installation de la librairie Basemap (librairie de carthographie)

:}

\begin{enumerate}

\item Une fois l'installation termin� t�l�charger la librairie Basemap �

cette adresse : \href{http://sourceforge.mirrorservice.org/p/py/python-xy/plugins/basemap-1.0.2_py27.exe}{http://sourceforge.mirrorservice.org/p/py/python-xy/plugins/basemap-1.0.2\_{}py27.exe}

\end{enumerate}

\section{Utilisateur Linux:}

\subsection{Librairies utilis� :}

Vous devez avoir installer Numpy et Matplotlib

pour cela je vous conseil d'utiliser l'instalateur PIP

\begin{verbatim}

sudo pip install matplotlib --upgrade

sudo pip install numpy

\end{verbatim}

\begin{flushleft}

Installation des biblioth�que g�ospatial n�c�ssaire � Basemap: 

\par\end{flushleft}

\begin{flushleft}

https://docs.djangoproject.com/fr/1.10/ref/contrib/gis/install/geolibs/

\par\end{flushleft}

\begin{flushleft}

Installation de Basemap

\par\end{flushleft}

\begin{flushleft}

http://matplotlib.org/basemap/users/installing.html

\par\end{flushleft}

\chapter{Installez les cartes des pays:}

Pour pouvoir afficher les fronti�res des pays, des d�partements, des

communes nous avons besoin d'un fichier qui contient toute les informations

pour permettre de les tracer avec les latitudes et les longitudes.

Ce sont se qu'on apelle des fichier SHAPEFILE (traduis� ``fichier

de formes''). Ils sont disponible librement et sont cr�� par des

d�velloppeur ind�pendant. Vous pouvez les t�l�charger via se site

internet : \href{http://www.gadm.org/country}{http://www.gadm.org/country}Choisissez

votre Pays (Country) et choisissez ``Shapefile'' dans les format

de fichier (File format), t�l�charger le fichier compr�ss� et d�compr�ss�

le contenue dans le dossier SHAPEFILE. Pour faire fonctionn� 

\begin{enumerate}

\item T�l�charger et d�zip� la carte de France dans le dossier SHAPEFILE\\

http://biogeo.ucdavis.edu/data/gadm2.8/shp/FRA\_adm\_shp.zip

\item T�l�charger et d�zip� la carte de Belgique dans le dossier SHAPEFILE\\

http://biogeo.ucdavis.edu/data/gadm2.8/shp/BEL\_adm\_shp.zip

\end{enumerate}

\chapter{Export des donn�es GPS du dictionnaire des Lieux de Heredis:}

\begin{enumerate}

\item Avec H�r�dis faite : Fichier &gt; Pr�parer pour ... &gt; Heredis Mac\\

\includegraphics[scale=0.4]{\string"../fichier heredis eeepc genealogie/mode d'emplois geolocalisation/1\string".eps}

\item Acceptez et enregistrez\\

\includegraphics[scale=0.4]{\string"C:/Users/Yoan/Desktop/fichier heredis eeepc genealogie/mode d'emplois geolocalisation/2\string".eps}

\item Si vous utilisez Firefox, installer SQLite Manager (\textcolor{blue}{\uline{\href{https://addons.mozilla.org/fr/firefox/addon/sqlite-manager/}{SQLIte Manager}}})\\

\includegraphics[scale=0.4]{\string"C:/Users/Yoan/Desktop/fichier heredis eeepc genealogie/mode d'emplois geolocalisation/3\string".eps}

\item Apr�s installation, d�marer le module, dans Outils &gt; SQLite Manager\\

\includegraphics[scale=0.4]{\string"../fichier heredis eeepc genealogie/mode d'emplois geolocalisation/4\string".eps}

\item Une nouvelle fen�tre apparait, cliquez sur Ouvrir\\

\includegraphics[scale=0.4]{\string"../fichier heredis eeepc genealogie/mode d'emplois geolocalisation/5\string".eps}

\item Avec la boite de dialogue parcourez vos dossier, pour faire apparaitre

les fichiers, selectionner ``Tout les fichier'' dans la liste d�roulante,

selectionner le fichier et cliquez sur Ouvrir\\

\includegraphics[scale=0.4]{\string"../fichier heredis eeepc genealogie/mode d'emplois geolocalisation/6\string".eps}

\item Les donn�es contenue dans le fichier H�r�dis pour Mac et convertit

en une base de donn�es SQL (\textit{Structured Query Language} , en

fran�ais Language de requ�te structur�, plus d'info ici :\href{https://fr.wikipedia.org/wiki/Structured_Query_Language}{Wkipedia}).

Vous pouvez donc voir apparaitre toutes les donn�es de votre fichier

sous la forme de Table, ces tables sont les �l�ments principaux de

la base de donn�es, se sont elles qui contiennent les informations.

Sur le volet de gauche vous verrez appara�tre les diff�rentes tables

du fichier, je vous invite � d�couvrir la table ``Lieux'' en double-cliquant

dessus.\\

\includegraphics[scale=0.4]{\string"../fichier heredis eeepc genealogie/mode d'emplois geolocalisation/7\string".eps}\\

\item Vous verrez apparaitre le d�tail de la table ``Lieux'' ainsi qu'un

tas d'informations utile pour les d�velloppeurs confirm�s en SQL,

nous allons maintenant exporter de cette table les informations utiles\\

\includegraphics[scale=0.4]{\string"C:/Users/Yoan/Desktop/fichier heredis eeepc genealogie/mode d'emplois geolocalisation/8\string".eps}

\item Allez dans l'onglet ``Executer le SQL'' et dans la case ``Entrez

les commandes SQL'' effacez l'exemple ``SELECT {*} FROM tablename''

et copier coller cette requ�te SQL :SELECT Ville, Latitude, longitude

FROM Lieux\\

\texttt{\textcolor{blue}{\emph{\includegraphics[scale=0.4]{\string"../fichier heredis eeepc genealogie/mode d'emplois geolocalisation/9\string".eps}}}}\\

Cette requ�te signifie en gros : s�lectionn� les colonne ``Ville'',

``Latitude'', ``Longitude'' de la table ``Lieux''

\item Maintenant cliquez sur le bouton ``Action'' et dans la liste d�roulante

``\textit{Save Result (CSV) to File}'' (Sauvegarder le r�sultat

(CSV) dans un fichier). Un fichier au format CSV et un fichier o�

les informations sont s�par� par un d�limitateur, le plus souvent,

des virgules (CSV = Comma Separated Values , Valeur S�par� par des

virgules, \href{https://fr.wikipedia.org/wiki/Comma-separated_values}{CSV})

ces dernier sont donc exploitable par Excel, OpenOffice, LibreOfice,

et d'autre languages de programmation (exemple ici quand le fichier

et ouvert avec LibreOffice).\\

\includegraphics[scale=0.4]{\string"../fichier heredis eeepc genealogie/mode d'emplois geolocalisation/10\string".eps}\\

\includegraphics[scale=0.4]{\string"../fichier heredis eeepc genealogie/mode d'emplois geolocalisation/11\string".eps}

\end{enumerate}

Enfin vous disposez d'un fichier CSV contenant la liste des latitudes

et longitudes de votre fichier g�n�alogique. Ce dernier nous servira

pour placer les trajectoires pour les p�rigrinations.

\chapter{Export des donn�es de la liste ascendante sous la forme TXT (ASCII):}

\begin{enumerate}

\item Avec H�r�dis, allez dans ``Documents'' &gt; ``Listes d'ascendances''

&gt; ``Compl�te...''\\

\includegraphics[scale=0.3]{\string"../fichier heredis eeepc genealogie/mode d'emplois geolocalisation/ascii1\string".eps}

\item Dans l'onglet ``Pr�sentation'' dans la section ``Styles des rubriques''

dans la cat�gorie ``Lieux : '' s�lectionn� ``Commune''\\

\includegraphics[scale=0.4]{\string"../fichier heredis eeepc genealogie/mode d'emplois geolocalisation/ascii2\string".eps}

\item Cliquez directement sur ``Exporter''\\

\includegraphics[scale=0.4]{\string"../fichier heredis eeepc genealogie/mode d'emplois geolocalisation/ascii3\string".eps}

\item Enregistrer le fichier dans le dossier et dans le nom de votre choix\\

\includegraphics[scale=0.4]{\string"../fichier heredis eeepc genealogie/mode d'emplois geolocalisation/ascii4\string".eps}

\end{enumerate}

\chapter{Utilisation :}

\begin{enumerate}

\item Doucle-clic sur le fichier Demo.py, la console IPython s'ouvre et

execute le script et une f�netre s'affiche. Ceci peux prendre un certain

temps.\\

\includegraphics[scale=0.6]{\string"C:/Users/Yoan/Desktop/fichier heredis eeepc genealogie/mode d'emplois geolocalisation/Peregrination\string".eps}

\item Cliquez sur le bouton ``Charger le fichier d'ascendance'', parcourer

dans vos dossier et cliquez sur le fichier d'ascendance que vous avez

g�n�r� {[}voir Chapitre 3{]}

\item Cliquez ensuite sur le bouton ``Charger le fichier de lieux'', parcourez

dans vos dossier et cliquez sur le fichier de lieux g�n�r� que vous

avez cr�� {[}voir Chapitre 2{]}

\item Cliquez ensuite sur ``Cr�� la carte'', la console d�file, les sosa

sont analys�e un par un et quand le p�re ou la m�re d'un sosa et n�

dans une commune diff�rente que l'enfant, la trajectoire et calcul�

et puis affich� dans la console. A la fin de l'analyse, une fen�tre

s'affiche avec la carte des commune de France et de Belgique, r�gl�

en fonction des communes.

\end{enumerate}

\begin{center}

\includegraphics[scale=0.5]{\string"C:/Users/Yoan/Desktop/fichier heredis eeepc genealogie/mode d'emplois geolocalisation/console-python-after\string".eps}

\par\end{center}

\begin{center}

\includegraphics[scale=0.9]{\string"C:/Users/Yoan/Desktop/fichier heredis eeepc genealogie/mode d'emplois geolocalisation/map-result\string".eps}

\par\end{center}

\begin{enumerate}

\item Pour pouvoir naviguer dans la carte, il suffit d'utiliser les outils

suivant mis � votre disposition \includegraphics{\string"C:/Users/Yoan/Desktop/fichier heredis eeepc genealogie/mode d'emplois geolocalisation/matplotlib-tool\string".eps}

\begin{enumerate}

\item La fl�che gauche permet de revenir � l'action pr�c�dente

\item la fl�che droite permet de revenir � l'action suivante

\item La croix multidirectionelle permet de d�placer le graphique dans le

cadre

\item La loupe permet de d�finir un cadre

\end{enumerate}

\end{enumerate}

\begin{center}

\includegraphics[scale=0.5]{figure_1}

\par\end{center}

\legend{Premier Zoom au niveau de la r�gion du Nord-Pas-de-Calais / Belgique}

\begin{center}

\includegraphics[scale=0.5]{figure_2}

\par\end{center}

\legend{Deuxi�me zoom au niveau de la r�gion Lille , Flandres Belges}

\begin{center}

\includegraphics[scale=0.85]{figure_3}

\par\end{center}

\legend{Troisi�me zoom au niveau de la r�gion Roubaix}

\end{document}
