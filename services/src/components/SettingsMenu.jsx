import { useState } from 'react';
import { Settings } from 'lucide-react';

export default function SettingsMenu({ showAll, setShowAll }) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div style={{ position: 'absolute', top: '170px', right: '10px', zIndex: 1000 }}>
      <button onClick={() => setIsOpen(!isOpen)} style={{ background: '#fff', border: 'none', padding: '5px', borderRadius: '10%', cursor: 'pointer' }}>
        <Settings size={24} />
      </button>

      {isOpen && (
        <div style={{ position: 'absolute', right: 10, border: '1px solid #ccc', padding: '20px', background: '#fff', borderRadius: '8px' }}>
          <label style={{ display: 'flex', alignItems: 'center', gap: '18px' }}>
            <input 
              type="checkbox" 
              checked={showAll} 
              onChange={() => setShowAll(!showAll)} 
            />
            Visa alla
          </label>
        </div>
      )}
    </div>
  );
}