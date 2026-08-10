import sqlite3
import math

conn = sqlite3.connect(r'C:\Users\user\OneDrive\Documents\web-rayane-ourad-neutre\backend\data\recruitment_app.db')
conn.row_factory = sqlite3.Row
rows = [dict(r) for r in conn.execute('SELECT * FROM players').fetchall()]

targets = [
    'Jude Bellingham',
    'Florian Wirtz',
    'Rayan Cherki',
    'William Saliba',
    'Achraf Hakimi',
    'Gianluigi Donnarumma',
    'Antoine Griezmann'
]

for t in targets:
    matched = [p for p in rows if t.lower() in p['name'].lower()]
    if not matched:
        continue
    target_p = matched[0]
    pVal = math.log10(max(1000000, target_p['market_value']))
    
    candidates = [p for p in rows if p['id'] != target_p['id'] and p['position'] == target_p['position']]
    
    computed = []
    for c in candidates:
        cVal = math.log10(max(1000000, c['market_value']))
        diffStatsSq = (
            math.pow(c['stat_finishing'] - target_p['stat_finishing'], 2) +
            math.pow(c['stat_dribbling'] - target_p['stat_dribbling'], 2) +
            math.pow(c['stat_passing'] - target_p['stat_passing'], 2) +
            math.pow(c['stat_pace'] - target_p['stat_pace'], 2) +
            math.pow(c['stat_defending'] - target_p['stat_defending'], 2) +
            math.pow(c['stat_physical'] - target_p['stat_physical'], 2)
        ) / 6.0
        
        valDiffSq = math.pow((pVal - cVal) * 14.0, 2)
        dist = math.sqrt(diffStatsSq + valDiffSq)
        sim = round(max(0, 99 - dist), 1)
        computed.append((c['name'], c['club'], sim))
        
    computed.sort(key=lambda x: x[2], reverse=True)
    print(f"=== {target_p['name']} ({target_p['club']} - {target_p['position']}) ===")
    for comp in computed[:4]:
        print(f"   -> {comp[0]} ({comp[1]}) : {comp[2]}%")
    print()
