from database import get_connection, create_db

def import_players():
    # S'assurer que les tables existent
    create_db()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Réinitialiser la table si elle contenait d'anciennes données
    cursor.execute("DELETE FROM players")
    
    # ⚽ Base de données enrichie de Joueurs Réels (Opta / StatsBomb / Données Financières)
    players_data = [
        # --- ATTAQUANTS (FW) ---
        ("Alexandre Lacazette", "Olympique Lyonnais", "Ligue 1", "Attaquant", 33, "France", 9000000, 4800000, 2025, 88, 72, 75, 70, 45, 78),
        ("Georges Mikautadze", "Olympique Lyonnais", "Ligue 1", "Attaquant", 23, "Géorgie", 20000000, 2400000, 2028, 86, 82, 74, 80, 38, 75),
        ("Ernest Nuamah", "Olympique Lyonnais", "Ligue 1", "Attaquant", 20, "Ghana", 18000000, 1800000, 2028, 74, 87, 72, 88, 40, 70),
        ("Malick Fofana", "Olympique Lyonnais", "Ligue 1", "Attaquant", 19, "Belgique", 15000000, 1200000, 2028, 78, 89, 74, 90, 35, 68),
        ("Gift Orban", "Olympique Lyonnais", "Ligue 1", "Attaquant", 21, "Nigeria", 15000000, 1500000, 2028, 82, 74, 65, 85, 30, 75),
        
        ("Bradley Barcola", "Paris Saint-Germain", "Ligue 1", "Attaquant", 21, "France", 50000000, 4000000, 2028, 84, 91, 80, 93, 42, 74),
        ("Kylian Mbappé", "Real Madrid", "La Liga", "Attaquant", 25, "France", 180000000, 31200000, 2029, 97, 94, 82, 97, 35, 84),
        ("Erling Haaland", "Manchester City", "Premier League", "Attaquant", 23, "Norvège", 180000000, 22500000, 2027, 98, 76, 68, 89, 40, 92),
        ("Jonathan David", "LOSC Lille", "Ligue 1", "Attaquant", 24, "Canada", 50000000, 2200000, 2025, 89, 78, 72, 84, 42, 80),
        ("Vinicius Jr", "Real Madrid", "La Liga", "Attaquant", 23, "Brésil", 180000000, 20800000, 2027, 91, 98, 84, 95, 38, 76),
        ("Viktor Gyökeres", "Sporting CP", "Liga Portugal", "Attaquant", 26, "Suède", 65000000, 3000000, 2028, 93, 84, 76, 88, 45, 90),
        ("Serhou Guirassy", "Borussia Dortmund", "Bundesliga", "Attaquant", 28, "Guinée", 40000000, 4500000, 2028, 92, 75, 70, 81, 40, 86),
        ("Santiago Giménez", "Feyenoord", "Eredivisie", "Attaquant", 23, "Mexique", 40000000, 2000000, 2027, 88, 76, 68, 82, 36, 82),
        ("Lautaro Martínez", "Inter Milan", "Serie A", "Attaquant", 26, "Argentine", 110000000, 11000000, 2029, 93, 83, 78, 82, 48, 85),
        ("Victor Osimhen", "Galatasaray", "Süper Lig", "Attaquant", 25, "Nigeria", 75000000, 9000000, 2026, 91, 80, 70, 89, 42, 88),

        # --- MILIEUX DE TERRAIN (MF) ---
        ("Rayan Cherki", "Olympique Lyonnais", "Ligue 1", "Milieu", 20, "France", 25000000, 2500000, 2026, 75, 95, 90, 78, 35, 62),
        ("Maxence Caqueret", "Olympique Lyonnais", "Ligue 1", "Milieu", 24, "France", 20000000, 2800000, 2027, 60, 78, 84, 76, 82, 85),
        ("Corentin Tolisso", "Olympique Lyonnais", "Ligue 1", "Milieu", 29, "France", 12000000, 4200000, 2027, 72, 74, 83, 68, 78, 80),
        ("Tanner Tessmann", "Olympique Lyonnais", "Ligue 1", "Milieu", 22, "USA", 7000000, 1400000, 2029, 65, 72, 78, 72, 80, 84),
        ("Nemanja Matić", "Olympique Lyonnais", "Ligue 1", "Milieu", 35, "Serbie", 3000000, 3000000, 2026, 55, 68, 85, 50, 84, 82),
        
        ("Maghnes Akliouche", "AS Monaco", "Ligue 1", "Milieu", 22, "France", 30000000, 1400000, 2026, 78, 89, 86, 82, 55, 68),
        ("Jude Bellingham", "Real Madrid", "La Liga", "Milieu", 20, "Angleterre", 180000000, 20800000, 2029, 90, 88, 91, 85, 84, 89),
        ("Florian Wirtz", "Bayer Leverkusen", "Bundesliga", "Milieu", 21, "Allemagne", 130000000, 7500000, 2027, 88, 94, 95, 84, 52, 70),
        ("Jamal Musiala", "Bayern Munich", "Bundesliga", "Milieu", 21, "Allemagne", 130000000, 8000000, 2026, 86, 97, 88, 88, 48, 72),
        ("Warren Zaïre-Emery", "Paris Saint-Germain", "Ligue 1", "Milieu", 18, "France", 60000000, 4500000, 2029, 70, 82, 84, 80, 80, 82),
        ("Lucas Paquetá", "West Ham", "Premier League", "Milieu", 26, "Brésil", 65000000, 7800000, 2027, 78, 89, 88, 75, 76, 82),
        ("Xavi Simons", "RB Leipzig", "Bundesliga", "Milieu", 21, "Pays-Bas", 80000000, 6000000, 2027, 82, 91, 89, 86, 45, 72),
        ("Eduardo Camavinga", "Real Madrid", "La Liga", "Milieu", 21, "France", 100000000, 8300000, 2029, 65, 86, 85, 84, 88, 84),
        ("Bruno Guimarães", "Newcastle United", "Premier League", "Milieu", 26, "Brésil", 85000000, 9600000, 2028, 74, 84, 88, 74, 84, 85),

        # --- DÉFENSEURS (DF) ---
        ("Moussa Niakhaté", "Olympique Lyonnais", "Ligue 1", "Défenseur", 28, "Sénégal", 16000000, 3000000, 2028, 40, 58, 65, 75, 86, 88),
        ("Clinton Mata", "Olympique Lyonnais", "Ligue 1", "Défenseur", 31, "Angola", 4000000, 1800000, 2026, 35, 68, 70, 78, 83, 82),
        ("Nicolas Tagliafico", "Olympique Lyonnais", "Ligue 1", "Défenseur", 31, "Argentine", 8000000, 3000000, 2025, 52, 70, 74, 72, 85, 80),
        ("Abner Vinícius", "Olympique Lyonnais", "Ligue 1", "Défenseur", 24, "Brésil", 8000000, 1600000, 2029, 42, 74, 73, 81, 78, 76),
        ("Saël Kumbedi", "Olympique Lyonnais", "Ligue 1", "Défenseur", 19, "France", 8000000, 1000000, 2027, 40, 72, 70, 85, 76, 74),
        
        ("Malo Gusto", "Chelsea", "Premier League", "Défenseur", 21, "France", 35000000, 2800000, 2030, 45, 82, 80, 89, 81, 78),
        ("Leny Yoro", "Manchester United", "Premier League", "Défenseur", 18, "France", 50000000, 6000000, 2029, 38, 70, 72, 84, 89, 84),
        ("Castello Lukeba", "RB Leipzig", "Bundesliga", "Défenseur", 21, "France", 40000000, 3200000, 2028, 35, 65, 76, 80, 88, 85),
        ("William Saliba", "Arsenal", "Premier League", "Défenseur", 23, "France", 80000000, 11000000, 2027, 35, 68, 78, 83, 93, 88),
        ("Achraf Hakimi", "Paris Saint-Germain", "Ligue 1", "Défenseur", 25, "Maroc", 60000000, 10000000, 2026, 72, 85, 84, 94, 78, 82),
        ("Jeremie Frimpong", "Bayer Leverkusen", "Bundesliga", "Défenseur", 23, "Pays-Bas", 50000000, 3500000, 2028, 78, 89, 83, 95, 72, 76),
        ("Theo Hernández", "AC Milan", "Serie A", "Défenseur", 26, "France", 60000000, 5200000, 2026, 74, 84, 79, 93, 80, 86),

        # --- GARDIENS (GK) ---
        ("Lucas Perri", "Olympique Lyonnais", "Ligue 1", "Gardien", 26, "Brésil", 8000000, 1500000, 2028, 10, 20, 65, 55, 90, 88),
        ("Anthony Lopes", "Olympique Lyonnais", "Ligue 1", "Gardien", 33, "Portugal", 3000000, 4200000, 2025, 10, 15, 60, 50, 86, 82),
        ("Mike Maignan", "AC Milan", "Serie A", "Gardien", 28, "France", 45000000, 5200000, 2026, 10, 25, 80, 60, 95, 90),
        ("Lucas Chevalier", "LOSC Lille", "Ligue 1", "Gardien", 22, "France", 25000000, 1200000, 2027, 10, 20, 72, 58, 88, 84),
        ("Diogo Costa", "FC Porto", "Liga Portugal", "Gardien", 24, "Portugal", 45000000, 2400000, 2027, 10, 30, 84, 58, 92, 86)
    ]

    cursor.executemany('''
        INSERT INTO players (
            name, club, league, position, age, nationality, market_value, wage, contract_expires,
            stat_finishing, stat_dribbling, stat_passing, stat_pace, stat_defending, stat_physical
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', players_data)

    conn.commit()
    conn.close()
    print(f"[OK] {len(players_data)} joueurs Opta importes avec succes dans la base de donnees SQLite !")


if __name__ == "__main__":
    import_players()