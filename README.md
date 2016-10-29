

[Source](http://peregrination.jimdo.com/manuel-d-utilisation/ "Permalink to Manuel d'utilisation - Pérégrination : Cartographie généalogique")

# Manuel d'utilisation - Pérégrination : Cartographie généalogique

Pour les non-spécialistes de l'informatique, je vais à la fois parler de termes techniques que je vais agrémenter d'exemple simple pour vous expliquer à la fois la simplicité et la complexité de ce qui se cache parfois derrière l'informatique. :)

Pérégrination ©, utilise pour fonctionné un [langage de programmation][1]. Ce langage de programmation s'appelle Python.  Comme les langues vivantes (Anglais, Français, Allemand, Chinois,...) un ordinateur parle aussi une langue, le binaire (0 et 1) or pour un être humain, c'est absolument impossible, et incompréhensible de parlé ce langage.

 

Les informaticiens ont donc inventés des langages, pour communiquer et donner des ordres aux ordinateurs. Ces langages ont été inventé d'abord par les américains, de ce fait, les mots utilisés dans le langage sont en anglais. Or, lorsque nous voyageons à l'étranger, il nous faut un interprète pour pouvoir souvent comprendre la langue du pays étranger.

 

Pour un ordinateur c'est exactement la même chose. L'ordinateur à besoin d'un programme qui convertit ces langages en langage "ordinateur", en binaire, et ce programme et appelé un [Interpréteur][2]. Ces langages sont communément appelés des langages de programmation, ils nous permettent d'interagir avec les composants physiques de l'ordinateur (disque dur, processeur...) et virtuel (fichiers, mémoire vive, ...), et permettent d'exécuter des taches très complexes et multiples, du fait de la capacité naturelle d'un ordinateur à réaliser des opérations en parallèle.

 

Car mon programme à été écrit en Python nous devons installer l'interpréteur Python. En plus de l'interpréteur, il vous installera ce que l'ont appelle des [bibliothèque logicielle][3] ou librairies. Imaginer une vraie bibliothèque, ce bâtiment contient des livres, et ces livres des chapitres. Chaque livre parle d'un sujet particulier, Science, Math, Littérature, Psychologie, Jeux, etc... En programmation , c'est la même chose, on aime bien nommer les choses avec celles du quotidien.

 

Une librairie et un ensemble de fichiers (comparer le à une série de tome) qui contient un ensemble de fonctions (qui seront ici nos chapitres) et chaque fonction a son propre but bien défini. Ainsi en python nous avons la librairie "[_math_][4]" qui permet de calculer Pi, de réaliser des puissances, de la trigonométrie, etc... Bien sur, un programmeur aurait put avoir l'envie de créer lui même sa propre fonction, réalisant le même but, mais souvent il est conseillé d'utiliser les fonctions des librairies, bien plus efficaces et rapides.

 

Comme ont dit en programmation, il ne sert à rien de réinventer la roue, si vous avez envie de faire quelque chose, quelqu'un l'aura déjà fait avant vous !

Vous aurez besoin de ces logiciels pour pouvoir convertir votre généalogie en plusieurs fichiers

![][5]

 

 

* Hérédis Bleu ou version supérieur

Ce navigateur ainsi que son module SQLite Manager nous serons très utile par la suite afin d'extraire les données GPS du fichier de Hérédis.

![][6]

![][7]

![][8]

![][9]

  

Pour que le programme fonctionne, nous devons installer un interpréteur Python.

 

Cet interpréteur et disponible sur le site officiel . Vous pouvez installer manuellement ces interpréteurs (actuellement la version 2.7.10 et 3.5.2). Vous aurez aussi besoin d'installer des librairies qui ne sont pas installées avec l'interpréteur, il s'agit des librairies NumPy, Matplotlib et Basemap. Enfin, si vous souhaitez visualiser ou modifier le code source, tester et exécuter vos scripts, vous devriez installer un Environnement de développement (IDE en Anglais). Vous pouvez faire manuellement tout ceci en prenant le temps de regardez la documentation associée sur le web, cela nécessite beaucoup de persévérance ! Heureusement pour vous, il existe un programme tout en un qui réalise tout ça pour vous ! Il s'agit de Python XY.

1. Télécharger Python X,Y 
2. Installez Python X,Y en suivant les paramètres qu'il vous indique
3. Patientez, l'installation peut être longue, je vous suggère en attendant de regarder une vidéo ou de réaliser une recherche généalogique ou de mettre à jour le dictionnaire des lieux de votre logiciel de généalogie  ;)

 

Voici la vidéo sur YouTube de l'installation de Python X,Y (Anglais)

Pour les non-anglais, vous pouvez générer les sous-titre et réaliser la traduction automatique des sous-titres:

(Valable uniquement pour les vidéos en langue anglo-saxonne)

1.  Avec votre souris cliquez sur le bouton "Sous-titre" (carré avec des petits trait à l'intérieur en bas à droite)
2. Ensuite cliquez sur "Paramètres" (roue cranté)
3. Sur la fenêtre qui s'affiche sur la vidéo cliquez sur "Sous-titres (1)         Anglais (généré automatiquement) >"
4. Cliquez sur "Traduire automatiquement"
5. Un nouveau volet s'affiche avec une liste de langue, à l'aide de l'ascenseur sur la gauche cliquez sur la langue "Français"
6. Puis cliquez n'importe pour revenir a la vidéo avec les sous-titre en Français : Note vous pouvez cliquez sur les sous-titre et les mettre n'importe où.

1. Une fois l'installation terminée télécharger la librairie Basemap à cette adresse :  puis double-cliquez pour l'installé  

![][10]

 

 

Mon ordinateur ayant à la fois installé sur son disque dur, deux systèmes d'exploitation (Windows et Linux), je peux à la fois tester mon programme dans un environnement Linux et Windows. Pour le moment le programme fonctionne sur Ubuntuu version 14.04.1. Je ne l'ai donc pas essayé sur Mac, Fédora, RedHat et Debian. Les interpréteurs Python étant déjà installés avec les librairies de base je vous recommande d'installer si cela n'est pas encore fait l'installateur de paquet PIP. Dans un terminal copier coller ses deux lignes de commandes. La première sert à installer  PIP,  et les composants de bases de python, la seconde permet de la mettre à jour.

    $ sudo apt-get install python-pip python-dev build-essential
    $ sudo pip install --upgrade pip

Ensuite nous devons installer les librairies Matplotlib et NumPy et Basemap

Pour installer Matplotlib, selon la documentation (Anglaise) de leur site internet suivant si vous êtes sur un système Linux/Debian ou Fedora/RedHat (http://matplotlib.org/1.5.1/users/installing.html)

    $ sudo pip install matplotlib
    $ sudo pip install --upgrade matplotlib

    $ sudo pip install numpy
    $ sudo pip install --upgrade numpy

https://docs.djangoproject.com/fr/1.10/ref/contrib/gis/install/geolibs/

http://matplotlib.org/basemap/users/installing.html

 

![][11]

Pour pouvoir afficher les frontières des pays, des départements, des communes nous avons besoin d'un fichier qui contient toute les informations pour permettre de les tracer avec les latitudes et les longitudes. Ce sont ce qu'on appelle des fichiers SHAPEFILE (traduisé "fichier de forme"). Ils sont disponibles librement et sont créés  par des développeurs indépendants. Vous pouvez les télécharger via ce site internet : [http://www.gadm.org/country][12]

 

Choisissez votre Pays (Country) et choisissez "Shapefile" dans les formats de fichiers (File format), télécharger le fichier compressé et décompressé le contenue dans le dossier SHAPEFILE

1. Télécharger et dézipé la carte de France dans le dossier SHAPEFILE

> 1. Télécharger et dézipé la carte de Belgique dans le dossier SHAPEFILE

> ![Capture d'écran sur le site de GADM avec le fichier Shapefile de la France.][13]Capture d'écran sur le site de GADM avec le fichier Shapefile de la France.

Avec Hérédis faite : Fichier > Préparer pour ... > Heredis Mac

![][14]

![][15]

Si vous utilisez Firefox, installer SQLite Manager (SQLIte Manager)

![][16]

Après installation, démarrer le module, dans Outils > SQLite Manager

![][17]

Une nouvelle fenêtre apparaît, cliquez sur Ouvrir

![][18]

Avec la boite de dialogue parcourez vos dossiers, pour faire apparaître les fichiers, sélectionner "Tout les fichiers" dans la liste déroulante, sélectionner le fichier et cliquez sur Ouvrir

![][19]

Les données contenue dans le fichier Hérédis pour Mac et convertit en une base de données SQL (Structured Query Language , en français Language de requête structuré, plus d'info ici :Wkipedia). Vous pouvez donc voir apparaître toutes les données de votre fichier sous la forme de Table, ces tables sont les éléments principaux de la base de données, ce sont elles qui contiennent les informations. Sur le volet de gauche vous verrez apparaître les différentes tables du fichier, je vous invite à découvrir la table "Lieux" en double-cliquant dessus.

![][20]

Vous verrez apparaitre le détail de la table "Lieux" ainsi qu'un tas d'informations utiles pour les développeurs confirmés en SQL, nous allons maintenant exporter de cette table les informations utiles.

![][21]

Allez dans l'onglet "Executer le SQL" et dans la case "Entrez les commandes SQL" effacez l'exemple "SELECT * FROM tablename" et copier coller cette requête SQL :SELECT Ville, Latitude, longitude FROM Lieux

![][22]

Cette requête signifie en gros : sélectionner les colonnes "Ville", "Latitude", "Longitude" de la table "Lieux"

  
Maintenant cliquez sur le bouton "Action" et dans la liste déroulante "Save Result (CSV) to File" (Sauvegarder le résultat (CSV) dans un fichier). Un fichier au format CSV et un fichier où les informations sont séparées par un délimiteur, le plus souvent, des virgules (CSV = Comma Separated Values , Valeur Séparé par des virgules, CSV) ces dernier sont donc exploitable par Excel, OpenOffice, LibreOfice, et d'autre langages de programmation (exemple ici quand le fichier et ouvert avec LibreOffice).

![][23]

![][24]

Enfin vous disposez d'un fichier CSV contenant la liste des latitudes et longitudes de votre fichier généalogique. Ce dernier nous servira pour placer les trajectoires pour les pérégrinations.

Avec Hérédis, allez dans "Documents" > "Listes d'ascendances" > "Complète..."

![][25]

Dans l'onglet "Présentation" dans la section "Styles des rubriques" dans la catégorie "Lieux : " sélectionnez "Commune"

![][26]

Cliquez directement sur "Exporter"

![][27]

Enregistrez le fichier dans le dossier et dans le nom de votre choix

![][28]

![GUI sous Linux][29]GUI sous Linux

![GUI sous Windows 8][30]GUI sous Windows 8

  

1. Télécharger le fichier ZIP
2. Extraire les fichiers du ZIP dans le dossier de votre choix
3. Double-clic sur "Launcher.py"

La première fois que vous l'utiliserai, une console vas s'ouvrir, ceci est tout à fait normal. Sur cette console des lignes défileront. Explication, le programme vas détecter si vous posséder sur votre ordinateur tout les éléments nécessaire pour son fonctionnement.

 

La librairie 'folium' n'est pas une librairie native de Python, elle n'est pas non plus apporter avec l'installation de Python X,Y. A l'intérieur du programme, dans le code source, le programme vas détecter la présence ou non de ces librairies, et les installer.

 

Pour les installer, Python possède un programme spécial qui s'appelle PIP. C'est ce programme que mon outils va utilisé pour installer les librairies manquantes.

 

Ainsi PIP vas vous installer la librairie Folium. A la façon des poupée russes, si une librairie à besoin d'une autre librairie pour fonctionné, c'est ce que l'on appelle des dépendances. Ainsi , PIP vas installez automatiquement tout ce qui vous manque (voir ci dessus l'illustartion).

![Installation de la librairie folium et de sa dépendance Jinja2 avec PIP lors du lancement du programme "Launcher.py"][31]Installation de la librairie folium et de sa dépendance Jinja2 avec PIP lors du lancement du programme "Launcher.py"

Windows va compiler les fichiers et créer des fichiers _peregrination.pyc_  et _Launcher.pyc _, pour que windows puisse utilisé mon programme.  
EN effet, windows et obligé de traduire mes fichier, écrit en langage "python" en fichier binaire (langage 0 et 1). Si vous cliquez sur ses fichiers, la même chose se produira. Ne cliquez pas sur le fichier peregrination. Ce dernier ne contient que les données.

![][32]

En raison d'un BUG que je dois encore déterminer la seule manière de faire fonctionner mon programme et la suivante :

![BUG ciblé][33]BUG ciblé

En raison d'un BUG que je dois encore déterminer la seule manière de faire fonctionner mon programme et la suivante :

1) clic-droit sur Launcher.py

 

2) cliquez sur "Edit with IDLE"

3) une fenêtre s'affiche, appuyer sur "F5" (ou "Run" > "Python Shell")

4) la console de IDLE ainsi que l'interfaçe graphique s'affiche, vous pouvez du coup utilisez mon programme

1. Télécharger le fichier ZIP
2. Extraire les fichiers du ZIP dans les dossiers de votre choix
3. Ouvrer une console (CTRL+ALT+T) et taper :

Vous pouvez aussi utilisé n'importe quelle environnement de développement (IDE) tel que IDLE, qui et naturellement fournis avec l'installation de Python, Spider, et tout autre programme supportant le langage python, en ouvrant le script Launcher.py et en exécutant le programme.

 

Note : Si vous avez installez la dernière version de Matplotlib (1.5.1) vous verrez apparaitre se message d'erreur, ceci n'est en rien un bug du programme mais une information indiquant pourquoi le programme sera long à charger:

    Warning (from warnings module):  
      File "/usr/local/lib/python2.7/dist-packages/matplotlib/font_manager.py", line 273  
        warnings.warn('Matplotlib is building the font cache using fc-list. This may take a moment.')  
    UserWarning: Matplotlib is building the font cache using fc-list. This may take a moment.

Cliquer sur le bouton "Charger le fichier d'ascendance"

Sélectionner votre fichier puis valider

![][34]

Cliquez sur le bouton "Charger le fichier de lieux"

Sélectionner votre fichier puis valider

![][35]

Cliquer sur le bouton "Options d'affichage" et coché les cases pour afficher les informations que vous souhaiter voir apparaitre sur les info-bulle de la carte

![][36]

Enfin généré votre carte  en appuyant sur le bouton "Créé la carte"

![][37]

  

![][38]

![][39]

  

Cliquer sur le bouton "Charger le fichier d'ascendance"

Sélectionner votre fichier puis valider

![][40]

Cliquez sur le bouton "Charger le fichier de lieux"

Sélectionner votre fichier puis valider

![][41]

Cliquer sur le bouton "Options d'affichage" et coché les cases pour afficher les informations que vous souhaiter voir apparaitre sur les info-bulle de la carte

![][42]

Enfin généré votre carte  en appuyant sur le bouton "Créé la carte"

![][43]

  

![][44]

![][45]

  

[1]: https://fr.wikipedia.org/wiki/Langage_de_programmation "https://fr.wikipedia.org/wiki/Langage_de_programmation"
[2]: https://fr.wikipedia.org/wiki/Interpr%C3%A8te_(informatique) "https://fr.wikipedia.org/wiki/Interpr%C3%A8te_(informatique)"
[3]: https://fr.wikipedia.org/wiki/Biblioth%C3%A8que_logicielle "https://fr.wikipedia.org/wiki/Biblioth%C3%A8que_logicielle"
[4]: https://docs.python.org/2/library/math.html "https://docs.python.org/2/library/math.html"
[5]: https://image.jimcdn.com/app/cms/image/transf/dimension=144x1024:format=jpg/path/s55280dc9b2bd5ac9/image/i540f2c8eb88001d4/version/1477258230/image.jpg
[6]: https://image.jimcdn.com/app/cms/image/transf/dimension=30x1024:format=png/path/s55280dc9b2bd5ac9/image/idff13891c64ded6b/version/1477258967/image.png
[7]: https://image.jimcdn.com/app/cms/image/transf/none/path/s55280dc9b2bd5ac9/image/i96f3a32c20990e38/version/1477258970/image.png
[8]: https://image.jimcdn.com/app/cms/image/transf/dimension=393x10000:format=png/path/s55280dc9b2bd5ac9/image/iebbf077e62d4a75e/version/1477231947/image.png
[9]: https://image.jimcdn.com/app/cms/image/transf/dimension=389x10000:format=png/path/s55280dc9b2bd5ac9/image/ib9fe9f3b6af8f028/version/1477231944/image.png
[10]: https://image.jimcdn.com/app/cms/image/transf/dimension=309x1024:format=png/path/s55280dc9b2bd5ac9/image/ieb4cb16b89d1dd78/version/1477266753/image.png
[11]: https://image.jimcdn.com/app/cms/image/transf/none/path/s55280dc9b2bd5ac9/image/ib03049230090baa6/version/1477268816/image.png
[12]: http://http/www.gadm.org/country "http:/www.gadm.org/country"
[13]: https://image.jimcdn.com/app/cms/image/transf/none/path/s55280dc9b2bd5ac9/image/i218bbb29cb72fcda/version/1477304927/image.png
[14]: https://image.jimcdn.com/app/cms/image/transf/dimension=1070x10000:format=png/path/s55280dc9b2bd5ac9/image/i87d2fb7aae60e7a0/version/1477335496/image.png
[15]: https://image.jimcdn.com/app/cms/image/transf/dimension=1070x10000:format=png/path/s55280dc9b2bd5ac9/image/i2867d9878915eddb/version/1477335756/image.png
[16]: https://image.jimcdn.com/app/cms/image/transf/dimension=1070x10000:format=png/path/s55280dc9b2bd5ac9/image/id7513bd4e9f949e8/version/1477335782/image.png
[17]: https://image.jimcdn.com/app/cms/image/transf/dimension=1070x10000:format=png/path/s55280dc9b2bd5ac9/image/i649281062ed8d379/version/1477335846/image.png
[18]: https://image.jimcdn.com/app/cms/image/transf/dimension=1070x10000:format=png/path/s55280dc9b2bd5ac9/image/i4f1285be88e3b8ef/version/1477336295/image.png
[19]: https://image.jimcdn.com/app/cms/image/transf/dimension=1070x10000:format=png/path/s55280dc9b2bd5ac9/image/i55be025b83c29b08/version/1477336350/image.png
[20]: https://image.jimcdn.com/app/cms/image/transf/dimension=1070x10000:format=png/path/s55280dc9b2bd5ac9/image/i936e7e4125a2ff44/version/1477337779/image.png
[21]: https://image.jimcdn.com/app/cms/image/transf/dimension=655x10000:format=png/path/s55280dc9b2bd5ac9/image/i0e6252aa2e25000e/version/1477337809/image.png
[22]: https://image.jimcdn.com/app/cms/image/transf/dimension=655x10000:format=png/path/s55280dc9b2bd5ac9/image/i4e495490970ce894/version/1477337806/image.png
[23]: https://image.jimcdn.com/app/cms/image/transf/dimension=655x10000:format=png/path/s55280dc9b2bd5ac9/image/i36529650bdcb9a5f/version/1477337801/image.png
[24]: https://image.jimcdn.com/app/cms/image/transf/dimension=655x10000:format=png/path/s55280dc9b2bd5ac9/image/i0b8021dcd8808dfc/version/1477338048/image.png
[25]: https://image.jimcdn.com/app/cms/image/transf/dimension=1070x10000:format=png/path/s55280dc9b2bd5ac9/image/i8f02d4dd557fbec1/version/1477344849/image.png
[26]: https://image.jimcdn.com/app/cms/image/transf/dimension=1070x10000:format=png/path/s55280dc9b2bd5ac9/image/if112262ae28df539/version/1477344949/image.png
[27]: https://image.jimcdn.com/app/cms/image/transf/dimension=1070x10000:format=png/path/s55280dc9b2bd5ac9/image/ibc245296f66540cf/version/1477344994/image.png
[28]: https://image.jimcdn.com/app/cms/image/transf/dimension=1070x10000:format=png/path/s55280dc9b2bd5ac9/image/i43db517208aeda2e/version/1477345052/image.png
[29]: https://image.jimcdn.com/app/cms/image/transf/none/path/s55280dc9b2bd5ac9/image/i41fca5dc7facc13f/version/1477671594/image.png
[30]: https://image.jimcdn.com/app/cms/image/transf/none/path/s55280dc9b2bd5ac9/image/i977751a5e3b2c001/version/1477671621/image.png
[31]: https://image.jimcdn.com/app/cms/image/transf/none/path/s55280dc9b2bd5ac9/image/i2f8e71564a4f5128/version/1477762646/image.png
[32]: https://image.jimcdn.com/app/cms/image/transf/none/path/s55280dc9b2bd5ac9/image/ic86fb501f8906bee/version/1477763221/image.png
[33]: https://image.jimcdn.com/app/cms/image/transf/none/path/s55280dc9b2bd5ac9/image/i500513555b96027d/version/1477764395/image.png
[34]: https://image.jimcdn.com/app/cms/image/transf/none/path/s55280dc9b2bd5ac9/image/i3fec8d231f1481d7/version/1477571073/image.png
[35]: https://image.jimcdn.com/app/cms/image/transf/none/path/s55280dc9b2bd5ac9/image/ibfcd08bd2a8649b0/version/1477571114/image.png
[36]: https://image.jimcdn.com/app/cms/image/transf/none/path/s55280dc9b2bd5ac9/image/ia0f571d1b0ce1e62/version/1477571192/image.png
[37]: https://image.jimcdn.com/app/cms/image/transf/none/path/s55280dc9b2bd5ac9/image/ie3375937f6e3d8e2/version/1477571223/image.png
[38]: https://image.jimcdn.com/app/cms/image/transf/dimension=519x10000:format=png/path/s55280dc9b2bd5ac9/image/i176c1ea0365bb4b3/version/1477679780/image.png
[39]: https://image.jimcdn.com/app/cms/image/transf/dimension=519x10000:format=png/path/s55280dc9b2bd5ac9/image/i0672e4c23a8f9ad3/version/1477680894/image.png
[40]: https://image.jimcdn.com/app/cms/image/transf/none/path/s55280dc9b2bd5ac9/image/i474da8c8e06f734b/version/1477576163/image.png
[41]: https://image.jimcdn.com/app/cms/image/transf/none/path/s55280dc9b2bd5ac9/image/i5f001c3be11aa990/version/1477575992/image.png
[42]: https://image.jimcdn.com/app/cms/image/transf/none/path/s55280dc9b2bd5ac9/image/ie3492d5810e37c41/version/1477575993/image.png
[43]: https://image.jimcdn.com/app/cms/image/transf/none/path/s55280dc9b2bd5ac9/image/i3ab2838f184c5c29/version/1477575993/image.png
[44]: https://image.jimcdn.com/app/cms/image/transf/dimension=519x10000:format=png/path/s55280dc9b2bd5ac9/image/i524832663aae7cce/version/1477680522/image.png
[45]: https://image.jimcdn.com/app/cms/image/transf/dimension=519x10000:format=png/path/s55280dc9b2bd5ac9/image/i28e602494db37d92/version/1477680520/image.png
