# Test_distrib 
Ce logiciel est un outil de comparaison de page de site web. Deux pages sont 
chargées dans une base de données et sont affichées côte à côte. L'utilisateur
peut ensuite utiliser un outil de comparaison (usersnap ou autre) avant de valider
l'état du site et de passer à la paire de pages suivante.

# Utilisation
## Récupération du dépôt
On récupère le dépôt avec:
```
git@github.com:epfl-sdf/test4wwp_distrib.git
```
(cette commande nécessite la présence de `git` sur l'ordinateur)

Pour executer les commandes des sections suivantes, il faut se mettre dans
le dossier du dépôt.

## Installation des outils nécessaires
Simplement avec la commande:
```
./install.sh
```

Pour que cette commande marche, il faut être sous Ubuntu ou une autre
distribution Linux utilisant `apt-get` comme gestionnaire de paquets et qui a les
mêmes noms de packets que sur les dépôts Ubuntu.

## Préparation
Simplement avec la commande:
```
./loadDB.sh
```

Avant de lancer `./start.sh`, il faut mettre user.csv et credentials.csv dans un
dossier credentials/ au même niveau que le dossier du dépôt.
Afin de populer la base de donnée, il faut faire `./loadDB.sh` dans le dossier dépôt.

## Lancement du serveur
Simplement avec la commande:
```
./start.sh
```

`start.sh` est un script qui lance un serveur python sur le port 8081. Pour s'y 
connecter, il suffit d'entrer l'url [ip]:8081 où ip est l'adresse ip de la machine 
depuis laquelle est lancé le serveur.

Les pages suivantes sont disponibles:

- /index:
page sur laquelle l'utilisateur peut sélectionner son nom afin de commencer les tests
- /logs:
page sur laquelle se trouve les logs des connexions qui ont été faites sur le serveurs
- /assigned:
page permettant de gérér la distribution des sites webs.
- /compare:
page donnée à l'utilisateur après qu'il se soit identifier sur /index.
Elle permet de comparer deux sites webs et de donner leur états. 

# Explication logiciel
`./start.sh` lance la commande python code.py 8081. code.py est le code du serveur.
Code.py


Dans le dossier Templates/ se trouve le code html des pages web. 
Si l'utilisateur accède  une url précise, le templates html correspondant
 lui sera envoyé et les instructions dans la classe correspondante à l'url seront executées.
Par exemple si l'utilisateur se connecte à l'url index, une requête sera envoyée
au serveur. Se dernier executera le code de la classe index dans code.py qui retournera
le template index.
La liste des urls disponibles se trouve dans un dictionnaire en tête de code.py.
Chaque page a sa propre class dans code.py qui permet d'effectuer des actions désirées 
en fonction de la page. 
Par exemple la class next correspond à l'url /next permet de mettre à jour les informations
de la database tel que logs et assigned\_websites.

`./loadDB.sh` lance plusieurs sous commandes:
- `python export_logs.py` qui exporte les logs de la database (si déjà existante)
- `sqlite3 distrib.db < create_table.sql` qui créée la database
- `python fillDB.py` qui popule les tables users et websites de la database

`python export_logs.py` permet d'exporter les logs de la database.
Il le fait dans un fichier logs-DATE.csv et dans distrib.log. Cette commande
est appelé chaque heure par `./start.sh` et permet d'avoir un backup des logs.

# La database
La database comporte 5 tables:
- `users (id, first_name, last_name)`
dont la clef primaire est id
- `websites (id, name, jahia, wordpress, userview, userpwd, random)`
dont la clef primaire est id
- `browsers (id, name, version, os)`
dont la clef primaire est id
- `assigned_websites (user_id, browser_id, website_id)`
dont la clef primaire est la combinaison `(user_id, browser_id et website_id)`
- `logs (user_id, browser_id, website_id, date, status)`
dont la clef primaire est la combinaison `(user_id, browser_id, website_id et date)`

Le fonctionnement général est le suivant:

Lorsqu'un utilisateur s'identifie sur /index, son id et l'id de son navigateur sont 
envoyé au serveur. Celui-ci envoit un requête SQL au serveur pour voir :
- Si un site web lui a été assigné dans `assigned_websites`
- S'il n'avait pas terminé un site qu'il avait commencé à tester (via logs)
- S'il reste des sites disponibles à tester (via logs).

Lorsqu'il presse sur suivant, le serveur supprime l'entrée correspondante dans 
assigned\_websites (si présente) et ajoute l'état du site dans logs.
L'utilisateur peut continuer jusqu'à ce que tout les sites aient été testés pour 
ce navigateur (grâce à logs).

