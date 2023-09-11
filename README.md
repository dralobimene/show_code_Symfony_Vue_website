2023-09-11
README.md

FRENCH:
Présente une partie du projet pour la certification CDA.
Le projet de la certification CDA est articulé comme suit
- 1 site web qui permet de publier des commentaires au sijet d'1 jeu crée en python.
  Le site utilise 3 technos:
    php, symfony pour les controllers qui traitent du json
    vite et vue pour l'affichage
    mongoDB pour la ... base de données.
- 1 moteur de jeu et 1 client lourd en python. Il est possible depuis le client lourd de se connecter à la mongoDB pour publier un commentaire. On peut jouer au jeu en monoplayer, local.
- 1 serveur TS (Node) qui permet de jouer en multiplayer (direct live), d'ou la presence ds la dump "test_perso_04" d'1 table "game" parce qu'il fallait enregistrer les fichiers json descriptifs des étages du donjon pour ensuite les partager entre les joueurs.


Dépôt qui contient
- 1 partie des fichiers Symfony (rep backend)
  Principalement:
    Le dossier src:
      src/Controller
      src/Document (les entités mais norme MongoDB)
      src/EventListener
      src/Repository
      src/Service
    Le dossier templates (qui ne sert pas a grd-chose étant donné qu'on utilise des "views").
    :es dossiers tests et translations ne servent à rien ici.
- 1 partie des fichiers Vue (rep frontend)
  Principalement:
    Le dossier src:
      src/assets
      src/components
      src/router
      src/views
      Des fichiers de configuration.
- 1 dump de la base de données MongoDB (rep test_perso_04)

Le projet tel quel ne fonctionnera pas si vous télécharez ces fichiers. Ce dépôt ne sert que de "vitrine" pour montrer 1 (petite partie de ce que j'ai fait pour la certif de la formation CDA).
Un second upload va voir le jour dans la journée (principalement du python et un peu de TS pour le serveur).
