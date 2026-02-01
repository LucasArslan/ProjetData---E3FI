# ImmoViz France 

### Objectif
L'objectif de ce projet est d'analyser le marché immobilier français en 2023 à travers les données officielles des Demandes de Valeurs Foncières (DVF). Il permet de visualiser les différences de prix au m², la répartition des types de biens et les dynamiques de vente à l'échelle départementale et communale via un dashboard interactif.

### User Guide
1. **Clonez le dépôt** : `$ git clone https://github.com/LucasArslan/ProjetData-Lucas-Noah`
2. **Déplacez-vous dans le dossier** : `$ cd Projet-data`
3. **Installez les modules nécessaires** : `$ pip install -r requirements.txt`
4. **Préparez les données** (téléchargement et nettoyage) : 
    * `$ python src/utils/get_data.py`
    * `$ python src/utils/get_geo.py`
    * `$ python src/utils/clean_data.py`
5. **Exécutez l'application** : `$ python main.py`
6. **Accédez au dashboard** en ouvrant votre navigateur à l’adresse : `http://127.0.0.1:8050/`

### Data
Les données utilisées proviennent de sources officielles ouvertes (Etalab) :
* **Transactions immobilières (DVF 2023)** : Détail des ventes, prix, surfaces et types de biens. [Lien data.gouv.fr](https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres/)
* **Contours administratifs** : Fichier GeoJSON pour la délimitation géographique des communes françaises. [Lien Etalab](https://etalab-datasets.geo.data.gouv.fr/contours-administratifs/2024/geojson/communes-100m.geojson)

### Developer Guide

**Structure du Projet :**
* **main.py** : Point d'entrée de l'application Dash gérant les callbacks et le serveur.
* **requirements.txt** : Liste des dépendances (Dash, Pandas, Plotly, etc.).
* **data/** : Répertoire contenant les fichiers CSV et GeoJSON (bruts et nettoyés).
* **src/utils/** : Fonctions de traitement de données.
    * `get_data.py` / `get_geo.py` : Scripts de récupération automatisée.
    * `clean_data.py` : Pipeline de nettoyage et formatage des types de données.
* **src/components/** :
    * `layout.py` : Définition de la structure de l'interface (Sidebar et zone d'affichage).

**Modifications possibles :**
* **Ajouter un graphique** : Déclarer un nouveau `dcc.Graph` dans `layout.py` et mettre à jour la liste des `Output` dans le callback `update_dashboard` de `main.py`.
* **Changer les filtres** : Ajouter un composant de saisie dans la sidebar de `layout.py` et l'inclure comme `State` ou `Input` dans `main.py`.

### Rapport d'analyse

En cartographiant les prix de l'immobilier, nous constatons que le marché français est marqué par une **disparité géographique majeure**. L'analyse révèle une concentration extrême des prix élevés en Île-de-France, particulièrement dans Paris intra-muros (6e, 7e, 8e arrondissements) où les prix dépassent régulièrement les 10 000 €/m². À l'inverse, les zones rurales affichent une accessibilité nettement supérieure avec des prix souvent inférieurs à 2 000 €/m².

L'étude des types de biens montre une **spécialisation territoriale** : les appartements dominent les transactions dans les grandes métropoles, tandis que les maisons individuelles constituent l'essentiel du volume en zones périurbaines et rurales. Sur l'année 2023, nous observons une saisonnalité avec un pic de transactions durant le printemps (avril-juin), période traditionnellement active pour les déménagements estivaux.

**Conclusions générales :**
Le marché immobilier français en 2023 reste très polarisé autour des grands centres urbains et du littoral. 

Initialement, ce projet visait à analyser l'évolution des prix sur une période de 2 à 3 ans. Cependant, face au volume massif des données DVF et aux contraintes de performance (temps de traitement et latence d'affichage du dashboard), nous avons fait le choix technique de nous concentrer exclusivement sur l'année 2023 afin de garantir une expérience utilisateur fluide et une analyse précise.

### Copyrights

Nous déclarons sur l’honneur que la majeure partie de ce projet (architecture logicielle, pipeline de traitement des données et logique métier) a été conçue et réalisée par nous-mêmes. 

Pour la mise en œuvre technique, nous nous sommes appuyés sur la documentation officielle de Plotly/Dash. L'utilisation de ChatGPT est intervenue de manière ponctuelle pour nous débloquer sur des problématiques spécifiques, notamment la gestion de l'affichage cartographique des arrondissements de Paris, Lyon et Marseille (PLM), ainsi que pour certains ajustements esthétiques du fichier CSS. 

**Projet réalisé par Arslan Lucas & Binetruy Noah**