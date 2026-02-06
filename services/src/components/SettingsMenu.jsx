import { useState } from 'react';
import { Settings } from 'lucide-react';
import './SettingsMenu.css';

export default function SettingsMenu({ showAll, setShowAll, categories, setCategories }) {
  const [isOpen, setIsOpen] = useState(false);

  const toggleCategory = (category) => {
    setCategories(prev => ({
      ...prev,
      [category]: !prev[category]
    }));
  };

  return (
    <div className="settings-container">
      <button 
        onClick={() => setIsOpen(!isOpen)} 
        className="settings-button"
      >
        <Settings size={24} />
      </button>

      {isOpen && (
          <div className="settings-menu">
          
          {/* Visa alla */}
          <label className="settings-label">
            <input 
              type="checkbox" 
              checked={showAll} 
              onChange={() => setShowAll(!showAll)}
              className="settings-checkbox"
            />
            <span>Visa alla</span>
          </label>

          <hr className="settings-divider" />

          {/* Kategorier */}
          <p className="settings-category-title">Kategori</p>

          {/* Innan Kristus */}
          <label className="settings-category-label">
            <span className="color-indicator color-indicator-red"></span>
            <input 
              type="checkbox" 
              checked={categories?.innanKristus ?? true} 
              onChange={() => toggleCategory('innanKristus')}
              className="settings-checkbox-hidden"
            />
            <span>Innan Kristus</span>
          </label>

          {/* Krig och konflikt */}
          <label className="settings-category-label">
            <span className="color-indicator color-indicator-blue"></span>
            <input 
              type="checkbox" 
              checked={categories?.krigOchKonflikt ?? true} 
              onChange={() => toggleCategory('krigOchKonflikt')}
              className="settings-checkbox-hidden"
            />
            <span>Krig och konflikt</span>
          </label>

          {/* Lägg till fler kategorier här */}
          
        </div>
      )}
    </div>
  );
}