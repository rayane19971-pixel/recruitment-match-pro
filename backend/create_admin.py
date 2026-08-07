from database import create_db, create_user
from auth_utils import hash_password

def init_test_users():
    # 1. S'assurer que la base et la table 'users' sont créées
    create_db()
    
    print("\n--- Création des comptes de démonstration ---")
    
    # 2. Créer l'Administrateur
    hashed_admin = hash_password("Admin_Rayane")
    create_user("rayane", hashed_admin, role="admin")
    
    # 3. Créer le Directeur Sportif
    hashed_director = hash_password("Director_OL")
    create_user("directeur", hashed_director, role="director")
    
    # 4. Créer le Recruteur / Scout
    hashed_scout = hash_password("Scout_OL")
    create_user("scout1", hashed_scout, role="scout")

if __name__ == "__main__":
    init_test_users()