
[Source](https://peregrination.jimdo.com/utilisation/ "Permalink to Utilisation - Pérégrination : Cartographie généalogique")

# Utilisation - Pérégrination : Cartographie généalogique

![][1]

&nbsp; 

Pérégrination a été testé pour le moment avec des fichiers GEDCOM issus de Hérédis. Toutefois, rien n'exclut le fait que des GEDCOMs d'autre logiciel peuvent fonctionner. Aussi, il est important que les lieux soient correctement formatés de manière à reconnaître chacune des parties administratives. Sans quoi, il sera impossible pour mon logiciel de géolocalisé les lieux. 

Le format du fichier doit être au format ANSI et non UTF8 de manière à ce que les caractères accentués puissent être encodés correctement. 

&nbsp; 

![][2]

![][3]

Pérégrination procède en 4 étapes : 

1. Lecture du fichier GEDCOM avec gedcompy 
2. Extraction de tout les individus 
3. Extraction de toute les familles 
4. Extraction de tout les lieux 

Une fois terminé, un message apparat avec le temps calculé 

  

![][4]

&nbsp; 

La seconde étape consiste à renseigner le type administratif de chaque localité. 

Une fenêtre affiche les 10 premières localités où les différents champs apparaissent dans les différentes colonnes. 

Pérégrination s'adapte à n'importe quelle situation, il affichera autant de colonnes qu'il y a de subdivisions. 

Une étiquette affiche alors l'ordre par défaut. Si ce dernier n'est pas bon, vous pouvez les modifier via les panneaux déroulants. 

&nbsp; 

![][5]

Vous avez le choix avec : 

* &nbsp;"Commune" 
* "Code Postal" 
* "Departement" 
* "Region" 
* "Pays" 
* "Subdivision" 
* "Ignorer" 

(Pour des raisons de compatibilité d'encodage des caractères j'ai omis les accents) 

  

![][6]

&nbsp; 

Une fois vos choix enregistrer, une étiquette s'affiche sous les menus déroulant avec la sélection que vous avez validé. Vous pouvez à tout moment changer vos choix. Une fois que tout est vérifié, vous pouvez cliquez sur "Valider" 

Si vous cliquez sur le bouton "Quitter" , vous quitterais la fenêtre du gestionnaire. L'étape n° 3 restera inactive. 

&nbsp; 

![][7]

Ce message s'affiche ensuite pour valider définitivement vos choix. &nbsp;Ceci active le bouton pour l'étape n° 3. Si vous cliquez sur "Non" vous reviendrez sur le gestionnaire des subdivision. 

&nbsp; 

C'est le **cœur**&nbsp;du programme, c'est lui qui va déterminé automatiquement les coordonnées GPS de chacun de vos lieux. Plusieurs options sont disponible comme l'utilisation de clé API GoogleMap disponible dans le programme ou via votre propre clé API GoogleMap Geocoding 

&nbsp; 

Pour gagner un temps précieux, Pérégrination permet de charger un fichier de Lieux qu'il à lui même déjà créé auparavant, et éviter de recommencer la recherche des lieux. Après avoir cliquez sur "Etape 3: Recherche des coordonnées GPS", ce message apparaît : 

&nbsp; 

&nbsp; 

![][8]

&nbsp; 

Si vous avez cliqué sur "Oui", une boite de dialogue apparaît et vous aide à parcourir dans vos dossiers pour retrouver le fichier CSV. Par défaut , le dossier et celui ou le programme se trouve. Néanmoins il garde en mémoire l'emplacement du dernier fichier ouvert (même après fermeture du programme).

&nbsp; 

![][9]

![][10]

  

&nbsp; 

Un fichier de Lieux et un fichier CSV (séparateur virgule) contenant : 

&nbsp; 

1. La première colonne pour les noms des lieux du GEDCOM 
2. Les Latitudes 
3. Les Longitudes 

[ ![Aperçues avec Notepad ++ , les CSV sont des fichiers séparés par des virgules \("comma" en anglais\), les guillemets anglais \("\) permettent d'éviter de prendre les virgules qui séparent les subdivisions des lieux de la première colonne][11]][12]

[ ![Aperçue avec OpenOfficeCalc][13]][12]

&nbsp; 

Une fois que les lieux sont chargé, le bouton pour l'étape n° 4 s'active. 

&nbsp; 

&nbsp; 

Vous avez cliquez sur "Non" car c'est la première fois que vous allez géolocalisé les lieux de votre fichier GEDCOM. Pérégrination est compatible avec la technologie de Google Map, et vous propose d'utilisé ce que l'ont appelle les clefs API. 

&nbsp; 

![][14]

&nbsp; 

Une clef API et une chaîne de caractère, comme un mot de passe, permettant de vous identifier pour accéder au serveur de Google (ici Google Map) de manière à ce que vous puissiez profiter de toute la puissance de calcul de leur serveur. 

&nbsp; 

&nbsp; 

![][15]

&nbsp; 

&nbsp; 

Depuis le 26 Octobre 2011, à cause du besoin grandissant des utilisateurs de Google à utilisé ses&nbsp;services,&nbsp;le&nbsp;service de géocodage Google Map et devenus limité (2500 reqêtes par jour). 

&nbsp; 

![Liste des différents services pour les APIs de Google Maps][16]Liste des différents services pour les APIs de Google Maps

&nbsp; 

&nbsp; 

Pérégrination utilise les lieux tel qu'ils sont définis dans le GEDCOM. Si dans votre arbre généalogique vous ajouté les subdivision du lieux pour un événement donné (hameau, lieux-dit, rue, localité, emplacement...) ceci sera inscrit dans le GEDCOM comme un lieu à part entière. 

&nbsp; 

Ainsi &nbsp;: 

_Roubaix, 59100, Nord, France_&nbsp; ET&nbsp;_Roubaix, 59100, Nord, France, Rue de l'Epeule_

seront considéré comme 2&nbsp;lieux différents, même si dans votre logiciel de généalogie, il les considérera comme 1 

&nbsp;seul et unique lieu. 

&nbsp; 

Or si vous avez 2500 Lieux différents, il faut savoir que Pérégrination utilise 6 combinaison d'orthographe différente des subdivision du lieux en cas d'échec de géolocalisation. Il se peut donc qu'il 

&nbsp; 

Pour géolocalisé un grand nombre de lieux (supérieur à 2000) Vous avez deux solution : 

&nbsp; 

1. Souscrire à une clef API payante, il existe des clef API pour 5000 a mais pas de panique, Pérégrination peut réussir à récupéré les coordonnées sans API, mais si cela dépasse plusieurs centaine de requête, cela peut signaler votre adresse IP aux serveur de google et bloqué l'accès au info sur GoogleMap (détection de Robots) 

&nbsp; 

Vous avez cliquez sur "Oui", dans ce cas Pérégrination affiche une fenêtre pour vous permettre de mettre votre propre clef API Google Map 

![][17]

Copier votre clef API (CTRL+C) puis cliquez dans la case blanche pour placer votre curseur et coller la clef (CTRL+V) ensuite appuyeZ sur le bouton "Valider". 

* Si la case et vide ce message d'erreur apparaîtra, vous retournerais directement sur CETTE FENËTRE. 
* Si le champ et bien rempli, un message apparaîtra pour valider votre choix. 
*     * Cliquez sur "Oui" pour valider pour enregistré votre clef. 
    * En cas d'erreur, vous pouvez cliquez sur "Non", vous reviendrais sur la fenêtre pour corrigé votre erreur. 

_Note : Cas particulier, si vous validé une clef API qui n'est pas bonne ou mal orthographié, la clef API ne fonctionnera pas lors du géocodage, et sera remplacer par l'une des 40 APIs disponibles dans le code source du programme._

![][18]

![][19]

  

Si vous avez cliquez sur "Non" un autre message apparaît : 

![][20]

Lorsque vous cliquez sur "Oui", Pérégrination vous ouvre automatiquement 3 fenêtres via votre navigateur par défault, pour vous permettre de créé : 

1. [Un compte Gmail][21]
2. [De lire la documentation concernant les clé API de Google Map][22]
3. [ De créé un projet et une clef API Google Map via la "Console des API Google"][23]

Une fois que vous avez votre clef API, vous pouvez la copier coller dans la fenêtre [(voir Clef API Google Map - OUI :)][24]

&nbsp; 

&nbsp; 

Vous avez cliquez sur "Non", un nouveau message apparaît vous informant que vous allais être redirigé pour enregistré le fichier CSV. 

&nbsp; 

![][25]

&nbsp; 

Dans la boite de dialogue écrivez le nom du fichier que vous souhaiter donner au fichier de Lieux, les résultat du géocodage seront automatiquement sauvegarder dans ce fichier, que vous pourrais utilisé lors de prochaine réalisations. Si vous cliquez sur annuler vous reviendrez sur la fenêtre de Pérégrination, sinon le géocodage se met en marche. 

. 

![][26]

Tout ce fait de manière automatisé, vous n'avez plus qu'as patienté... 

![][27]

&nbsp; 

Voici comment procède pérégrination dans son analyse des lieux : 

&nbsp; 

&nbsp; 

![Diagramme des différentes composition d'adresse effectué par Pérégrination][28]Diagramme des différentes composition d'adresse effectué par Pérégrination

&nbsp; 

Pour évité toute mauvaise surprise, car la géolocalisation n'est pas une science exacte, Pérégrination est doté d'un visualiseur. Chaque couple de coordonnées (Latitudes et Longitudes) vont être groupé avec leur lieux correspondants. Ainsi si un lieu A et un lieu B ont les même coordonnées, ils seront regroupé ensemble. 

&nbsp; 

![][29]

&nbsp; 

Ensuite ont télécharges les images de OpenStreetMap pour chacune des coordonnées retrouvé, de manière à se que l'ont puisse visualisé sur une carte vers quoi les coordonnées pointes. 

&nbsp; 

&nbsp; 

![Téléchargement des images correspondant à chaque couple de coordonnées GPS : Ici La Bassée, avec un regroupement de trois subdivision différentes][30]Téléchargement des images correspondant à chaque couple de coordonnées GPS : Ici La Bassée, avec un regroupement de trois subdivision différentes

&nbsp; 

Enfin, &nbsp;effet, malgré toutes les méthodes mises en œuvre pour vérifier chaque résultat durant la recherche des coordonnées, nous sommes jamais à l'abri d'une erreur, surtout si les lieux rechercher sont orthographié selon leurs anciennes orthographes ou parce que ces derniers ont changé de nom, fusionné, divisé ou disparu. 

&nbsp; 

![][31]

&nbsp; 

Une fois les lieux géolocalisé, le visualiseur s'ouvre. 

* Les différents lieux correspondants aux mêmes coordonnée retrouvé sont situé dans un cadre après le titre 
* L'image de la carte avec un point coloré central qui situe l'emplacement exact des coordonnées 
* La carte permet d'accéder directement à la position GPS sur Google Map via votre navigateur par défaut 
* Le panneau de Control sur la droite: 
*     * Avec le numéro du lieux 
    * Les touches directionnelles: 
    *         * "&gt;" pour aller à l'image suivante 
        * "&lt;" pour revenir à l'image précédente 
        * "+" pour accéder a la position GPS sur une carte Google Map &nbsp;via votre navigateur par défaut 
        * suivis par les étiquette indiquant les coordonnées Latitude et Longitude du lieu 
* Les champs pour modifier les coordonnées: 
*     * Champs "Latitude" et "Longitude" : 
    *         * Il y à un contrôle des caractère, si il y a la présence d'un autre caractère que : "+-1234567890.", la chaîne de caractère sera automatiquement refusé 
    * Bouton "Mettre à jour les coordonnées GPS pour ce lieux": 
    *         * Les coordonnées sont automatiquement changé dans le fichier CSV ainsi que dans les donnée en mémoire 
        * La carte est télécharger de nouveau et réactualisé dans la fenêtre 
* Bouton "Quitter" qui ferme automatiquement la fenêtre et active le bouton pour l'étape n°4 

![][32]

&nbsp; 

* Il s'agit d'un simple moteur de recherche, inscrive n'importe quelle chaîne de caractère (avec ou sans accent avec ou sans majuscules, mixte,...) il vous trouvera tout les individu qui possèdent cette chaîne de caractère dans leur Nom et Prénoms, choisissez soit l'ascendance, ou la descendance et validez. 
* Si vous cliquez sur "Quitter" vous reviendrais au départ, cliquez sur "Validez" et le bouton de l'étape 5 s'activera. 
* Si vous ne sélectionné pas de personnes ni de sens de direction (Ascendance/Descendance vous aurai un message d'erreur 

![][33]

&nbsp; 

Suivent les options d'affichage, ils s'agit des données que vous souhaiterais voir apparaître dans les fenêtres Pop-up de la carte lorsque vous cliquez sur une trajectoire, ou sur le repère d'une ville. 

* "Nombre de °,x,+" affiche le nombre de Naissance de Décès et de Mariage qui s'est produit dans le lieu 
* "Nombre total d'événement" : Affiche la somme de tout les événement de la ville (Naissance, mariage, décès ...) 
* "Départ(s)" : Indique les individus qui sont partie, ayant eu une descendance dans un lieu différent que leur lieu de naissance 
* "Arrivée(s)" : Indique les individus qui sont arrivé, ayant une ville de naissance différente de celle de leur enfant 
* "Nom(s)" : Liste des patronyme ayant eu un événement avec ce lieu 
* "Date extrêmes" : Comme écrit, il d'agit d'afficher la date du plus ancien et du plus récent événement produit dans cette localité 
* "Valider" : Valide la sélection 

![][34]

Pour utilisé ces option vous devez préalablement télécharger les fichier SHAPEFILE correspondant au différents pays des villes géolocalisé 

&nbsp; 

Attention ! Plus la généalogie contiendra d'individu, en fonction du nombre d'options que vous avez choisis de faire afficher, les bulles seront proportionnellement rempli en fonction du niveau géographique du regroupement, ^référer un regroupement par commune si les adresse sont nombreuse, et les individu peu nombreux, un regroupement par département, si les individu ne sont pas concentré etc... Toutes les combinaison sont possible. 

&nbsp; 

![][35]

&nbsp; 

Si vous cliquez sur "Passer" L'ascendance (ou la descendance) du personnage choisis et créé et la carte et réalisé sous la forme d'un fichier HTML dans vos dossier. Deux modèle de carte sont créé, un modèle type "Relief" et un modèle type "Routier", ses deux dernier se complémentent l'une étant plus détaillé que l'autre. 

![][36]

[1]: https://image.jimcdn.com/app/cms/image/transf/none/path/s55280dc9b2bd5ac9/image/i2bdb5331006c5827/version/1489019269/image.png
[2]: https://image.jimcdn.com/app/cms/image/transf/none/path/s55280dc9b2bd5ac9/image/i40efa48d2602ff5e/version/1489056300/image.png
[3]: https://image.jimcdn.com/app/cms/image/transf/none/path/s55280dc9b2bd5ac9/image/i335618a063835e79/version/1489087734/image.png
[4]: https://image.jimcdn.com/app/cms/image/transf/none/path/s55280dc9b2bd5ac9/image/i4059ae8a011edfe3/version/1489056473/image.png
[5]: https://image.jimcdn.com/app/cms/image/transf/none/path/s55280dc9b2bd5ac9/image/i303b5294bc6f0f27/version/1489057089/image.png
[6]: https://image.jimcdn.com/app/cms/image/transf/none/path/s55280dc9b2bd5ac9/image/ibf93e8f609ba898d/version/1489078184/image.png
[7]: https://image.jimcdn.com/app/cms/image/transf/none/path/s55280dc9b2bd5ac9/image/ib97c72f0acf9ed27/version/1489027405/image.png
[8]: https://image.jimcdn.com/app/cms/image/transf/none/path/s55280dc9b2bd5ac9/image/if013fd33ba1a65ca/version/1489025303/image.png
[9]: https://image.jimcdn.com/app/cms/image/transf/none/path/s55280dc9b2bd5ac9/image/ia3f20bf3ef2dc224/version/1489027435/image.png
[10]: https://image.jimcdn.com/app/cms/image/transf/none/path/s55280dc9b2bd5ac9/image/i8557bf37bacaac5d/version/1489025790/image.png
[11]: https://image.jimcdn.com/app/cms/image/transf/dimension=1920x400:format=png/path/s55280dc9b2bd5ac9/image/i900948ebbd98f107/version/1489058809/image.png
[12]: javascript:
[13]: https://image.jimcdn.com/app/cms/image/transf/dimension=1920x400:format=png/path/s55280dc9b2bd5ac9/image/i4d95afcfcb3cf684/version/1489058636/image.png
[14]: https://image.jimcdn.com/app/cms/image/transf/none/path/s55280dc9b2bd5ac9/image/i4ae3731c84898cef/version/1489093642/image.png
[15]: https://image.jimcdn.com/app/cms/image/transf/none/path/s55280dc9b2bd5ac9/image/ia8eafd7dbf53ef7d/version/1489077881/image.png
[16]: https://image.jimcdn.com/app/cms/image/transf/none/path/s55280dc9b2bd5ac9/image/i1a9d3fd98b1e50b9/version/1489078970/image.png
[17]: https://image.jimcdn.com/app/cms/image/transf/none/path/s55280dc9b2bd5ac9/image/i6262964d489342f2/version/1489066507/image.png
[18]: https://image.jimcdn.com/app/cms/image/transf/none/path/s55280dc9b2bd5ac9/image/ib544d99f6b1fa684/version/1489067137/image.png
[19]: https://image.jimcdn.com/app/cms/image/transf/dimension=334x10000:format=png/path/s55280dc9b2bd5ac9/image/ic262dd88c959b9c4/version/1489094918/image.png
[20]: https://image.jimcdn.com/app/cms/image/transf/dimension=461x10000:format=png/path/s55280dc9b2bd5ac9/image/i1ce4deb04cfc3aa4/version/1489094895/image.png
[21]: https://accounts.google.com/SignUp?service=mail&amp;continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&lt;mpl=default "https://accounts.google.com/SignUp?service=mail&amp;continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&lt;mpl=default"
[22]: https://developers.google.com/maps/documentation/geocoding/get-api-key?hl=fr "https://developers.google.com/maps/documentation/geocoding/get-api-key?hl=fr"
[23]: https://www.google.fr/url?sa=t&amp;rct=j&amp;q=&amp;esrc=s&amp;source=web&amp;cd=1&amp;cad=rja&amp;uact=8&amp;ved=0ahUKEwj-kf6G0MnSAhWE0RoKHQ9UDyMQFggaMAA&amp;url=https%3A%2F%2Fconsole.developers.google.com%2F%3Fhl%3DFR&amp;usg=AFQjCNF-vbOpRiGCi4cKnLe84p-p_faf3w&amp;sig2=-0S533HZJ9TfcEQz-Lwq2Q&amp;bvm=bv.149093890,d.d2s "https://www.google.fr/url?sa=t&amp;rct=j&amp;q=&amp;esrc=s&amp;source=web&amp;cd=1&amp;cad=rja&amp;uact=8&amp;ved=0ahUKEwj-kf6G0MnSAhWE0RoKHQ9UDyMQFggaMAA&amp;url=https%3A%2F%2Fconsole.developers.google.com%2F%3Fhl%3DFR&amp;usg=AFQjCNF-vbOpRiGCi4cKnLe84p-p_faf3w&amp;sig2=-0S533HZJ9TfcEQz-Lwq2Q&amp;bvm=bv.149093890,d.d2s"
[24]: https://peregrination.jimdo.com/utilisation/#api_yes "https://peregrination.jimdo.com/utilisation/#api_yes"
[25]: https://image.jimcdn.com/app/cms/image/transf/none/path/s55280dc9b2bd5ac9/image/ib73de96f20a441c1/version/1489098180/image.png
[26]: https://image.jimcdn.com/app/cms/image/transf/dimension=570x10000:format=png/path/s55280dc9b2bd5ac9/image/i112cfaea40500542/version/1489098520/image.png
[27]: https://image.jimcdn.com/app/cms/image/transf/dimension=704x10000:format=png/path/s55280dc9b2bd5ac9/image/i743d15b79631aba2/version/1489117304/image.png
[28]: https://image.jimcdn.com/app/cms/image/transf/dimension=573x10000:format=png/path/s55280dc9b2bd5ac9/image/i1c08c3697796871a/version/1489115573/image.png
[29]: https://image.jimcdn.com/app/cms/image/transf/none/path/s55280dc9b2bd5ac9/image/i8d57ce202124a2b0/version/1489117367/image.png
[30]: https://image.jimcdn.com/app/cms/image/transf/none/path/s55280dc9b2bd5ac9/image/i3a744a0318705b1f/version/1489118149/image.png
[31]: https://image.jimcdn.com/app/cms/image/transf/none/path/s55280dc9b2bd5ac9/image/ifc690f974dcdae4f/version/1489118340/image.png
[32]: https://image.jimcdn.com/app/cms/image/transf/none/path/s55280dc9b2bd5ac9/image/i75b26c3c9dee287e/version/1489120157/image.png
[33]: https://image.jimcdn.com/app/cms/image/transf/none/path/s55280dc9b2bd5ac9/image/if0b342b59b70babc/version/1489119205/image.png
[34]: https://image.jimcdn.com/app/cms/image/transf/none/path/s55280dc9b2bd5ac9/image/if1282a653a786810/version/1489121115/image.png
[35]: https://image.jimcdn.com/app/cms/image/transf/none/path/s55280dc9b2bd5ac9/image/id7b83a03c8ef6c5b/version/1489121811/image.png
[36]: https://image.jimcdn.com/app/cms/image/transf/dimension=1070x10000:format=png/path/s55280dc9b2bd5ac9/image/idbd3050a94865f88/version/1489122111/image.png

  
