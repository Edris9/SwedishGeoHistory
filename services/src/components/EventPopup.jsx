import { useState } from 'react';
import './EventPopup.css';

export default function EventPopup({ event, onClose }) {
    const [expanded, setExpanded] = useState(false);

    if (!event) return null;

    return (
        <div className="event-overlay">
            <div className="event-popup">
                <button className="event-close-btn" onClick={onClose}>✕</button>
                
                <h2 className="event-title">{event.title}</h2>
                <p className="event-meta">{event.year} • {event.area || 'Sverige'}</p>
                
                <p className="event-description">
                    {expanded 
                        ? event.description 
                        : event.description?.slice(0, 150) + '...'
                    }
                </p>
                
                <button className="event-more-btn" onClick={() => setExpanded(!expanded)}>
                    {expanded ? 'Visa mindre' : 'Visa mer'}
                </button>
            </div>
        </div>
    );
}