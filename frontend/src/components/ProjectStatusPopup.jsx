import { useState, useEffect } from 'react';
import './ProjectStatusPopup.css';

export default function ProjectStatusPopup({ onClose }) {
  const [visible, setVisible] = useState(true);

  if (!visible) return null;

  return (
    <div className="status-overlay">
      <div className="status-popup">
        <h2> Projektstatus</h2>

        <div className="status-content">
          <div className="status-section done">
            <h3>✅ KLART</h3>
            <ul>
              <li>Backend API (C#/.NET)</li>
              <li>Scraper (Python/Wikipedia)</li>
              <li>3D-jordglob (MapTiler)</li>
              <li>Klickbara händelser</li>
              <li>Startsida (roll + namn)</li>
              <li>Timeline-slider</li>
              <li>Kategorier (färgkodade prickar)</li>
            </ul>
          </div>

          <div className="status-section todo">
            <h3>🔧 KVAR</h3>
            <ul>
              <li>Hastighetsoptimering</li>
              <li>Spridning av "Sverige"-händelser</li>
              <li>AI-röst (Web Speech API)</li>
              <li>Språkstöd (EN/AR/FA)</li>
              <li>Lärarportal (felrapportering)</li>
            </ul>
          </div>
        </div>

        <button className="status-ok-btn" onClick={() => {
          // localStorage.setItem('hasSeenProjectStatus', 'true'); // uncommenta om du vill spara
          onClose();
        }}>
          OK
        </button>
      </div>
    </div>
  );
}