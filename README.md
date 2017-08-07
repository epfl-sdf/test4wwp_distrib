# test4wwp distrib
Distributeur de tâches pour la comparaison visuelle de deux pages web pour le projet test4wwp

Pages disponibles: 

"/" - Page d'accueil.

"/logs" - Affiche l'historique des visites et comparaisons.

"/compare" - Permet de comparer deux urls passées en argument dans url1 et url2. Il est conseillé de ne pas l'utiliser avec l'argument id autre qu'en suivant les boutons disponibles.

### Installation:
**``./install.sh``**
Nécessite aussi la présence des fichiers credentials.csv et users.csv dans le dossier credentials situé dans le répertoire au-dessus.

Une fois ces fichiers en place, exécuter **``./loadDB.sh``** pour (ré)initialiser la base de données.

### Utilisation:
**``./start.sh``**
