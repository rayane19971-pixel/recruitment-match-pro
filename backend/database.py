import sqlite3
import os
import math

DB_PATH = "data/recruitment_app.db"

def get_connection():
    """Crée le dossier data si nécessaire et retourne une connexion SQLite."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    """Initialise les tables 'users' et 'players'."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Table Utilisateurs (RBAC)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL, 
            role TEXT NOT NULL DEFAULT 'scout'
        )
    ''')
    
    # Table Joueurs (Données Opta + Financières)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            club TEXT NOT NULL,
            league TEXT NOT NULL,
            position TEXT NOT NULL,
            age INTEGER NOT NULL,
            nationality TEXT NOT NULL,
            market_value INTEGER NOT NULL,
            wage INTEGER NOT NULL,
            contract_expires INTEGER NOT NULL,
            
            -- Métriques Opta (Percentiles 0 à 100)
            stat_finishing INTEGER DEFAULT 50,  -- xG / Finition
            stat_dribbling INTEGER DEFAULT 50,  -- Dribbles / Percussion
            stat_passing INTEGER DEFAULT 50,    -- xA / Passes clés
            stat_pace INTEGER DEFAULT 50,       -- Vitesse / Courses progressives
            stat_defending INTEGER DEFAULT 50,  -- Tacles / Interceptions
            stat_physical INTEGER DEFAULT 50    -- Duels aériens / Endurance
        )
    ''')
    
    conn.commit()
    conn.close()
    print("[OK] Base de donnees (users & players) prete !")


# --- GESTION UTILISATEURS ---

def get_user_by_username(username: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def create_user(username: str, hashed_password: str, role: str = "scout"):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, hashed_password, role)
        )
        conn.commit()
        print(f"✅ Utilisateur '{username}' (Rôle: {role}) créé avec succès !")
        return True
    except sqlite3.IntegrityError:
        print(f"⚠️ Erreur : L'utilisateur '{username}' existe déjà.")
        return False
    finally:
        conn.close()

# --- MOTEUR DE MATCHING JOUEURS (OPTA) ---

def search_players_matching(
    position: str = None,
    max_age: int = None,
    max_market_value: int = None,
    max_wage: int = None,
    max_contract_year: int = None,
    target_finishing: int = 50,
    target_dribbling: int = 50,
    target_passing: int = 50,
    target_pace: int = 50,
    target_defending: int = 50,
    target_physical: int = 50,
    name_query: str = None
):
    """
    Recherche et calcule le score de compatibilité (%) entre le profil recherché 
    et les statistiques Opta réelles de chaque joueur.
    Permet également la recherche directe par nom de joueur (ex: 'Cherki', 'Mbappé').
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Construction dynamique des filtres bloquants
    query = "SELECT * FROM players WHERE 1=1"
    params = []
    
    if name_query and name_query.strip():
        query += " AND name LIKE ?"
        params.append(f"%{name_query.strip()}%")
    if position and position != "Tous":
        query += " AND position = ?"
        params.append(position)
    if max_age:
        query += " AND age <= ?"
        params.append(max_age)
    if max_market_value:
        query += " AND market_value <= ?"
        params.append(max_market_value)
    if max_wage:
        query += " AND wage <= ?"
        params.append(max_wage)
    if max_contract_year:
        query += " AND contract_expires <= ?"
        params.append(max_contract_year)
        
    cursor.execute(query, params)
    players = cursor.fetchall()
    conn.close()

    
    results = []
    for player in players:
        p = dict(player)
        
        # Algorithme de distance euclidienne pondérée (Compatibilité Opta %)
        diff_sq = (
            (p['stat_finishing'] - target_finishing)**2 +
            (p['stat_dribbling'] - target_dribbling)**2 +
            (p['stat_passing'] - target_passing)**2 +
            (p['stat_pace'] - target_pace)**2 +
            (p['stat_defending'] - target_defending)**2 +
            (p['stat_physical'] - target_physical)**2
        )
        distance = math.sqrt(diff_sq / 6)
        
        # Transformation de la distance en pourcentage de compatibilité (0 à 100%)
        match_score = round(max(0, 100 - distance), 1)
        p['match_score'] = match_score
        results.append(p)
        
    # Tri des résultats par score de compatibilité décroissant (%)
    results.sort(key=lambda x: x['match_score'], reverse=True)
    return results

def get_knn_similar_players(player_id: int, k: int = 5, min_similarity: float = 50.0):
    """
    Algorithme KNN (K-Nearest Neighbors / K-Plus Proches Voisins)
    Trouve les K joueurs réels les plus proches statistiquement d'un joueur cible (ex: trouver un jumeau à Cherki ou Lacazette).
    Filtre les résultats trop éloignés (par défaut similarité minimale = 50%).
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Récupérer le joueur cible
    cursor.execute("SELECT * FROM players WHERE id = ?", (player_id,))
    target_player = cursor.fetchone()
    if not target_player:
        conn.close()
        return None
        
    t = dict(target_player)
    
    # 2. Récupérer tous les autres joueurs de la même catégorie de poste (ex: tous les Attaquants ou Milieux)
    cursor.execute("SELECT * FROM players WHERE position = ? AND id != ?", (t['position'], player_id))
    candidates = cursor.fetchall()
    conn.close()
    
    # 3. Calcul de la distance euclidienne multidimensionnelle (KNN)
    knn_results = []
    for candidate in candidates:
        c = dict(candidate)
        
        # Formule Mathématique KNN : Distance entre le vecteur du joueur cible et le candidat
        distance = math.sqrt(
            (c['stat_finishing'] - t['stat_finishing'])**2 +
            (c['stat_dribbling'] - t['stat_dribbling'])**2 +
            (c['stat_passing'] - t['stat_passing'])**2 +
            (c['stat_pace'] - t['stat_pace'])**2 +
            (c['stat_defending'] - t['stat_defending'])**2 +
            (c['stat_physical'] - t['stat_physical'])**2
        ) / math.sqrt(6)
        
        similarity_pct = round(max(0, 100 - distance), 1)
        c['similarity_score'] = similarity_pct
        
        # 🛡️ FILTRE DE QUALITÉ : On ne retient que les joueurs ayant une similarité suffisante !
        if similarity_pct >= min_similarity:
            knn_results.append(c)
        
    # 4. Sélection des K plus proches voisins (triés par similarité maximale)
    knn_results.sort(key=lambda x: x['similarity_score'], reverse=True)
    return knn_results[:k]


if __name__ == "__main__":
    create_db()