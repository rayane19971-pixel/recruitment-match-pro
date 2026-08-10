import React, { useState } from 'react';

export default function ScoutingFilters({ onSearch, loading }) {
  const [position, setPosition] = useState('Tous');
  const [maxAge, setMaxAge] = useState(38);
  const [maxContractYear, setMaxContractYear] = useState(2030);
  const [maxMarketValue, setMaxMarketValue] = useState(200); // en M€
  
  // State Opta local (ouvert pour charger les joueurs immédiatement)
  const [finishing, setFinishing] = useState(40);
  const [dribbling, setDribbling] = useState(40);
  const [passing, setPassing] = useState(40);
  const [pace, setPace] = useState(40);
  const [defending, setDefending] = useState(30);
  const [physical, setPhysical] = useState(40);

  const handleSubmit = (e) => {
    if (e) e.preventDefault();
    onSearch({
      position,
      maxAge,
      maxContractYear,
      maxMarketValue,
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

      <div className="filters-row" style={{ marginTop: '0.5rem' }}>
        <div className="filter-group">
          <label className="filter-label">
            Fin contrat max: <span className="slider-val">{maxContractYear}</span>
          </label>
          <input 
            type="range" min="2025" max="2032" value={maxContractYear} 
            onChange={(e) => setMaxContractYear(Number(e.target.value))}
          />
        </div>

        <div className="filter-group">
          <label className="filter-label">
            Valeur Max: <span className="slider-val">{maxMarketValue >= 200 ? 'Illimitée' : `${maxMarketValue} M€`}</span>
          </label>
          <input 
            type="range" min="5" max="200" step="5" value={maxMarketValue} 
            onChange={(e) => setMaxMarketValue(Number(e.target.value))}
          />
        </div>
      </div>

      <hr style={{ borderColor: 'rgba(255,255,255,0.08)', margin: '1rem 0' }} />

      <h4 style={{ fontSize: '0.78rem', color: '#06b6d4', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
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

      <button 
        className="btn-primary" 
        style={{ width: '100%', marginTop: '1.2rem', padding: '12px' }}
        onClick={handleSubmit}
        disabled={loading}
      >
        {loading ? 'Calcul Opta en cours...' : '🔍 Lancer le Matching Opta'}
      </button>
    </div>
  );
}
