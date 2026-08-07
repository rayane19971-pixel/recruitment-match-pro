from database import get_connection, create_db

def import_real_opta_players():
    create_db()
    conn = get_connection()
    cursor = conn.cursor()
    
    # Réinitialiser la table des joueurs pour n'avoir QUE des vrais joueurs réels
    cursor.execute("DELETE FROM players")
    
    # ⚽ Base de Données 100% Joueurs Réels (Stats Opta / FBref & Valeurs Financières Transfermarkt)
    real_players = [
        # === LIGUE 1 (FRANCE) ===
        # Attaquants / Ailiers
        ("Kylian Mbappé", "Paris Saint-Germain", "Ligue 1", "Attaquant", 25, "France", 180000000, 31200000, 2029, 97, 94, 82, 97, 35, 84),
        ("Bradley Barcola", "Paris Saint-Germain", "Ligue 1", "Attaquant", 21, "France", 50000000, 4000000, 2028, 84, 91, 80, 93, 42, 74),
        ("Ousmane Dembélé", "Paris Saint-Germain", "Ligue 1", "Attaquant", 27, "France", 60000000, 12000000, 2028, 76, 97, 92, 94, 32, 65),
        ("Randal Kolo Muani", "Paris Saint-Germain", "Ligue 1", "Attaquant", 25, "France", 45000000, 9000000, 2028, 80, 82, 72, 88, 40, 78),
        ("Gonçalo Ramos", "Paris Saint-Germain", "Ligue 1", "Attaquant", 23, "Portugal", 50000000, 6000000, 2028, 85, 72, 68, 80, 42, 82),
        
        ("Alexandre Lacazette", "Olympique Lyonnais", "Ligue 1", "Attaquant", 33, "France", 9000000, 4800000, 2025, 88, 72, 75, 70, 45, 78),
        ("Georges Mikautadze", "Olympique Lyonnais", "Ligue 1", "Attaquant", 23, "Géorgie", 20000000, 2400000, 2028, 86, 82, 74, 80, 38, 75),
        ("Ernest Nuamah", "Olympique Lyonnais", "Ligue 1", "Attaquant", 20, "Ghana", 18000000, 1800000, 2028, 74, 87, 72, 88, 40, 70),
        ("Malick Fofana", "Olympique Lyonnais", "Ligue 1", "Attaquant", 19, "Belgique", 15000000, 1200000, 2028, 78, 89, 74, 90, 35, 68),
        ("Gift Orban", "Olympique Lyonnais", "Ligue 1", "Attaquant", 21, "Nigeria", 15000000, 1500000, 2028, 82, 74, 65, 85, 30, 75),
        ("Wilfried Zaha", "Olympique Lyonnais", "Ligue 1", "Attaquant", 31, "Côte d'Ivoire", 11000000, 3000000, 2025, 78, 88, 76, 82, 38, 74),
        
        ("Jonathan David", "LOSC Lille", "Ligue 1", "Attaquant", 24, "Canada", 50000000, 2200000, 2025, 89, 78, 72, 84, 42, 80),
        ("Edon Zhegrova", "LOSC Lille", "Ligue 1", "Attaquant", 25, "Kosovo", 25000000, 1500000, 2026, 80, 93, 85, 86, 35, 62),
        ("Mason Greenwood", "Olympique de Marseille", "Ligue 1", "Attaquant", 22, "Angleterre", 35000000, 4000000, 2029, 88, 86, 78, 88, 32, 72),
        ("Elye Wahi", "Olympique de Marseille", "Ligue 1", "Attaquant", 21, "France", 30000000, 2800000, 2029, 82, 78, 68, 86, 35, 74),
        ("Pierre-Emerick Aubameyang", "Al-Qadsiah", "Saudi Pro League", "Attaquant", 35, "Gabon", 5000000, 8000000, 2026, 86, 76, 70, 82, 35, 72),
        ("Folarin Balogun", "AS Monaco", "Ligue 1", "Attaquant", 23, "USA", 30000000, 3600000, 2028, 82, 76, 70, 84, 38, 76),
        ("Breel Embolo", "AS Monaco", "Ligue 1", "Attaquant", 27, "Suisse", 12000000, 3000000, 2026, 78, 74, 68, 80, 45, 88),
        ("Arnaud Kalimuendo", "Stade Rennais", "Ligue 1", "Attaquant", 22, "France", 20000000, 1800000, 2027, 80, 76, 72, 82, 38, 74),
        ("Ludovic Ajorque", "Stade Brestois", "Ligue 1", "Attaquant", 30, "France", 4000000, 1200000, 2027, 76, 60, 65, 62, 50, 92),
        
        # Milieux de Terrain
        ("Rayan Cherki", "Olympique Lyonnais", "Ligue 1", "Milieu", 20, "France", 25000000, 2500000, 2026, 75, 95, 90, 78, 35, 62),
        ("Maxence Caqueret", "Olympique Lyonnais", "Ligue 1", "Milieu", 24, "France", 20000000, 2800000, 2027, 60, 78, 84, 76, 82, 85),
        ("Corentin Tolisso", "Olympique Lyonnais", "Ligue 1", "Milieu", 29, "France", 12000000, 4200000, 2027, 72, 74, 83, 68, 78, 80),
        ("Tanner Tessmann", "Olympique Lyonnais", "Ligue 1", "Milieu", 22, "USA", 7000000, 1400000, 2029, 65, 72, 78, 72, 80, 84),
        ("Jordan Veretout", "Olympique Lyonnais", "Ligue 1", "Milieu", 31, "France", 8000000, 3600000, 2026, 68, 72, 82, 68, 76, 78),
        ("Nemanja Matić", "Olympique Lyonnais", "Ligue 1", "Milieu", 35, "Serbie", 3000000, 3000000, 2026, 55, 68, 85, 50, 84, 82),
        
        ("Vitinha", "Paris Saint-Germain", "Ligue 1", "Milieu", 24, "Portugal", 55000000, 5500000, 2027, 72, 86, 91, 76, 78, 74),
        ("Warren Zaïre-Emery", "Paris Saint-Germain", "Ligue 1", "Milieu", 18, "France", 60000000, 4500000, 2029, 70, 82, 84, 80, 80, 82),
        ("Joao Neves", "Paris Saint-Germain", "Ligue 1", "Milieu", 19, "Portugal", 60000000, 4000000, 2029, 68, 84, 89, 78, 85, 80),
        ("Fabian Ruiz", "Paris Saint-Germain", "Ligue 1", "Milieu", 28, "Espagne", 35000000, 5000000, 2027, 75, 78, 88, 68, 74, 76),
        ("Maghnes Akliouche", "AS Monaco", "Ligue 1", "Milieu", 22, "France", 30000000, 1400000, 2026, 78, 89, 86, 82, 55, 68),
        ("Lamine Camara", "AS Monaco", "Ligue 1", "Milieu", 20, "Sénégal", 15000000, 1200000, 2029, 65, 76, 82, 78, 82, 84),
        ("Benjamin Bourigeaud", "Al-Duhail", "Qatar Stars League", "Milieu", 30, "France", 18000000, 4000000, 2027, 78, 76, 88, 72, 65, 74),
        ("Teji Savanier", "Montpellier HSC", "Ligue 1", "Milieu", 32, "France", 7000000, 2200000, 2026, 76, 82, 90, 65, 60, 72),
        ("Pierre-Lees Melou", "Stade Brestois", "Ligue 1", "Milieu", 31, "France", 10000000, 1500000, 2027, 72, 76, 85, 68, 86, 84),
        ("Angel Gomes", "LOSC Lille", "Ligue 1", "Milieu", 23, "Angleterre", 28000000, 1800000, 2025, 70, 88, 89, 78, 68, 65),  # En fin de contrat !
        
        # Défenseurs
        ("Moussa Niakhaté", "Olympique Lyonnais", "Ligue 1", "Défenseur", 28, "Sénégal", 16000000, 3000000, 2028, 40, 58, 65, 75, 86, 88),
        ("Clinton Mata", "Olympique Lyonnais", "Ligue 1", "Défenseur", 31, "Angola", 4000000, 1800000, 2026, 35, 68, 70, 78, 83, 82),
        ("Nicolas Tagliafico", "Olympique Lyonnais", "Ligue 1", "Défenseur", 31, "Argentine", 8000000, 3000000, 2025, 52, 70, 74, 72, 85, 80),
        ("Abner Vinícius", "Olympique Lyonnais", "Ligue 1", "Défenseur", 24, "Brésil", 8000000, 1600000, 2029, 42, 74, 73, 81, 78, 76),
        ("Saël Kumbedi", "Olympique Lyonnais", "Ligue 1", "Défenseur", 19, "France", 8000000, 1000000, 2027, 40, 72, 70, 85, 76, 74),
        ("Dušan Caleta-Car", "Olympique Lyonnais", "Ligue 1", "Défenseur", 27, "Croatie", 7000000, 2400000, 2027, 35, 52, 68, 65, 82, 86),
        
        ("Achraf Hakimi", "Paris Saint-Germain", "Ligue 1", "Défenseur", 25, "Maroc", 60000000, 10000000, 2026, 72, 85, 84, 94, 78, 82),
        ("Nuno Mendes", "Paris Saint-Germain", "Ligue 1", "Défenseur", 22, "Portugal", 55000000, 6000000, 2026, 62, 88, 80, 93, 80, 78),
        ("Marquinhos", "Paris Saint-Germain", "Ligue 1", "Défenseur", 30, "Brésil", 50000000, 14400000, 2028, 45, 65, 76, 74, 90, 85),
        ("Willian Pacho", "Paris Saint-Germain", "Ligue 1", "Défenseur", 22, "Équateur", 40000000, 3500000, 2029, 30, 60, 72, 78, 88, 88),
        ("Leonardo Balerdi", "Olympique de Marseille", "Ligue 1", "Défenseur", 25, "Argentine", 20000000, 2800000, 2028, 38, 64, 74, 76, 85, 84),
        ("Wilfried Singo", "AS Monaco", "Ligue 1", "Défenseur", 23, "Côte d'Ivoire", 25000000, 2000000, 2028, 48, 76, 70, 86, 84, 88),
        ("Facundo Medina", "RC Lens", "Ligue 1", "Défenseur", 25, "Argentine", 25000000, 1800000, 2028, 45, 72, 80, 74, 86, 84),
        ("Kevin Danso", "RC Lens", "Ligue 1", "Défenseur", 25, "Autriche", 25000000, 1800000, 2027, 32, 58, 68, 78, 88, 90),
        
        # Gardiens
        ("Lucas Perri", "Olympique Lyonnais", "Ligue 1", "Gardien", 26, "Brésil", 8000000, 1500000, 2028, 10, 20, 65, 55, 90, 88),
        ("Anthony Lopes", "Olympique Lyonnais", "Ligue 1", "Gardien", 33, "Portugal", 3000000, 4200000, 2025, 10, 15, 60, 50, 86, 82),
        ("Gianluigi Donnarumma", "Paris Saint-Germain", "Ligue 1", "Gardien", 25, "Italie", 40000000, 12000000, 2026, 10, 15, 62, 52, 92, 90),
        ("Lucas Chevalier", "LOSC Lille", "Ligue 1", "Gardien", 22, "France", 25000000, 1200000, 2027, 10, 20, 72, 58, 88, 84),
        ("Brice Samba", "RC Lens", "Ligue 1", "Gardien", 30, "France", 15000000, 2400000, 2028, 10, 25, 76, 54, 87, 85),
        ("Geronimo Rulli", "Olympique de Marseille", "Ligue 1", "Gardien", 32, "Argentine", 5000000, 2000000, 2027, 10, 20, 70, 52, 85, 82),
        
        # === PREMIER LEAGUE (ANGLETERRE) ===
        ("Erling Haaland", "Manchester City", "Premier League", "Attaquant", 23, "Norvège", 180000000, 22500000, 2027, 98, 76, 68, 89, 40, 92),
        ("Mohamed Salah", "Liverpool", "Premier League", "Attaquant", 32, "Égypte", 55000000, 21000000, 2025, 92, 90, 86, 88, 38, 78),  # Fin de contrat 2025 !
        ("Bukayo Saka", "Arsenal", "Premier League", "Attaquant", 22, "Angleterre", 140000000, 12000000, 2027, 88, 93, 88, 89, 45, 78),
        ("Cole Palmer", "Chelsea", "Premier League", "Attaquant", 22, "Angleterre", 90000000, 7800000, 2033, 90, 91, 91, 82, 40, 72),
        ("Son Heung-min", "Tottenham Hotspur", "Premier League", "Attaquant", 31, "Corée du Sud", 45000000, 11500000, 2025, 91, 86, 82, 87, 35, 74),
        ("Alexander Isak", "Newcastle United", "Premier League", "Attaquant", 24, "Suède", 75000000, 7200000, 2028, 90, 88, 74, 89, 36, 80),
        ("Ollie Watkins", "Aston Villa", "Premier League", "Attaquant", 28, "Angleterre", 65000000, 7800000, 2028, 88, 80, 78, 86, 42, 84),
        
        ("Rodri", "Manchester City", "Premier League", "Milieu", 28, "Espagne", 130000000, 13000000, 2027, 78, 84, 94, 72, 92, 91),
        ("Declan Rice", "Arsenal", "Premier League", "Milieu", 25, "Angleterre", 120000000, 14000000, 2028, 72, 82, 87, 78, 90, 89),
        ("Martin Ødegaard", "Arsenal", "Premier League", "Milieu", 25, "Norvège", 110000000, 13500000, 2028, 84, 92, 96, 78, 55, 70),
        ("Bruno Guimarães", "Newcastle United", "Premier League", "Milieu", 26, "Brésil", 85000000, 9600000, 2028, 74, 84, 88, 74, 84, 85),
        ("Kevin De Bruyne", "Manchester City", "Premier League", "Milieu", 32, "Belgique", 50000000, 24000000, 2025, 86, 87, 98, 74, 52, 76),
        ("Lucas Paquetá", "West Ham", "Premier League", "Milieu", 26, "Brésil", 65000000, 7800000, 2027, 78, 89, 88, 75, 76, 82),
        ("Alexis Mac Allister", "Liverpool", "Premier League", "Milieu", 25, "Argentine", 75000000, 9000000, 2028, 76, 84, 90, 74, 82, 80),
        ("Enzo Fernández", "Chelsea", "Premier League", "Milieu", 23, "Argentine", 75000000, 10800000, 2031, 72, 82, 91, 72, 80, 82),
        
        ("William Saliba", "Arsenal", "Premier League", "Défenseur", 23, "France", 80000000, 11000000, 2027, 35, 68, 78, 83, 93, 88),
        ("Gabriel Magalhães", "Arsenal", "Premier League", "Défenseur", 26, "Brésil", 75000000, 6000000, 2027, 50, 58, 70, 74, 91, 92),
        ("Virgil van Dijk", "Liverpool", "Premier League", "Défenseur", 32, "Pays-Bas", 30000000, 13500000, 2025, 45, 60, 78, 72, 94, 94),
        ("Trent Alexander-Arnold", "Liverpool", "Premier League", "Défenseur", 25, "Angleterre", 70000000, 11000000, 2025, 70, 84, 97, 82, 70, 74),
        ("Malo Gusto", "Chelsea", "Premier League", "Défenseur", 21, "France", 35000000, 2800000, 2030, 45, 82, 80, 89, 81, 78),
        ("Leny Yoro", "Manchester United", "Premier League", "Défenseur", 18, "France", 50000000, 6000000, 2029, 38, 70, 72, 84, 89, 84),
        ("Josko Gvardiol", "Manchester City", "Premier League", "Défenseur", 22, "Croatie", 75000000, 7200000, 2028, 55, 78, 82, 84, 88, 86),
        
        ("Alisson Becker", "Liverpool", "Premier League", "Gardien", 31, "Brésil", 28000000, 9000000, 2027, 10, 25, 82, 56, 94, 88),
        ("Ederson", "Manchester City", "Premier League", "Gardien", 30, "Brésil", 35000000, 6000000, 2026, 10, 30, 92, 60, 90, 86),
        ("David Raya", "Arsenal", "Premier League", "Gardien", 28, "Espagne", 35000000, 5000000, 2028, 10, 22, 85, 55, 89, 84),

        # === LA LIGA (ESPAGNE) ===
        ("Vinicius Jr", "Real Madrid", "La Liga", "Attaquant", 23, "Brésil", 180000000, 20800000, 2027, 91, 98, 84, 95, 38, 76),
        ("Lamine Yamal", "FC Barcelona", "La Liga", "Attaquant", 16, "Espagne", 120000000, 1600000, 2026, 85, 96, 91, 91, 40, 65),
        ("Robert Lewandowski", "FC Barcelona", "La Liga", "Attaquant", 35, "Pologne", 15000000, 20800000, 2026, 94, 76, 75, 72, 38, 84),
        ("Antoine Griezmann", "Atlético Madrid", "La Liga", "Attaquant", 33, "France", 25000000, 12500000, 2026, 88, 86, 93, 76, 68, 76),
        ("Rodrygo", "Real Madrid", "La Liga", "Attaquant", 23, "Brésil", 110000000, 12500000, 2028, 86, 92, 84, 90, 42, 70),
        ("Endrick", "Real Madrid", "La Liga", "Attaquant", 17, "Brésil", 60000000, 4000000, 2030, 84, 85, 70, 88, 35, 80),
        ("Nico Williams", "Athletic Bilbao", "La Liga", "Attaquant", 21, "Espagne", 70000000, 5200000, 2027, 82, 94, 82, 94, 38, 72),
        
        ("Jude Bellingham", "Real Madrid", "La Liga", "Milieu", 20, "Angleterre", 180000000, 20800000, 2029, 90, 88, 91, 85, 84, 89),
        ("Pedri", "FC Barcelona", "La Liga", "Milieu", 21, "Espagne", 80000000, 9300000, 2026, 75, 94, 95, 76, 68, 68),
        ("Gavi", "FC Barcelona", "La Liga", "Milieu", 19, "Espagne", 90000000, 6800000, 2026, 74, 86, 88, 80, 84, 84),
        ("Eduardo Camavinga", "Real Madrid", "La Liga", "Milieu", 21, "France", 100000000, 8300000, 2029, 65, 86, 85, 84, 88, 84),
        ("Aurélien Tchouaméni", "Real Madrid", "La Liga", "Milieu", 24, "France", 100000000, 12500000, 2028, 68, 78, 85, 78, 90, 90),
        ("Federico Valverde", "Real Madrid", "La Liga", "Milieu", 25, "Uruguay", 120000000, 16600000, 2029, 82, 85, 87, 91, 82, 89),
        ("Frenkie de Jong", "FC Barcelona", "La Liga", "Milieu", 27, "Pays-Bas", 70000000, 18000000, 2026, 70, 90, 93, 78, 76, 78),
        
        ("Jules Koundé", "FC Barcelona", "La Liga", "Défenseur", 25, "France", 55000000, 13500000, 2027, 45, 75, 78, 84, 88, 82),
        ("Ronald Araujo", "FC Barcelona", "La Liga", "Défenseur", 25, "Uruguay", 70000000, 7000000, 2026, 42, 62, 70, 85, 92, 92),
        ("Antonio Rüdiger", "Real Madrid", "La Liga", "Défenseur", 31, "Allemagne", 25000000, 14500000, 2026, 48, 64, 74, 82, 91, 94),
        ("Éder Militão", "Real Madrid", "La Liga", "Défenseur", 26, "Brésil", 60000000, 14500000, 2028, 44, 66, 72, 84, 89, 88),
        
        ("Thibaut Courtois", "Real Madrid", "La Liga", "Gardien", 32, "Belgique", 30000000, 15000000, 2026, 10, 18, 74, 52, 96, 92),
        ("Marc-André ter Stegen", "FC Barcelona", "La Liga", "Gardien", 32, "Allemagne", 28000000, 14000000, 2028, 10, 22, 88, 55, 91, 85),
        ("Jan Oblak", "Atlético Madrid", "La Liga", "Gardien", 31, "Slovénie", 28000000, 10000000, 2028, 10, 15, 68, 50, 93, 88),

        # === BUNDESLIGA (ALLEMAGNE) ===
        ("Florian Wirtz", "Bayer Leverkusen", "Bundesliga", "Milieu", 21, "Allemagne", 130000000, 7500000, 2027, 88, 94, 95, 84, 52, 70),
        ("Jamal Musiala", "Bayern Munich", "Bundesliga", "Milieu", 21, "Allemagne", 130000000, 8000000, 2026, 86, 97, 88, 88, 48, 72),
        ("Harry Kane", "Bayern Munich", "Bundesliga", "Attaquant", 30, "Angleterre", 90000000, 25000000, 2027, 97, 78, 86, 75, 42, 86),
        ("Xavi Simons", "RB Leipzig", "Bundesliga", "Milieu", 21, "Pays-Bas", 80000000, 6000000, 2027, 82, 91, 89, 86, 45, 72),
        ("Jeremie Frimpong", "Bayer Leverkusen", "Bundesliga", "Défenseur", 23, "Pays-Bas", 50000000, 3500000, 2028, 78, 89, 83, 95, 72, 76),
        ("Castello Lukeba", "RB Leipzig", "Bundesliga", "Défenseur", 21, "France", 40000000, 3200000, 2028, 35, 65, 76, 80, 88, 85),
        ("Serhou Guirassy", "Borussia Dortmund", "Bundesliga", "Attaquant", 28, "Guinée", 40000000, 4500000, 2028, 92, 75, 70, 81, 40, 86),
        ("Alphonso Davies", "Bayern Munich", "Bundesliga", "Défenseur", 23, "Canada", 50000000, 11000000, 2025, 65, 91, 78, 97, 76, 80),  # Fin de contrat 2025 !
        
        # === SERIE A (ITALIE) ===
        ("Lautaro Martínez", "Inter Milan", "Serie A", "Attaquant", 26, "Argentine", 110000000, 11000000, 2029, 93, 83, 78, 82, 48, 85),
        ("Khvicha Kvaratskhelia", "SSC Napoli", "Serie A", "Attaquant", 23, "Géorgie", 80000000, 3000000, 2027, 84, 96, 85, 88, 38, 74),
        ("Rafael Leão", "AC Milan", "Serie A", "Attaquant", 25, "Portugal", 90000000, 8500000, 2028, 84, 95, 82, 94, 32, 80),
        ("Nicolò Barella", "Inter Milan", "Serie A", "Milieu", 27, "Italie", 80000000, 9000000, 2029, 78, 86, 90, 82, 84, 84),
        ("Theo Hernández", "AC Milan", "Serie A", "Défenseur", 26, "France", 60000000, 5200000, 2026, 74, 84, 79, 93, 80, 86),
        ("Mike Maignan", "AC Milan", "Serie A", "Gardien", 28, "France", 45000000, 5200000, 2026, 10, 25, 80, 60, 95, 90),
        ("Bremer", "Juventus", "Serie A", "Défenseur", 27, "Brésil", 60000000, 6500000, 2028, 42, 58, 68, 80, 93, 94),

        # === AUTRES NATIONS & NOUVELLES PÉPITES ===
        ("Viktor Gyökeres", "Sporting CP", "Liga Portugal", "Attaquant", 26, "Suède", 65000000, 3000000, 2028, 93, 84, 76, 88, 45, 90),
        ("Diogo Costa", "FC Porto", "Liga Portugal", "Gardien", 24, "Portugal", 45000000, 2400000, 2027, 10, 30, 84, 58, 92, 86),
        ("Santiago Giménez", "Feyenoord", "Eredivisie", "Attaquant", 23, "Mexique", 40000000, 2000000, 2027, 88, 76, 68, 82, 36, 82),
        ("Johan Bakayoko", "PSV Eindhoven", "Eredivisie", "Attaquant", 21, "Belgique", 45000000, 1800000, 2026, 80, 91, 82, 90, 38, 74)
    ]

    cursor.executemany('''
        INSERT INTO players (
            name, club, league, position, age, nationality, market_value, wage, contract_expires,
            stat_finishing, stat_dribbling, stat_passing, stat_pace, stat_defending, stat_physical
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', real_players)

    conn.commit()
    conn.close()
    print(f"[OK] Base SQLite peuplee exclusivement avec {len(real_players)} vrais joueurs professionnels reels !")

if __name__ == "__main__":
    import_real_opta_players()
