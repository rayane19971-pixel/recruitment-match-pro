import React, { useState, useEffect } from 'react';

const SAMPLE_PLAYERS_SEARCH = [
  { id: 1, name: "Kylian Mbappé", club: "Real Madrid", league: "LaLiga", position: "Attaquant", age: 25, nationality: "France", market_value: 180000000, wage: 30000000, contract_expires: 2029, stat_finishing: 93, stat_dribbling: 92, stat_passing: 80, stat_pace: 97, stat_defending: 36, stat_physical: 78 },
  { id: 2, name: "Erling Haaland", club: "Manchester City", league: "Premier League", position: "Attaquant", age: 24, nationality: "Norvège", market_value: 180000000, wage: 25000000, contract_expires: 2027, stat_finishing: 94, stat_dribbling: 80, stat_passing: 65, stat_pace: 89, stat_defending: 45, stat_physical: 88 },
  { id: 3, name: "Rayan Cherki", club: "Olympique Lyonnais", league: "Ligue 1", position: "Milieu", age: 21, nationality: "France", market_value: 25000000, wage: 2400000, contract_expires: 2026, stat_finishing: 75, stat_dribbling: 89, stat_passing: 84, stat_pace: 78, stat_defending: 38, stat_physical: 65 },
  { id: 4, name: "Alexandre Lacazette", club: "Olympique Lyonnais", league: "Ligue 1", position: "Attaquant", age: 33, nationality: "France", market_value: 10000000, wage: 6000000, contract_expires: 2025, stat_finishing: 85, stat_dribbling: 78, stat_passing: 76, stat_pace: 72, stat_defending: 44, stat_physical: 76 },
  { id: 5, name: "Bradley Barcola", club: "Paris SG", league: "Ligue 1", position: "Attaquant", age: 21, nationality: "France", market_value: 50000000, wage: 4500000, contract_expires: 2028, stat_finishing: 78, stat_dribbling: 86, stat_passing: 75, stat_pace: 91, stat_defending: 40, stat_physical: 70 },
  { id: 6, name: "Jude Bellingham", club: "Real Madrid", league: "LaLiga", position: "Milieu", age: 21, nationality: "Angleterre", market_value: 180000000, wage: 20000000, contract_expires: 2029, stat_finishing: 86, stat_dribbling: 88, stat_passing: 85, stat_pace: 82, stat_defending: 78, stat_physical: 85 },
  { id: 7, name: "William Saliba", club: "Arsenal", league: "Premier League", position: "Défenseur", age: 23, nationality: "France", market_value: 80000000, wage: 9000000, contract_expires: 2027, stat_finishing: 35, stat_dribbling: 72, stat_passing: 78, stat_pace: 82, stat_defending: 88, stat_physical: 86 },
  { id: 8, name: "Achraf Hakimi", club: "Paris SG", league: "Ligue 1", position: "Défenseur", age: 25, nationality: "Maroc", market_value: 60000000, wage: 10000000, contract_expires: 2026, stat_finishing: 72, stat_dribbling: 82, stat_passing: 80, stat_pace: 92, stat_defending: 76, stat_physical: 78 },
  { id: 9, name: "Georges Mikautadze", club: "Olympique Lyonnais", league: "Ligue 1", position: "Attaquant", age: 23, nationality: "Géorgie", market_value: 20000000, wage: 3000000, contract_expires: 2028, stat_finishing: 82, stat_dribbling: 81, stat_passing: 72, stat_pace: 80, stat_defending: 35, stat_physical: 72 },
  { id: 10, name: "Malick Fofana", club: "Olympique Lyonnais", league: "Ligue 1", position: "Attaquant", age: 19, nationality: "Belgique", market_value: 15000000, wage: 1800000, contract_expires: 2028, stat_finishing: 74, stat_dribbling: 85, stat_passing: 70, stat_pace: 89, stat_defending: 32, stat_physical: 66 },
  { id: 11, name: "Lucas Paquetá", club: "West Ham", league: "Premier League", position: "Milieu", age: 26, nationality: "Brésil", market_value: 65000000, wage: 8500000, contract_expires: 2027, stat_finishing: 78, stat_dribbling: 87, stat_passing: 86, stat_pace: 75, stat_defending: 68, stat_physical: 78 },
  { id: 12, name: "Gianluigi Donnarumma", club: "Paris SG", league: "Ligue 1", position: "Gardien", age: 25, nationality: "Italie", market_value: 40000000, wage: 12000000, contract_expires: 2026, stat_finishing: 15, stat_dribbling: 25, stat_passing: 60, stat_pace: 50, stat_defending: 89, stat_physical: 82 }
];

export default function PlayerSearchBar({ token, onSelectPlayer }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    if (searchTerm.trim().length < 2) {
      setSuggestions([]);
      setIsOpen(false);
      return;
    }

    const timer = setTimeout(() => {
      fetch(`http://127.0.0.1:8000/players/search?query=${encodeURIComponent(searchTerm)}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      })
        .then(res => {
          if (!res.ok) throw new Error("API non joignable");
          return res.json();
        })
        .then(data => {
          if (data && data.joueurs) {
            setSuggestions(data.joueurs);
            setIsOpen(true);
          }
        })
        .catch(err => {
          // Fallback recherche locale pour Vercel
          const q = searchTerm.toLowerCase();
          const matches = SAMPLE_PLAYERS_SEARCH.filter(p => p.name.toLowerCase().includes(q));
          setSuggestions(matches);
          setIsOpen(true);
        });
    }, 150);

    return () => clearTimeout(timer);
  }, [searchTerm, token]);

  return (
    <div style={{ position: 'relative', width: '100%', marginBottom: '1.25rem' }}>
      <input
        type="text"
        placeholder="🔍 Rechercher directement un joueur par son nom (ex: Cherki, Mbappé, Barcola, Lacazette, Bellingham)..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        style={{
          width: '100%',
          padding: '12px 18px',
          borderRadius: '12px',
          border: '1px solid rgba(255, 255, 255, 0.15)',
          background: 'rgba(15, 23, 42, 0.75)',
          color: 'white',
          fontSize: '0.92rem',
          outline: 'none',
          boxShadow: '0 4px 15px rgba(0, 0, 0, 0.2)'
        }}
      />

      {isOpen && suggestions.length > 0 && (
        <div style={{
          position: 'absolute',
          top: '100%',
          left: 0,
          right: 0,
          background: '#1e293b',
          border: '1px solid rgba(255,255,255,0.15)',
          borderRadius: '12px',
          marginTop: '6px',
          maxHeight: '300px',
          overflowY: 'auto',
          zIndex: 1000,
          boxShadow: '0 15px 35px rgba(0,0,0,0.6)'
        }}>
          {suggestions.map((p) => (
            <div
              key={p.id}
              onClick={() => {
                onSelectPlayer(p);
                setIsOpen(false);
                setSearchTerm('');
              }}
              style={{
                padding: '12px 16px',
                borderBottom: '1px solid rgba(255,255,255,0.06)',
                cursor: 'pointer',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                transition: 'background 0.15s ease'
              }}
              onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(79, 70, 229, 0.4)'}
              onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
            >
              <div>
                <strong style={{ color: 'white', display: 'block', fontSize: '0.95rem' }}>{p.name}</strong>
                <span style={{ color: '#94a3b8', fontSize: '0.78rem' }}>{p.club} • {p.position}</span>
              </div>
              <span style={{ color: '#06b6d4', fontSize: '0.8rem', fontWeight: 600 }}>{p.age} ans ({p.nationality})</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
