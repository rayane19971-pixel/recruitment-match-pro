# Recruitment Match PRO

Application web de scouting et d'analyse de données pour le football professionnel.

Le projet permet de rechercher des joueurs des 5 grands championnats européens (saison 2024-2025), de comparer leurs statistiques avec des graphiques en radar et de trouver des profils similaires via un algorithme KNN.

## Contenu du dépôt

- `backend/` : API Python avec FastAPI, SQLite et scripts de données.
- `Frontend/` : Application React avec Vite et CSS personnalisé.

## Démarrage en local

1. **Lancer le backend** :
   ```bash
   cd backend
   pip install -r requirements.txt
   python main.py
   ```

2. **Lancer le frontend** :
   ```bash
   cd Frontend
   npm install
   npm run dev
   ```

## Version en ligne
Le site est déployé sur Vercel :
https://recruitment-match-pro.vercel.app

## Fonctionnalités
- Moteur de recherche et filtres multicritères (poste, âge, valeur max, note).
- Radar de performance à 6 axes (Finition, Dribble, Passes, Vitesse, Défense, Physique).
- Recherche de jumeaux statistiques (KNN).
- Espace Direction Sportive avec budget mercato et simulateur de transfert.

## Auteur
Rayane Ourad
