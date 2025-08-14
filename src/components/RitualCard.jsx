import React, { useState } from 'react';
import './RitualCard.css';

const RitualCard = ({ 
  ritual, 
  onExecute, 
  onEdit, 
  onToggleActive,
  stats = null 
}) => {
  const [isExecuting, setIsExecuting] = useState(false);
  const [showDetails, setShowDetails] = useState(false);

  const ritualIcons = {
    morning: '🌅',
    evening: '🌙',
    break: '⏸️',
    custom: '✨'
  };

  const handleExecute = async () => {
    if (isExecuting) return;
    
    setIsExecuting(true);
    try {
      await onExecute(ritual);
    } finally {
      setIsExecuting(false);
    }
  };

  const formatTime = (timeString) => {
    if (!timeString) return null;
    return new Date(`2000-01-01T${timeString}`).toLocaleTimeString('pt-BR', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getConsistencyColor = (score) => {
    if (score >= 80) return '#27AE60';
    if (score >= 60) return '#F1C40F';
    return '#E74C3C';
  };

  return (
    <div className={`ritual-card ${!ritual.is_active ? 'inactive' : ''}`}>
      <div className="ritual-header">
        <div className="ritual-icon">
          {ritualIcons[ritual.ritual_type] || ritualIcons.custom}
        </div>
        <div className="ritual-info">
          <h3 className="ritual-name">{ritual.name}</h3>
          <p className="ritual-description">{ritual.description}</p>
        </div>
        <div className="ritual-actions">
          <button
            className="toggle-active-btn"
            onClick={() => onToggleActive(ritual.id, !ritual.is_active)}
            title={ritual.is_active ? 'Desativar ritual' : 'Ativar ritual'}
          >
            {ritual.is_active ? '⏸️' : '▶️'}
          </button>
          <button
            className="edit-btn"
            onClick={() => onEdit(ritual)}
            title="Editar ritual"
          >
            ✏️
          </button>
        </div>
      </div>

      <div className="ritual-details">
        <div className="detail-item">
          <span className="detail-label">Duração:</span>
          <span className="detail-value">{ritual.duration_minutes} min</span>
        </div>
        
        {ritual.scheduled_time && (
          <div className="detail-item">
            <span className="detail-label">Horário:</span>
            <span className="detail-value">{formatTime(ritual.scheduled_time)}</span>
          </div>
        )}
        
        <div className="detail-item">
          <span className="detail-label">Frequência:</span>
          <span className="detail-value">
            {ritual.frequency === 'daily' ? 'Diário' : 
             ritual.frequency === 'weekly' ? 'Semanal' : 'Personalizado'}
          </span>
        </div>
      </div>

      {stats && (
        <div className="ritual-stats">
          <div className="stat-item">
            <div className="stat-value">{stats.total_executions}</div>
            <div className="stat-label">Execuções</div>
          </div>
          <div className="stat-item">
            <div className="stat-value">{stats.average_rating}/5</div>
            <div className="stat-label">Avaliação</div>
          </div>
          <div className="stat-item">
            <div 
              className="stat-value"
              style={{ color: getConsistencyColor(stats.consistency_score) }}
            >
              {stats.consistency_score}%
            </div>
            <div className="stat-label">Consistência</div>
          </div>
        </div>
      )}

      {showDetails && ritual.instructions && (
        <div className="ritual-instructions">
          <h4>Instruções:</h4>
          <div className="instructions-content">
            {ritual.instructions.split('\n').map((line, index) => (
              <p key={index}>{line}</p>
            ))}
          </div>
        </div>
      )}

      <div className="ritual-footer">
        <button
          className="details-btn"
          onClick={() => setShowDetails(!showDetails)}
        >
          {showDetails ? 'Ocultar Detalhes' : 'Ver Instruções'}
        </button>
        
        {ritual.is_active && (
          <button
            className={`execute-btn ${isExecuting ? 'executing' : ''}`}
            onClick={handleExecute}
            disabled={isExecuting}
          >
            {isExecuting ? (
              <>
                <div className="spinner"></div>
                Executando...
              </>
            ) : (
              <>
                <span className="execute-icon">🧘‍♀️</span>
                Executar Ritual
              </>
            )}
          </button>
        )}
      </div>
    </div>
  );
};

export default RitualCard;

