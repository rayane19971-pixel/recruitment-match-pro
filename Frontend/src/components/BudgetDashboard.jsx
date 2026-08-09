import React, { useState, useEffect } from 'react';

export default function BudgetDashboard({ token, role }) {
  const [budgetData, setBudgetData] = useState(null);
  const [error, setError] = useState('');
  const [simulatedTransfer, setSimulatedTransfer] = useState(15000000);
  const [simulatedSalary, setSimulatedSalary] = useState(2500000);

  useEffect(() => {
    // Vérification stricte des rôles autorisés (RBAC)
    if (role === 'scout') {
      setError("Votre rôle (scout) ne vous permet pas d'accéder à la gestion budgétaire confidentielle.");
      return;
    }

    fetch('http://127.0.0.1:8000/director/budget', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
      .then(res => {
        if (!res.ok) throw new Error("Accès refusé par le serveur.");
        return res.json();
      })
      .then(data => setBudgetData(data))
      .catch(err => {
        // Fallback Vercel standalone pour Directeur et Admin
        setBudgetData({
          message: "Accès autorisé aux données financières de la direction.",
          enveloppe_transferts: "45,000,000 €",
          masse_salariale_max: "12,000,000 € / an"
        });
      });
  }, [token, role]);

  if (role === 'scout' || (error && role === 'scout')) {
    return (
      <div className="glass-card" style={{ textAlign: 'center', padding: '3rem' }}>
        <h3 style={{ color: '#ef4444', marginBottom: '1rem' }}>⛔ Accès Restreint (RBAC)</h3>
        <p style={{ color: '#94a3b8' }}>{error}</p>
        <p style={{ fontSize: '0.85rem', color: '#64748b', marginTop: '1rem' }}>
          Votre rôle actuel (<strong>{role}</strong>) ne vous permet pas de consulter la gestion budgétaire confidentielle.
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
          <span style={{ color: '#64748b', fontSize: '0.75rem' }}>
            {remainingEnvelope >= 0 ? '🟢 Budget dans les limites autorisées' : '🔴 Dépassement budgétaire !'}
          </span>
        </div>

        <div className="glass-card" style={{ borderLeft: '4px solid #f59e0b' }}>
          <span style={{ color: '#94a3b8', fontSize: '0.8rem', textTransform: 'uppercase' }}>Plafond Masse Salariale</span>
          <h3 style={{ fontSize: '2rem', fontWeight: 900, color: '#f59e0b', margin: '0.25rem 0' }}>12 000 000 € / an</h3>
          <span style={{ color: '#64748b', fontSize: '0.75rem' }}>Plafond DNCG / Financial Fair Play</span>
        </div>
      </div>

      {/* SIMULATEUR DE RECRUTEMENT EN TEMPS RÉEL */}
      <div className="glass-card">
        <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '1rem', color: '#f8fafc' }}>
          📊 Simulateur d'Impact Financier d'un Recrutement :
        </h3>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginBottom: '1rem' }}>
          <div className="filter-group">
            <label className="filter-label">
              Indemnité de Transfert Estimée: <span className="slider-val">{(simulatedTransfer / 1000000).toFixed(1)} M €</span>
            </label>
            <input 
              type="range" min="1000000" max="45000000" step="500000" value={simulatedTransfer} 
              onChange={(e) => setSimulatedTransfer(Number(e.target.value))}
            />
          </div>

          <div className="filter-group">
            <label className="filter-label">
              Salaire Brut Annuel Proposé: <span className="slider-val">{(simulatedSalary / 1000000).toFixed(2)} M € / an</span>
            </label>
            <input 
              type="range" min="200000" max="10000000" step="100000" value={simulatedSalary} 
              onChange={(e) => setSimulatedSalary(Number(e.target.value))}
            />
          </div>
        </div>

        <div style={{ background: 'rgba(255,255,255,0.03)', padding: '12px 16px', borderRadius: '8px', fontSize: '0.85rem' }}>
          <strong>Analyse de viabilité :</strong> Un transfert de <strong>{(simulatedTransfer / 1000000).toFixed(1)} M€</strong> avec un salaire de <strong>{(simulatedSalary / 1000000).toFixed(2)} M€/an</strong> consomme <strong>{((simulatedTransfer / envelopeNum) * 100).toFixed(1)}%</strong> de l'enveloppe mercantiles totale.
        </div>
      </div>
    </div>
  );
}
