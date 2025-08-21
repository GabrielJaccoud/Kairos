import React from 'react';
import './BadgeDisplay.css';

const BadgeDisplay = ({ badges }) => {
  return (
    <div className="badge-display-container">
      <h2>Suas Insígnias de Consciência</h2>
      <div className="badges-grid">
        {badges.map(badge => (
          <div key={badge.id} className={`badge-card ${badge.unlocked ? 'unlocked' : 'locked'}`}>
            <div className="badge-icon">{badge.icon}</div>
            <h3>{badge.name}</h3>
            <p>{badge.description}</p>
            {!badge.unlocked && <span className="badge-locked-overlay">🔒</span>}
          </div>
        ))}
      </div>
    </div>
  );
};

export default BadgeDisplay;


