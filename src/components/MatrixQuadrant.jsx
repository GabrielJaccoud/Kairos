import React, { useState } from 'react';
import './MatrixQuadrant.css';

const MatrixQuadrant = ({ 
  quadrant, 
  tasks = [], 
  onTaskClick, 
  onAddTask, 
  className = '' 
}) => {
  const [isHovered, setIsHovered] = useState(false);

  const quadrantConfig = {
    urgent_important: {
      title: 'Urgente + Importante',
      subtitle: 'Crises e emergências',
      color: '#8B1538',
      icon: '🚨',
      gradient: 'linear-gradient(135deg, #8B1538, #A0173F)'
    },
    important_not_urgent: {
      title: 'Importante + Não Urgente',
      subtitle: 'Planejamento e prevenção',
      color: '#B8860B',
      icon: '⭐',
      gradient: 'linear-gradient(135deg, #B8860B, #DAA520)'
    },
    urgent_not_important: {
      title: 'Urgente + Não Importante',
      subtitle: 'Interrupções e distrações',
      color: '#CD853F',
      icon: '⚡',
      gradient: 'linear-gradient(135deg, #CD853F, #D2691E)'
    },
    not_urgent_not_important: {
      title: 'Não Urgente + Não Importante',
      subtitle: 'Atividades triviais',
      color: '#F4E4BC',
      icon: '📝',
      gradient: 'linear-gradient(135deg, #F4E4BC, #F5DEB3)'
    },
    presence: {
      title: 'Eixo da Presença',
      subtitle: 'Improvisos conscientes',
      color: '#8B4513',
      icon: '🌟',
      gradient: 'linear-gradient(135deg, #8B4513, #A0522D)'
    }
  };

  const config = quadrantConfig[quadrant] || quadrantConfig.presence;

  return (
    <div 
      className={`matrix-quadrant ${className}`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      style={{
        background: config.gradient,
        transform: isHovered ? 'translateY(-2px)' : 'translateY(0)',
        boxShadow: isHovered 
          ? `0 8px 25px ${config.color}30` 
          : `0 4px 15px ${config.color}20`
      }}
    >
      <div className="quadrant-header">
        <div className="quadrant-icon">{config.icon}</div>
        <div className="quadrant-info">
          <h3 className="quadrant-title">{config.title}</h3>
          <p className="quadrant-subtitle">{config.subtitle}</p>
        </div>
        <div className="task-count">{tasks.length}</div>
      </div>

      <div className="quadrant-content">
        {tasks.length === 0 ? (
          <div className="empty-state">
            <p>Nenhuma tarefa neste quadrante</p>
            <button 
              className="add-task-btn"
              onClick={() => onAddTask && onAddTask(quadrant)}
            >
              + Adicionar Tarefa
            </button>
          </div>
        ) : (
          <div className="tasks-list">
            {tasks.slice(0, 3).map((task, index) => (
              <div 
                key={task.id || index}
                className="task-item"
                onClick={() => onTaskClick && onTaskClick(task)}
              >
                <div className="task-content">
                  <h4 className="task-title">{task.title}</h4>
                  {task.scheduled_for && (
                    <span className="task-time">
                      {new Date(task.scheduled_for).toLocaleTimeString('pt-BR', {
                        hour: '2-digit',
                        minute: '2-digit'
                      })}
                    </span>
                  )}
                  {task.contacts && JSON.parse(task.contacts).length > 0 && (
                    <div className="task-contacts">
                      {JSON.parse(task.contacts).slice(0, 2).map((contact, i) => (
                        <span key={i} className="contact-avatar">
                          {contact.charAt(0).toUpperCase()}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
                {task.ai_priority_score && (
                  <div className="priority-indicator">
                    <div 
                      className="priority-bar"
                      style={{
                        width: `${task.ai_priority_score * 100}%`,
                        backgroundColor: task.ai_priority_score > 0.7 ? '#E74C3C' : 
                                        task.ai_priority_score > 0.4 ? '#F1C40F' : '#8BC34A'
                      }}
                    />
                  </div>
                )}
              </div>
            ))}
            
            {tasks.length > 3 && (
              <div className="more-tasks">
                +{tasks.length - 3} mais tarefas
              </div>
            )}
          </div>
        )}
      </div>

      {onAddTask && tasks.length > 0 && (
        <button 
          className="floating-add-btn"
          onClick={() => onAddTask(quadrant)}
          title="Adicionar nova tarefa"
        >
          +
        </button>
      )}
    </div>
  );
};

export default MatrixQuadrant;

