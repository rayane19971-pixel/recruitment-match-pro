import React, { useState, useEffect } from 'react';
import ALL_PLAYERS from '../data/players_dataset.json';

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
          // Fallback recherche locale sur les 17 660 joueurs pour Vercel
          const q = searchTerm.toLowerCase();
          const matches = ALL_PLAYERS.filter(p => p.name && p.name.toLowerCase().includes(q)).slice(0, 20);
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
        placeholder="🔍 Rechercher un joueur parmi 17 660 (ex: Cherki, Mbappé, Barcola, Lacazette, Bellingham)..."
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
