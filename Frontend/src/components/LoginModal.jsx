import React, { useState } from 'react';

export default function LoginModal({ onLoginSuccess }) {
  const [username, setUsername] = useState('rayane');
  const [password, setPassword] = useState('Admin_Rayane');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const formData = new URLSearchParams();
      formData.append('username', username);
      formData.append('password', password);

      const response = await fetch('http://127.0.0.1:8000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData,
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || 'Identifiants incorrects');
      }

      const data = await response.json();
      onLoginSuccess(data.access_token, data.role, data.username);
    } catch (err) {
      // 🛡️ MODE DEMO EN LIGNE (Vérification stricte des identifiants sur Vercel)
      console.warn("Backend local non joignable, authentification sur identifiants stricts Vercel:", err);
      
      const u = username.trim().toLowerCase();
      const p = password.trim();

      if (u === 'rayane' && p === 'Admin_Rayane') {
        onLoginSuccess('demo_token_admin', 'admin', 'rayane');
      } else if (u === 'directeur' && p === 'Director_OL') {
        onLoginSuccess('demo_token_director', 'director', 'directeur');
      } else if (u === 'scout1' && p === 'Scout_OL') {
        onLoginSuccess('demo_token_scout', 'scout', 'scout1');
      } else {
        setError('Identifiants incorrects. Veuillez utiliser un des comptes de test autorisés ci-dessous.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-card login-box">
      <div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
        <div 
          className="badge-logo" 
          style={{ width: '60px', height: '60px', margin: '0 auto 1rem auto', fontSize: '1.4rem' }}
        >
          PRO
        </div>
        <h2 style={{ fontSize: '1.5rem', fontWeight: 800 }}>RECRUITMENT MATCH PRO</h2>
        <p style={{ color: '#94a3b8', fontSize: '0.85rem', marginTop: '4px' }}>
          Plateforme SaaS de Scouting & Data Intelligence
        </p>
      </div>

      {error && (
        <div style={{ 
          background: 'rgba(244, 63, 94, 0.15)', 
          border: '1px solid #f43f5e', 
          color: '#f43f5e', 
          padding: '10px 14px', 
          borderRadius: '8px', 
          fontSize: '0.85rem',
          marginBottom: '1rem'
        }}>
          ⚠️ {error}
        </div>
      )}

      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        <div className="filter-group">
          <label className="filter-label">Nom d'utilisateur</label>
          <input 
            type="text" 
            value={username} 
            onChange={(e) => setUsername(e.target.value)} 
            placeholder="Pseudo"
            required
          />
        </div>

        <div className="filter-group">
          <label className="filter-label">Mot de passe</label>
          <input 
            type="password" 
            value={password} 
            onChange={(e) => setPassword(e.target.value)} 
            placeholder="Mot de passe"
            required
          />
        </div>

        <button type="submit" className="btn-primary" disabled={loading} style={{ marginTop: '0.5rem' }}>
          {loading ? 'Connexion en cours...' : 'Se connecter'}
        </button>

        <div style={{ marginTop: '1rem', background: 'rgba(255,255,255,0.03)', padding: '10px', borderRadius: '8px', fontSize: '0.75rem', color: '#94a3b8' }}>
          <strong style={{ color: '#06b6d4', display: 'block', marginBottom: '4px' }}>Comptes de démonstration pré-remplis :</strong>
          • Admin : <code>rayane</code> / <code>Admin_Rayane</code><br/>
          • Directeur Sportif : <code>directeur</code> / <code>Director_OL</code><br/>
          • Recruteur Scout : <code>scout1</code> / <code>Scout_OL</code>
        </div>
      </form>
    </div>
  );
}
