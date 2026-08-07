import React, { useState, useEffect } from 'react';

export default function BudgetDashboard({ token, role }) {
  const [budgetData, setBudgetData] = useState(null);
  const [error, setError] = useState('');
  const [simulatedTransfer, setSimulatedTransfer] = useState(15000000);
  const [simulatedSalary, setSimulatedSalary] = useState(2500000);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/director/budget', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
      .then(res => {
        if (!res.ok) throw new Error("Accès refusé. Réservé aux Directeurs Sportifs et Admin.");
        return res.json();
      })
      .then(data => setBudgetData(data))
      .catch(err => setError(err.message));
  }, [token]);

  if (error) {
    return (
      <div className="glass-card" style={{ textAlign: 'center', padding: '3rem' }}>
        <h3 style={{ color: '#ef4444', marginBottom: '1rem' }}>⛔ Accès Restreint (RBAC)</h3>
        <p style={{ color: '#94a3b8' }}>{error}</p>
        <p style={{ fontSize: '0.85rem', color: '#64748b', marginTop: '1rem' }}>
          Votre rôle actuel (<strong>{role}</strong>) ne vous permet pas de consulter la gestion budgétaire confidentielle du club.
        </p>
      </div>
    );
  }

  const envelopeNum = 45000000;
  const remainingEnvelope = envelopeNum - simulatedTransfer;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      <div className="glass-card">
        <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: '#06b6d4', marginBottom: '0.5rem' }}>
          💰 Espace Direction Sportive & Budget Mercato Pro
        </h2>

        <p style={{ color: '#94a3b8', fontSize: '0.9rem' }}>
          Suivi confidentiel des enveloppes de transfert et simulation de masse salariale.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.5rem' }}>
        <div className="glass-card" style={{ borderLeft: '4px solid #10b981' }}>
          <span style={{ color: '#94a3b8', fontSize: '0.8rem', textTransform: 'uppercase' }}>Enveloppe Transferts Totale</span>
          <h3 style={{ fontSize: '2rem', fontWeight: 900, color: '#10b981', margin: '0.25rem 0' }}>45 000 000 €</h3>
          <span style={{ color: '#64748b', fontSize: '0.75rem' }}>Saison 2026 - Validé par la Direction</span>
        </div>

        <div className="glass-card" style={{ borderLeft: '4px solid #3b82f6' }}>
          <span style={{ color: '#94a3b8', fontSize: '0.8rem', textTransform: 'uppercase' }}>Enveloppe Restante après simulation</span>
          <h3 style={{ fontSize: '2rem', fontWeight: 900, color: remainingEnvelope >= 0 ? '#3b82f6' : '#ef4444', margin: '0.25rem 0' }}>
            {(remainingEnvelope / 1000000).toFixed(1)} M €
          </h3>
          <span style={{ color: '#64748b', fontSize: '0.75rem' }}>Ajustement en temps réel</span>
        </div>

        <div className="glass-card" style={{ borderLeft: '4px solid #e5a93c' }}>
          <span style={{ color: '#94a3b8', fontSize: '0.8rem', textTransform: 'uppercase' }}>Masse Salariale Max</span>
          <h3 style={{ fontSize: '2rem', fontWeight: 900, color: '#e5a93c', margin: '0.25rem 0' }}>12 000 000 € / an</h3>
          <span style={{ color: '#64748b', fontSize: '0.75rem' }}>Plafond DNCG & Droit TV</span>
        </div>
      </div>

      {/* SIMULATEUR DE TRANSFERT */}
      <div className="glass-card">
        <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '1rem', color: 'white' }}>
          🧮 Simulateur d'Impact Financier Mercato :
        </h3>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
          <div className="filter-group">
            <label className="filter-label">
              Montant de Transfert simulé : <span className="slider-val">{(simulatedTransfer / 1000000).toFixed(1)} M €</span>
            </label>
            <input 
              type="range" 
              min="0" 
              max="45000000" 
              step="500000" 
              value={simulatedTransfer}
              onChange={(e) => setSimulatedTransfer(Number(e.target.value))}
            />
          </div>

          <div className="filter-group">
            <label className="filter-label">
              Salaire Annuel Proposé : <span className="slider-val">{(simulatedSalary / 1000000).toFixed(2)} M € / an</span>
            </label>
            <input 
              type="range" 
              min="0" 
              max="10000000" 
              step="100000" 
              value={simulatedSalary}
              onChange={(e) => setSimulatedSalary(Number(e.target.value))}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
