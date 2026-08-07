import random
from database import get_connection, create_db

# --- DONNÉES DE GÉNÉRATION DE MASSIVE DATABASE DE FOOTBALL ---

FIRST_NAMES = [
    "Lucas", "Mateo", "Enzo", "Hugo", "Leo", "Gabriel", "Rayan", "Arthur", "Jules", "Louis",
    "Marco", "Matteo", "Alessandro", "Giovanni", "Lorenzo", "Federico", "Nicolo", "Andrea",
    "Carlos", "Alejandro", "Daniel", "Pablo", "Adrian", "Gonzalo", "Rodrigo", "Javier",
    "Oliver", "Jack", "Harry", "Charlie", "George", "James", "William", "Thomas", "Ethan",
    "Florian", "Maximilian", "Julian", "Leon", "Felix", "Paul", "Jonas", "Lukas", "Tim",
    "Thiago", "Felipe", "Matheus", "Rafael", "Bruno", "Diego", "Bernardo", "Pedro", "João",
    "Mohamed", "Youssef", "Amine", "Achraf", "Sofiane", "Ismaël", "Idrissa", "Sadio", "Kalidou"
]

LAST_NAMES = [
    "Dupont", "Moreau", "Bernard", "Petit", "Roux", "Girard", "Lefebvre", "Mercier", "Bonnet",
    "Rossi", "Russo", "Ferrari", "Esposito", "Bianchi", "Romano", "Colombo", "Ricci", "Greco",
    "García", "Martínez", "López", "González", "Rodríguez", "Fernández", "Pérez", "Sánchez",
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Taylor",
    "Müller", "Schmidt", "Schneider", "Fischer", "Weber", "Meyer", "Wagner", "Becker", "Schulz",
    "Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira", "Alves", "Pereira", "Lima",
    "Diallo", "Traoré", "Camara", "Mendy", "Sow", "Diop", "Cissé", "Koné", "Coulibaly", "Brahimi"
]

CLUBS_BY_LEAGUE = {
    "Ligue 1": ["Olympique Lyonnais", "Paris Saint-Germain", "AS Monaco", "LOSC Lille", "OGC Nice", "RC Lens", "Olympique de Marseille", "Stade Rennais", "RC Strasbourg", "Toulouse FC", "FC Nantes", "Stade Brestois"],
    "Ligue 2": ["AS Saint-Étienne", "Girondins de Bordeaux", "AJ Auxerre", "Angers SCO", "SM Caen", "SC Bastia", "EA Guingamp", "Paris FC"],
    "Premier League": ["Manchester City", "Arsenal", "Liverpool", "Aston Villa", "Tottenham Hotspur", "Chelsea", "Newcastle United", "Manchester United", "West Ham", "Brighton", "Wolverhampton", "Fulham"],
    "Championship": ["Leicester City", "Leeds United", "Southampton", "Ipswich Town", "West Bromwich", "Norwich City", "Coventry City", "Middlesbrough"],
    "La Liga": ["Real Madrid", "FC Barcelona", "Atlético Madrid", "Athletic Bilbao", "Real Sociedad", "Real Betis", "Villarreal", "Sevilla FC", "Girona FC", "Valencia CF"],
    "Bundesliga": ["Bayer Leverkusen", "Bayern Munich", "VfB Stuttgart", "RB Leipzig", "Borussia Dortmund", "Eintracht Frankfurt", "TSG Hoffenheim", "SC Freiburg"],
    "Serie A": ["Inter Milan", "AC Milan", "Juventus", "Atalanta", "AS Roma", "SS Lazio", "SSC Napoli", "ACF Fiorentina", "Bologna"],
    "Liga Portugal": ["Sporting CP", "SL Benfica", "FC Porto", "SC Braga", "Vitoria Guimaraes"],
    "Eredivisie": ["PSV Eindhoven", "Feyenoord", "Ajax Amsterdam", "AZ Alkmaar", "Twente"],
    "Brasileirão": ["Flamengo", "Palmeiras", "Botafogo", "Atlético Mineiro", "Fluminense", "São Paulo FC", "Grêmio", "Internacional"]
}

LEAGUE_NATIONALITIES = {
    "Ligue 1": ["France", "France", "France", "Brésil", "Sénégal", "Côte d'Ivoire", "Algérie", "Belgique", "Portugal", "Cameroun"],
    "Ligue 2": ["France", "France", "France", "France", "Mali", "Sénégal", "Maroc"],
    "Premier League": ["Angleterre", "Angleterre", "Brésil", "Espagne", "France", "Portugal", "Argentine", "Pays-Bas", "Ecosse"],
    "Championship": ["Angleterre", "Angleterre", "Irlande", "Ecosse", "Pays de Galles"],
    "La Liga": ["Espagne", "Espagne", "Espagne", "Argentine", "Brésil", "Uruguay", "France"],
    "Bundesliga": ["Allemagne", "Allemagne", "Allemagne", "France", "Autriche", "Suisse", "Pays-Bas"],
    "Serie A": ["Italie", "Italie", "Italie", "Argentine", "Brésil", "France", "Hollande"],
    "Liga Portugal": ["Portugal", "Portugal", "Brésil", "Brésil", "Argentine", "Espagne"],
    "Eredivisie": ["Pays-Bas", "Pays-Bas", "Belgique", "Danemark", "Maroc", "Mexique"],
    "Brasileirão": ["Brésil", "Brésil", "Brésil", "Argentine", "Uruguay", "Colombie", "Paraguay"]
}

POSITIONS = ["Attaquant", "Milieu", "Défenseur", "Gardien"]

def generate_player(id_num):
    league = random.choice(list(CLUBS_BY_LEAGUE.keys()))
    club = random.choice(CLUBS_BY_LEAGUE[league])
    nationality = random.choice(LEAGUE_NATIONALITIES[league])
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    name = f"{first_name} {last_name}"
    
    position = random.choices(POSITIONS, weights=[0.25, 0.40, 0.28, 0.07])[0]
    age = random.randint(17, 34)
    
    # Génération de stats Opta réalistes par poste (Percentiles 0 à 99)
    if position == "Attaquant":
        finishing = random.randint(55, 96)
        dribbling = random.randint(50, 94)
        passing = random.randint(40, 85)
        pace = random.randint(60, 96)
        defending = random.randint(20, 55)
        physical = random.randint(50, 92)
    elif position == "Milieu":
        finishing = random.randint(40, 85)
        dribbling = random.randint(55, 95)
        passing = random.randint(60, 97)
        pace = random.randint(50, 88)
        defending = random.randint(45, 88)
        physical = random.randint(50, 90)
    elif position == "Défenseur":
        finishing = random.randint(20, 55)
        dribbling = random.randint(35, 75)
        passing = random.randint(45, 82)
        pace = random.randint(55, 90)
        defending = random.randint(65, 97)
        physical = random.randint(65, 95)
    else:  # Gardien
        finishing = random.randint(5, 20)
        dribbling = random.randint(10, 35)
        passing = random.randint(40, 80)
        pace = random.randint(35, 65)
        defending = random.randint(80, 98)
        physical = random.randint(70, 92)

    # Données financières cohérentes selon le niveau général et l'âge
    overall_rating = (finishing + dribbling + passing + pace + defending + physical) // 6
    
    if overall_rating > 85:
        market_value = random.randint(45, 120) * 1000000
        wage = random.randint(400, 1200) * 10000
    elif overall_rating > 75:
        market_value = random.randint(12, 44) * 1000000
        wage = random.randint(120, 390) * 10000
    elif overall_rating > 65:
        market_value = random.randint(3, 11) * 1000000
        wage = random.randint(40, 110) * 10000
    else:
        market_value = random.randint(500, 2900) * 1000
        wage = random.randint(10, 38) * 10000

    contract_expires = random.choice([2025, 2026, 2027, 2028, 2029, 2030])

    return (
        name, club, league, position, age, nationality, market_value, wage, contract_expires,
        finishing, dribbling, passing, pace, defending, physical
    )

def generate_large_database(count=1500):
    create_db()
    conn = get_connection()
    cursor = conn.cursor()
    
    print(f"Génération de {count} joueurs professionnels dans la base SQLite...")
    
    players = [generate_player(i) for i in range(count)]
    
    cursor.executemany('''
        INSERT INTO players (
            name, club, league, position, age, nationality, market_value, wage, contract_expires,
            stat_finishing, stat_dribbling, stat_passing, stat_pace, stat_defending, stat_physical
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', players)
    
    conn.commit()
    conn.close()
    print(f"[OK] Base de donnees peuplee avec succès : {count} joueurs pro disponibles !")

if __name__ == "__main__":
    generate_large_database(1500)
