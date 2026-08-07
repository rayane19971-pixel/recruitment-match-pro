import csv
import re
import os
from database import get_connection, create_db

def parse_currency(val_str):
    """Convertit des chaînes comme '€91M', '€115K', '€500' en chiffres réels (float/int)."""
    if not val_str or val_str == 'nan' or val_str == '0':
        return 0
    val_str = str(val_str).replace('€', '').strip()
    multiplier = 1
    if 'M' in val_str:
        multiplier = 1000000
        val_str = val_str.replace('M', '')
    elif 'K' in val_str:
        multiplier = 1000
        val_str = val_str.replace('K', '')
    try:
        return int(float(val_str) * multiplier)
    except ValueError:
        return 0

def parse_contract_year(contract_str):
    """Extrait l'année de fin de contrat (ex: 2026, 2025)."""
    if not contract_str or contract_str == 'nan':
        return 2026
    match = re.search(r'(202\d|203\d)', str(contract_str))
    if match:
        return int(match.group(1))
    return 2026

def map_position(pos_str):
    """Mappe les postes FIFA (ST, RW, CM, LB, GK...) vers nos 4 catégories principales."""
    pos_str = str(pos_str).upper()
    if any(p in pos_str for p in ['GK', 'GOALKEEPER']):
        return 'Gardien'
    elif any(p in pos_str for p in ['CB', 'LB', 'RB', 'LWB', 'RWB', 'DEFENDER']):
        return 'Défenseur'
    elif any(p in pos_str for p in ['CM', 'CAM', 'CDM', 'LM', 'RM', 'MIDFIELDER']):
        return 'Milieu'
    else:
        return 'Attaquant'

def import_fifa_official_csv():
    csv_file = "FIFA23_official_data.csv"
    if not os.path.exists(csv_file):
        print(f"Erreur : Le fichier {csv_file} est introuvable.")
        return

    create_db()
    conn = get_connection()
    cursor = conn.cursor()
    
    print("Videz de la base et import des 17,600+ VRAIS joueurs FIFA...")
    cursor.execute("DELETE FROM players")
    
    inserted_count = 0
    batch = []
    
    with open(csv_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('Name', '').strip()
            if not name:
                continue
                
            club = row.get('Club', 'Libre').strip()
            if club == 'nan' or not club:
                club = "Libre"
                
            nationality = row.get('Nationality', 'Inconnue').strip()
            league = "International"
            
            try:
                age = int(row.get('Age', 24))
            except ValueError:
                age = 24
                
            overall = int(float(row.get('Overall', 65)))
            position = map_position(row.get('Position', 'Attaquant'))
            market_value = parse_currency(row.get('Value', '0'))
            wage = parse_currency(row.get('Wage', '0')) * 52  # Hebdomadaire -> Annuel (52 semaines)
            if wage == 0 and market_value > 0:
                wage = int(market_value * 0.08)
                
            contract_expires = parse_contract_year(row.get('Contract Valid Until', '2026'))
            
            # Ajustement des percentiles Opta selon l'Overall réel FIFA et la spécialité par poste
            if position == "Attaquant":
                finishing = min(99, max(30, overall + 5))
                dribbling = min(99, max(30, overall + 2))
                passing = min(99, max(30, overall - 5))
                pace = min(99, max(30, overall + 4))
                defending = min(99, max(20, overall - 25))
                physical = min(99, max(30, overall - 2))
            elif position == "Milieu":
                finishing = min(99, max(30, overall - 5))
                dribbling = min(99, max(30, overall + 3))
                passing = min(99, max(30, overall + 6))
                pace = min(99, max(30, overall - 2))
                defending = min(99, max(30, overall - 5))
                physical = min(99, max(30, overall))
            elif position == "Défenseur":
                finishing = min(99, max(20, overall - 20))
                dribbling = min(99, max(30, overall - 10))
                passing = min(99, max(30, overall - 5))
                pace = min(99, max(30, overall - 2))
                defending = min(99, max(30, overall + 8))
                physical = min(99, max(30, overall + 6))
            else:  # Gardien
                finishing = 15
                dribbling = 20
                passing = min(99, max(30, overall - 15))
                pace = 50
                defending = min(99, max(30, overall + 10))
                physical = min(99, max(30, overall + 5))
                
            batch.append((
                name, club, league, position, age, nationality, market_value, wage, contract_expires,
                finishing, dribbling, passing, pace, defending, physical
            ))
            
            if len(batch) >= 1000:
                cursor.executemany('''
                    INSERT INTO players (
                        name, club, league, position, age, nationality, market_value, wage, contract_expires,
                        stat_finishing, stat_dribbling, stat_passing, stat_pace, stat_defending, stat_physical
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', batch)
                inserted_count += len(batch)
                batch = []
                
        if batch:
            cursor.executemany('''
                INSERT INTO players (
                    name, club, league, position, age, nationality, market_value, wage, contract_expires,
                    stat_finishing, stat_dribbling, stat_passing, stat_pace, stat_defending, stat_physical
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', batch)
            inserted_count += len(batch)

    conn.commit()
    conn.close()
    print(f"[OK] {inserted_count} VRAIS joueurs FIFA officiels importés avec succès dans SQLite !")

if __name__ == "__main__":
    import_fifa_official_csv()
