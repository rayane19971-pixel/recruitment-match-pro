# Recruitment Match PRO ⚽

Plateforme SaaS de Data Intelligence et Scouting Professionnel pour le football.

L'application permet d'analyser les performances des joueurs professionnels issus des 5 grands championnats européens (saison 2024-2025), d'effectuer des recherches de profils similaires via l'algorithme des k-NN et de simuler la gestion budgétaire d'un mercato.

---

## 🛠️ Stack Technique

### Backend (Python & FastAPI)
- **FastAPI** : API REST rapide et documentée pour les endpoints de recherche et d'authentification.
- **SQLite** : Base de données locale pour la gestion des comptes utilisateurs et des statistiques joueurs.
- **PyJWT & Passlib** : Sécurité et gestion des rôles d'accès RBAC (Scout, Directeur Sportif, Admin).
- **pandas & scikit-learn** : Traitement des données Opta / FBref et algorithme de recherche par similarité (k-NN).

### Frontend (React & Vite)
- **React 18** : Découpage modulaire des composants (Filtres, Recherche, Radar Canvas, Dashboard Budget).
- **Vanilla CSS** : Design épuré moderne sur thème sombre.
- **HTML5 Canvas / SVG** : Représentation graphique multidimensionnelle sous forme de radar 6 axes.

---

## 🔑 Niveaux d'Accès (RBAC)

- **Recruteur (Scout)** : Recherche de joueurs, filtres multicritères, graphiques radars et jumeaux statistiques.
- **Directeur Sportif** : Accès étendu aux fiches confidentielles (Valeurs marchandes, Salaires) et simulateur d'enveloppe mercato.
- **Administrateur** : Gestion globale de la plateforme.

---

## 🚀 Lancement Local

1. **Lancer le Backend Python** :
   ```bash
   cd backend
   pip install -r requirements.txt
   python main.py
   ```
2. **Lancer le Frontend React** :
   ```bash
   cd Frontend
   npm install
   npm run dev
   ```

---

## 🌐 Déploiement

Le frontend est déployé et hébergé en ligne sur Vercel :
👉 [https://recruitment-match-pro.vercel.app](https://recruitment-match-pro.vercel.app)

---

## 👤 Auteur
**Rayane Ourad** — Projet Data Science & Développement Web.
