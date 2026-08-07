import React, { useState } from 'react';

export default function ScoutingFilters({ onSearch, loading }) {
  const [position, setPosition] = useState('Tous');
  const [maxAge, setMaxAge] = useState(30);
  const [maxContractYear, setMaxContractYear] = useState(2030);
  
  // State Opta local (isole le composant pour éviter les re-renders inutiles de la grille)
  const [finishing, setFinishing] = useState(70);
  const [dribbling, setDribbling] = useState(70);
  const [passing, setPassing] = useState(70);
  const [pace, setPace] = useState(75);
  const [defending, setDefending] = useState(50);
  const [physical, setPhysical] = useState(65);

  const handleSubmit = (e) => {
    if (e) e.preventDefault();
    onSearch({
      position,
      maxAge,
      maxContractYear,
      finishing,
      dribbling,
      passing,
      pace,
      defending,
      physical
    });
  };

  return (
    <div className="glass-card filter-panel">
      <h3 className="panel-title">🎛️ Filtres & Curseurs Opta</h3>

      <div className="filters-row">
        <div className="filter-group">
          <label className="filter-label">Poste</label>
          <select value={position} onChange={(e) => setPosition(e.target.value)}>
            <option value="Tous">Tous</option>
            <option value="Attaquant">Attaquant</option>
            <option value="Milieu">Milieu</option>
            <option value="Défenseur">Défenseur</option>
            <option value="Gardien">Gardien</option>
          </select>
        </div>

        <div className="filter-group">
          <label className="filter-label">
            Âge max: <span className="slider-val">{maxAge} ans</span>
          </label>
          <input 
            type="range" min="16" max="38" value={maxAge} 
            onChange={(e) => setMaxAge(Number(e.target.value))}
          />
        </div>
      </div>

      <div className="filter-group">
        <label className="filter-label">
          Fin de contrat max: <span className="slider-val">{maxContractYear}</span>
        </label>
        <input 
          type="range" min="2025" max="2032" value={maxContractYear} 
          onChange={(e) => setMaxContractYear(Number(e.target.value))}
        />
      </div>

      <hr style={{ borderColor: 'rgba(255,255,255,0.08)' }} />

      <h4 style={{ fontSize: '0.78rem', color: '#e5a93c', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
        Profil Statistiques Opta (0 - 100) :
      </h4>

      {/* GRILLE COMPACTE ET ULTRA-RAPIDE DE CURSEURS OPTA */}
      <div className="sliders-grid">
        <div className="filter-group-compact">
          <label className="filter-label-compact">
            Finition <span className="slider-val">{finishing}</span>
          </label>
          <input 
            type="range" min="0" max="100" value={finishing} 
            onChange={(e) => setFinishing(Number(e.target.value))}
          />
        </div>

        <div className="filter-group-compact">
          <label className="filter-label-compact">
            Dribble <span className="slider-val">{dribbling}</span>
          </label>
          <input 
            type="range" min="0" max="100" value={dribbling} 
            onChange={(e) => setDribbling(Number(e.target.value))}
          />
        </div>

        <div className="filter-group-compact">
          <label className="filter-label-compact">
            Passes <span className="slider-val">{passing}</span>
          </label>
          <input 
            type="range" min="0" max="100" value={passing} 
            onChange={(e) => setPassing(Number(e.target.value))}
          />
        </div>

        <div className="filter-group-compact">
          <label className="filter-label-compact">
            Vitesse <span className="slider-val">{pace}</span>
          </label>
          <input 
            type="range" min="0" max="100" value={pace} 
            onChange={(e) => setPace(Number(e.target.value))}
          />
        </div>

        <div className="filter-group-compact">
          <label className="filter-label-compact">
            Défense <span className="slider-val">{defending}</span>
          </label>
          <input 
            type="range" min="0" max="100" value={defending} 
            onChange={(e) => setDefending(Number(e.target.value))}
          />
        </div>

        <div className="filter-group-compact">
          <label className="filter-label-compact">
            Physique <span className="slider-val">{physical}</span>
          </label>
          <input 
            type="range" min="0" max="100" value={physical} 
            onChange={(e) => setPhysical(Number(e.target.value))}
          />
        </div>
      </div>

      <button className="btn-primary" onClick={handleSubmit} disabled={loading} style={{ marginTop: '0.5rem', width: '100%', padding: '12px' }}>
        {loading ? 'Calcul en cours...' : '🔍 Lancer le Matching Opta'}
      </button>
    </div>
  );
}
