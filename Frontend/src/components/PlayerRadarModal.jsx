import React, { useState, useEffect } from 'react';
import RadarChartCanvas from './RadarChartCanvas';

const SAMPLE_PLAYERS_KNN = [
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
  { id: 11, name: "Lucas Paquetá", club: "West Ham", league: "Premier League", position: "Milieu", age: 26, nationality: "Brésil", market_value: 65000000, wage: 8500000, contract_expires: 2027, stat_finishing: 78, stat_dribbling: 87, stat_passing: 86, stat_pace: 75, stat_defending: 68, stat_physical: 78 }
];

export default function PlayerRadarModal({ player, token, role, onClose, onSelectPlayer }) {
  const [similarPlayers, setSimilarPlayers] = useState([]);
  const [loadingKnn, setLoadingKnn] = useState(false);

  useEffect(() => {
    if (player) {
      setLoadingKnn(true);
      fetch(`http://127.0.0.1:8000/players/${player.id || 1}/similar?k=4`, {
        headers: { 'Authorization': `Bearer ${token}` }
      })
        .then(res => {
          if (!res.ok) throw new Error("API non joignable");
          return res.json();
        })
        .then(data => {
          if (data && data.voisins_similaires) {
            setSimilarPlayers(data.voisins_similaires);
          }
          setLoadingKnn(false);
        })
        .catch(err => {
          // Fallback KNN local client-side pour Vercel
          const candidates = SAMPLE_PLAYERS_KNN.filter(p => p.id !== player.id);
          const computed = candidates.map(c => {
            const diffSq = (
              Math.pow(c.stat_finishing - (player.stat_finishing || 50), 2) +
              Math.pow(c.stat_dribbling - (player.stat_dribbling || 50), 2) +
              Math.pow(c.stat_passing - (player.stat_passing || 50), 2) +
              Math.pow(c.stat_pace - (player.stat_pace || 50), 2) +
              Math.pow(c.stat_defending - (player.stat_defending || 50), 2) +
              Math.pow(c.stat_physical - (player.stat_physical || 50), 2)
            );
            const dist = Math.sqrt(diffSq / 6);
            const sim = Math.round(Math.max(0, 100 - dist) * 10) / 10;
            return { ...c, similarity_score: sim };
          });
          computed.sort((a, b) => b.similarity_score - a.similarity_score);
          setSimilarPlayers(computed.slice(0, 4));
          setLoadingKnn(false);
        });
    }
  }, [player, token]);

  if (!player) return null;

  const isScout = role === 'scout';

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>&times;</button>
        
        <div style={{ marginBottom: '1rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <h2 style={{ fontSize: '1.5rem', fontWeight: 800 }}>{player.name}</h2>
              <p style={{ color: '#94a3b8', fontSize: '0.9rem' }}>
                {player.club} ({player.league || 'Ligue 1'}) — {player.position}
              </p>
            </div>
            {player.score_compatibilite && (
              <span className="match-badge">
                {player.score_compatibilite}
              </span>
            )}
          </div>
        </div>

        {/* RADAR CANVAS */}
        <RadarChartCanvas player={player} />

        {/* FINANCIAL & CONTRACT INFO */}
        <div className="player-meta" style={{ marginTop: '1rem' }}>
          <div className="meta-item">
            <span>Âge & Nationalité</span>
            <strong>{player.age} ans ({player.nationality})</strong>
          </div>
          <div className="meta-item">
            <span>Fin de Contrat</span>
            <strong style={{ color: player.contract_expires <= 2026 ? '#f59e0b' : 'white' }}>
              {player.contract_expires}
            </strong>
          </div>
          <div className="meta-item">
            <span>Valeur Marchande</span>
            <strong>
              {!isScout && typeof player.market_value === 'number' 
                ? `${(player.market_value / 1000000).toFixed(1)} M €` 
                : <span className="confidential-tag">Confidentiel (Réservé Direction)</span>}
            </strong>
          </div>
          <div className="meta-item">
            <span>Salaire Annuel</span>
            <strong>
              {!isScout && typeof player.wage === 'number' 
                ? `${(player.wage / 1000000).toFixed(2)} M € / an` 
                : <span className="confidential-tag">Confidentiel (Réservé Direction)</span>}
            </strong>
          </div>
        </div>

        {/* KNN SIMILAR PLAYERS (JUMEAUX STATISTIQUES) */}
        <div style={{ marginTop: '1.5rem', borderTop: '1px solid rgba(255,255,255,0.08)', paddingTop: '1rem' }}>
          <h4 style={{ fontSize: '0.95rem', color: '#06b6d4', marginBottom: '0.75rem' }}>
            🤖 Jumeaux Statistiques Opta (Algorithme KNN) :
          </h4>
          {loadingKnn ? (
            <p style={{ fontSize: '0.8rem', color: '#64748b' }}>Calcul KNN en cours...</p>
          ) : (
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem' }}>
              {similarPlayers.map((sim) => (
                <div 
                  key={sim.id}
                  onClick={() => onSelectPlayer(sim)}
                  style={{
                    background: 'rgba(255,255,255,0.03)',
                    border: '1px solid rgba(255,255,255,0.06)',
                    padding: '8px 12px',
                    borderRadius: '8px',
                    cursor: 'pointer',
                    fontSize: '0.8rem',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center'
                  }}
                >
                  <div>
                    <strong style={{ display: 'block', color: 'white' }}>{sim.name}</strong>
                    <span style={{ color: '#64748b', fontSize: '0.7rem' }}>{sim.club}</span>
                  </div>
                  <span style={{ color: '#10b981', fontWeight: 'bold' }}>{sim.similarity_score}%</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
