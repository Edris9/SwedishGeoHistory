import { useState } from 'react';
import './Startsida.css';

export default function Startsida({ onStart }) {
  const [role, setRole] = useState('');      // 'student' eller 'larare'
  const [namn, setNamn] = useState('');

  // components/Startsida.jsx  (ändra längst ner i handleStart)
    async function handleStart() {
    if (!role || !namn.trim()) {
        alert('Välj roll och skriv ditt namn tack!');
        return;
    }
    
    // Spara till Supabase via backend
    try {
        await fetch('http://localhost:5007/api/users', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                role: role,
                name: namn.trim()
            })
        });
    } catch (error) {
        console.log('Kunde inte spara användare:', error);
    }

    onStart?.();
}

  return (
    <div className="startsida">
      <div className="gradient-bg" />

      <div className="content">
        <h1>
          Välkommen till <br />
          <span className="highlight">Kartutforskaren</span>
        </h1>

        <div className="form-container">
          <div className="role-buttons">
            <button
              className={`role-btn ${role === 'student' ? 'active' : ''}`}
              onClick={() => setRole('student')}
            >
              Jag är elev / student
            </button>
            <button
              className={`role-btn ${role === 'larare' ? 'active' : ''}`}
              onClick={() => setRole('larare')}
            >
              Jag är lärare
            </button>
          </div>

          {role && (
            <>
              <input
                type="text"
                placeholder="Ditt namn..."
                value={namn}
                onChange={(e) => setNamn(e.target.value)}
                className="namn-input"
              />

              <button className="start-btn" onClick={handleStart}>
                Börja utforska kartan →
              </button>
            </>
          )}
        </div>

        <p className="small-info">
          Jag vill veta vilka som besöker kartan.
        </p>
      </div>
    </div>
  );
}