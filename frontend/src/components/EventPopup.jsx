import { useState } from 'react';
import './EventPopup.css';

export default function EventPopup({ event, onClose }) {
  const [expanded, setExpanded] = useState(false);

  if (!event) return null;

  const shortDesc = event.description?.slice(0, 250) + (event.description?.length > 250 ? '...' : '');

  return (
    <div className="event-overlay">
      <div className="event-popup">
        <button className="event-close-btn" onClick={onClose} aria-label="Stäng">
          ✕
        </button>

        <h2 className="event-title">{event.title}</h2>
        <p className="event-meta">
          {event.year} • {event.area || 'Sverige'}
        </p>

        <div className="event-description-wrapper">
          <p className="event-description">
            {expanded ? event.description : shortDesc}
          </p>
        </div>

        <div className="event-actions">
          {event.sourceUrl && (
            <a
              href={event.sourceUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="event-source-link"
            >
              <span className="link-icon">↗</span>
              Läs mer på källan
            </a>
          )}

          {(event.description?.length > 250 || expanded) && (
            <button
              className="event-more-btn"
              onClick={() => setExpanded(!expanded)}
            >
              {expanded ? 'Visa mindre' : 'Visa mer'}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}