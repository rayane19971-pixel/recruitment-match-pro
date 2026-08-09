import React, { useState, useEffect } from 'react';
import RadarChartCanvas from './RadarChartCanvas';
import ALL_PLAYERS from '../data/players_dataset.json';

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
          // Fallback KNN local sur les 17 660 joueurs (filtré par même poste)
          const candidates = ALL_PLAYERS.filter(p => p.id !== player.id && p.position === player.position);
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
            🤖 Jumeaux Statistiques Opta (Algorithme KNN sur 17 660 joueurs) :
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
