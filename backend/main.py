from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from database import get_user_by_username, create_user, search_players_matching, get_connection
from auth_utils import hash_password, verify_password, create_access_token, decode_access_token

app = FastAPI(
    title="Recruitment Match OL - API",
    description="API de recrutement basée sur la data intelligence Opta pour l'Olympique Lyonnais",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# --- MODÈLES PYDANTIC ---
class UserRegister(BaseModel):
    username: str
    password: str
    role: str = "scout"

# --- DÉPENDANCES SÉCURITÉ & RÔLES ---

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Jeton d'authentification invalide ou expiré.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    user = get_user_by_username(username)
    if user is None:
        raise credentials_exception
    return dict(user)

def require_role(allowed_roles: list):
    def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Accès refusé. Rôle requis: {allowed_roles}"
            )
        return current_user
    return role_checker

# --- ROUTES PUBLIQUES ---

@app.get("/")
def home():
    return {
        "club": "Olympique Lyonnais",
        "statut": "Système de Recrutement Opta Connecté",
        "version": "1.0.0"
    }

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utilisateur ou mot de passe incorrect.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]}
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user["role"],
        "username": user["username"]
    }

# --- ROUTES DE RECHERCHE DE JOUEURS & MATCHING OPTA ---

@app.get("/players/search")
def search_players(
    position: Optional[str] = Query(None, description="Poste: Attaquant, Milieu, Défenseur, Gardien"),
    max_age: Optional[int] = Query(None, description="Âge maximum"),
    max_market_value: Optional[int] = Query(None, description="Valeur marchand maximale en €"),
    max_wage: Optional[int] = Query(None, description="Salaire maximum annuel en €"),
    max_contract_year: Optional[int] = Query(None, description="Fin de contrat max (ex: 2026)"),
    
    # Curseurs Opta (0 à 100)
    finishing: int = Query(50, ge=0, le=100, description="Niveau de Finition / xG (0-100)"),
    dribbling: int = Query(50, ge=0, le=100, description="Niveau de Dribble / Percussion (0-100)"),
    passing: int = Query(50, ge=0, le=100, description="Niveau de Passes clés / xA (0-100)"),
    pace: int = Query(50, ge=0, le=100, description="Niveau de Vitesse (0-100)"),
    defending: int = Query(50, ge=0, le=100, description="Niveau de Défense (0-100)"),
    physical: int = Query(50, ge=0, le=100, description="Niveau Physique / Endurance (0-100)"),
    query: str = Query(None, description="Nom ou recherche partielle de joueur"),
    
    current_user: dict = Depends(get_current_user)
):
    """
    Recherche multicritère et calcul du score de compatibilité Opta (0-100%).
    Données financières masquées pour les comptes 'scout'.
    """
    players = search_players_matching(
        position=position,
        max_age=max_age,
        max_market_value=max_market_value,
        max_wage=max_wage,
        max_contract_year=max_contract_year,
        target_finishing=finishing,
        target_dribbling=dribbling,
        target_passing=passing,
        target_pace=pace,
        target_defending=defending,
        target_physical=physical,
        name_query=query
    )

    # Ajout explicite du pourcentage de compatibilité et masquage selon rôle
    for p in players:
        p["score_compatibilite"] = f"{p['match_score']}%"
        if current_user["role"] == "scout":
            p["market_value"] = "Confidentiel (Réservé Direction)"
            p["wage"] = "Confidentiel (Réservé Direction)"
            
    return {
        "total_resultats": len(players),
        "recherche_par": current_user["username"],
        "role_utilisateur": current_user["role"],
        "joueurs": players
    }


@app.get("/players/{player_id}")
def get_player_detail(player_id: int, current_user: dict = Depends(get_current_user)):
    """Retourne la fiche détaillée d'un joueur (utile pour le graphique radar)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM players WHERE id = ?", (player_id,))
    player = cursor.fetchone()
    conn.close()
    
    if not player:
        raise HTTPException(status_code=404, detail="Joueur non trouvé.")
        
    p = dict(player)
    if current_user["role"] == "scout":
        p["market_value"] = "Confidentiel"
        p["wage"] = "Confidentiel"
        
    return p

@app.get("/players/{player_id}/similar")
def get_similar_players_knn(
    player_id: int, 
    k: int = Query(5, ge=1, le=20, description="Nombre de K plus proches voisins à retourner"),
    min_similarity: float = Query(50.0, ge=0.0, le=100.0, description="Seuil de similarité minimale en %"),
    current_user: dict = Depends(get_current_user)
):
    """
    Recherche KNN (K-Nearest Neighbors).
    Prend un joueur et retourne ses K plus proches voisins statistiques (jumeaux statistiques).
    Filtre les profils ayant une similarité inférieure au seuil minimal.
    """
    from database import get_knn_similar_players
    similar_players = get_knn_similar_players(player_id, k=k, min_similarity=min_similarity)
    
    if similar_players is None:
        raise HTTPException(status_code=404, detail="Joueur non trouvé.")
        
    if current_user["role"] == "scout":
        for p in similar_players:
            p["market_value"] = "Confidentiel"
            p["wage"] = "Confidentiel"
            
    return {
        "joueur_id_cible": player_id,
        "k_voisins_demandes": k,
        "seuil_minimal": f"{min_similarity}%",
        "nb_voisins_qualifies": len(similar_players),
        "algorithme": "KNN (Distance Euclidienne Multidimensionnelle Opta)",
        "voisins_similaires": similar_players
    }



# --- ROUTES ADMINISTRATIVES ET RÔLES ---

@app.get("/users/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    return {
        "id": current_user["id"],
        "username": current_user["username"],
        "role": current_user["role"]
    }

@app.get("/director/budget")
def director_budget(current_user: dict = Depends(require_role(["director", "admin"]))):
    return {
        "message": "Accès autorisé aux données financières de la direction.",
        "enveloppe_transferts": "45,000,000 €",
        "masse_salariale_max": "12,000,000 € / an",
        "autorise_par": current_user["username"]
    }


@app.post("/register")
def register_user(
    user_data: UserRegister, 
    current_user: dict = Depends(require_role(["admin"]))
):
    hashed_pwd = hash_password(user_data.password)
    success = create_user(user_data.username, hashed_pwd, user_data.role)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Impossible de créer cet utilisateur (pseudo déjà pris)."
        )
    return {"message": f"Utilisateur '{user_data.username}' créé avec le rôle '{user_data.role}'."}