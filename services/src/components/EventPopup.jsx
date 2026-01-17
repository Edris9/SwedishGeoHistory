import { useState } from 'react';

export default function EventPopup({ event, onClose }) {
    const [expanded, setExpanded] = useState(false);

    if (!event) return null;

    return (
        <div style={styles.overlay}>
            <div style={styles.popup}>
                <button style={styles.closeBtn} onClick={onClose}>✕</button>
                
                <h2 style={styles.title}>{event.title}</h2>
                <p style={styles.meta}>{event.year} • {event.area || 'Sverige'}</p>
                
                <p style={styles.description}>
                    {expanded 
                        ? event.description 
                        : event.description?.slice(0, 150) + '...'
                    }
                </p>
                
                <button style={styles.moreBtn} onClick={() => setExpanded(!expanded)}>
                    {expanded ? 'Visa mindre' : 'Visa mer'}
                </button>
            </div>
        </div>
    );
}

const styles = {
    overlay: {
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        background: 'rgba(0,0,0,0.5)',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        zIndex: 1000
    },
    popup: {
        background: '#1a1a2e',
        color: '#fff',
        padding: '30px',
        borderRadius: '15px',
        maxWidth: '400px',
        position: 'relative'
    },
    closeBtn: {
        position: 'absolute',
        top: '10px',
        right: '15px',
        background: 'none',
        border: 'none',
        color: '#fff',
        fontSize: '20px',
        cursor: 'pointer'
    },
    title: {
        margin: '0 0 10px 0'
    },
    meta: {
        color: '#888',
        marginBottom: '15px'
    },
    description: {
        lineHeight: '1.6'
    },
    moreBtn: {
        marginTop: '15px',
        padding: '10px 20px',
        background: '#ff4444',
        border: 'none',
        borderRadius: '8px',
        color: '#fff',
        cursor: 'pointer'
    }
};