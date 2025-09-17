import React, { useState, useEffect } from 'react';
import './PresencePoints.css';

const PresencePoints = ({ 
  currentPoints = 0, 
  recentActivities = [], 
  onPointsUpdate,
  showDetails = false 
}) => {
  const [displayPoints, setDisplayPoints] = useState(currentPoints);
  const [animatingPoints, setAnimatingPoints] = useState(0);
  const [showPointsAnimation, setShowPointsAnimation] = useState(false);
  const [presenceLevel, setPresenceLevel] = useState(1);
  const [progressToNext, setProgressToNext] = useState(0);

  // Sistema de níveis baseado em presença
  const presenceLevels = [
    { level: 1, name: "Despertar", minPoints: 0, maxPoints: 100, color: "#E8F4FD" },
    { level: 2, name: "Consciência", minPoints: 100, maxPoints: 300, color: "#B8E6B8" },
    { level: 3, name: "Presença", minPoints: 300, maxPoints: 600, color: "#87CEEB" },
    { level: 4, name: "Serenidade", minPoints: 600, maxPoints: 1000, color: "#DDA0DD" },
    { level: 5, name: "Sabedoria", minPoints: 1000, maxPoints: 1500, color: "#F0E68C" },
    { level: 6, name: "Transcendência", minPoints: 1500, maxPoints: 2500, color: "#FFB6C1" },
    { level: 7, name: "Iluminação", minPoints: 2500, maxPoints: 5000, color: "#98FB98" },
    { level: 8, name: "Mestre da Presença", minPoints: 5000, maxPoints: Infinity, color: "#FFD700" }
  ];

  // Tipos de atividades e seus valores de pontos
  const activityPoints = {
    // Reflexão Diária
    daily_reflection_basic: 10,
    daily_reflection_deep: 25,
    daily_reflection_transformative: 50,
    
    // Rituais
    morning_ritual_completed: 15,
    evening_ritual_completed: 15,
    custom_ritual_completed: 20,
    ritual_consistency_bonus: 30, // 7 dias consecutivos
    
    // Matriz de Presença
    task_completed_mindfully: 5,
    urgent_important_handled: 15,
    presence_axis_choice: 25,
    matrix_review_completed: 10,
    
    // Experiências Imersivas
    immersive_experience_completed: 30,
    breathing_session_completed: 20,
    emotional_processing_session: 35,
    
    // Crescimento Pessoal
    insight_recorded: 15,
    pattern_recognized: 20,
    breakthrough_moment: 50,
    
    // Conexão Social
    gratitude_expressed: 10,
    compassion_practiced: 15,
    conflict_resolved_mindfully: 25,
    
    // Consistência e Hábitos
    weekly_consistency_bonus: 100,
    monthly_milestone: 200,
    presence_streak_7_days: 75,
    presence_streak_30_days: 300
  };

  useEffect(() => {
    // Calcular nível atual baseado nos pontos
    const currentLevel = presenceLevels.find(level => 
      currentPoints >= level.minPoints && currentPoints < level.maxPoints
    ) || presenceLevels[presenceLevels.length - 1];

    setPresenceLevel(currentLevel.level);

    // Calcular progresso para o próximo nível
    if (currentLevel.maxPoints !== Infinity) {
      const progress = ((currentPoints - currentLevel.minPoints) / 
                       (currentLevel.maxPoints - currentLevel.minPoints)) * 100;
      setProgressToNext(Math.min(progress, 100));
    } else {
      setProgressToNext(100);
    }

    // Animar mudança de pontos
    if (currentPoints !== displayPoints) {
      const pointsDiff = currentPoints - displayPoints;
      setAnimatingPoints(pointsDiff);
      setShowPointsAnimation(true);
      
      // Animar contagem
      const duration = 1500;
      const steps = 30;
      const increment = pointsDiff / steps;
      let step = 0;
      
      const timer = setInterval(() => {
        step++;
        setDisplayPoints(prev => {
          const newValue = prev + increment;
          return step === steps ? currentPoints : Math.round(newValue);
        });
        
        if (step === steps) {
          clearInterval(timer);
          setTimeout(() => setShowPointsAnimation(false), 500);
        }
      }, duration / steps);
    }
  }, [currentPoints, displayPoints]);

  const getCurrentLevelInfo = () => {
    return presenceLevels.find(level => level.level === presenceLevel) || presenceLevels[0];
  };

  const getNextLevelInfo = () => {
    return presenceLevels.find(level => level.level === presenceLevel + 1);
  };

  const calculateActivityPoints = (activity) => {
    return activityPoints[activity.type] || 0;
  };

  const getActivityDescription = (activity) => {
    const descriptions = {
      daily_reflection_basic: "Reflexão diária básica",
      daily_reflection_deep: "Reflexão profunda",
      daily_reflection_transformative: "Reflexão transformadora",
      morning_ritual_completed: "Ritual matinal concluído",
      evening_ritual_completed: "Ritual noturno concluído",
      custom_ritual_completed: "Ritual personalizado",
      ritual_consistency_bonus: "Bônus de consistência (7 dias)",
      task_completed_mindfully: "Tarefa concluída com presença",
      urgent_important_handled: "Crise gerenciada com sabedoria",
      presence_axis_choice: "Escolha consciente no Eixo da Presença",
      matrix_review_completed: "Revisão da matriz concluída",
      immersive_experience_completed: "Experiência imersiva concluída",
      breathing_session_completed: "Sessão de respiração",
      emotional_processing_session: "Processamento emocional",
      insight_recorded: "Insight registrado",
      pattern_recognized: "Padrão reconhecido",
      breakthrough_moment: "Momento de breakthrough",
      gratitude_expressed: "Gratidão expressa",
      compassion_practiced: "Compaixão praticada",
      conflict_resolved_mindfully: "Conflito resolvido com consciência",
      weekly_consistency_bonus: "Bônus semanal de consistência",
      monthly_milestone: "Marco mensal alcançado",
      presence_streak_7_days: "Sequência de 7 dias de presença",
      presence_streak_30_days: "Sequência de 30 dias de presença"
    };
    
    return descriptions[activity.type] || activity.type;
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 1) return "Hoje";
    if (diffDays === 2) return "Ontem";
    if (diffDays <= 7) return `${diffDays - 1} dias atrás`;
    return date.toLocaleDateString('pt-BR');
  };

  const currentLevelInfo = getCurrentLevelInfo();
  const nextLevelInfo = getNextLevelInfo();

  return (
    <div className="presence-points">
      <div className="points-header">
        <div className="points-display">
          <div className="points-number">
            {displayPoints.toLocaleString()}
            {showPointsAnimation && (
              <span className={`points-animation ${animatingPoints > 0 ? 'positive' : 'negative'}`}>
                {animatingPoints > 0 ? '+' : ''}{animatingPoints}
              </span>
            )}
          </div>
          <div className="points-label">Pontos de Presença</div>
        </div>
        
        <div className="level-display">
          <div 
            className="level-badge"
            style={{ backgroundColor: currentLevelInfo.color }}
          >
            <span className="level-number">{currentLevelInfo.level}</span>
            <span className="level-name">{currentLevelInfo.name}</span>
          </div>
        </div>
      </div>

      <div className="progress-section">
        <div className="progress-info">
          <span className="current-level">{currentLevelInfo.name}</span>
          {nextLevelInfo && (
            <>
              <span className="progress-arrow">→</span>
              <span className="next-level">{nextLevelInfo.name}</span>
            </>
          )}
        </div>
        
        <div className="progress-bar">
          <div 
            className="progress-fill"
            style={{ 
              width: `${progressToNext}%`,
              backgroundColor: currentLevelInfo.color 
            }}
          />
        </div>
        
        {nextLevelInfo && (
          <div className="progress-text">
            {nextLevelInfo.minPoints - currentPoints} pontos para o próximo nível
          </div>
        )}
      </div>

      {showDetails && (
        <div className="points-details">
          <h3>Atividades Recentes</h3>
          <div className="activities-list">
            {recentActivities.length > 0 ? (
              recentActivities.slice(0, 10).map((activity, index) => (
                <div key={index} className="activity-item">
                  <div className="activity-info">
                    <span className="activity-description">
                      {getActivityDescription(activity)}
                    </span>
                    <span className="activity-date">
                      {formatDate(activity.timestamp)}
                    </span>
                  </div>
                  <div className="activity-points">
                    +{calculateActivityPoints(activity)}
                  </div>
                </div>
              ))
            ) : (
              <div className="no-activities">
                <p>Nenhuma atividade recente</p>
                <p className="no-activities-hint">
                  Complete reflexões, rituais ou use a matriz para ganhar pontos!
                </p>
              </div>
            )}
          </div>
        </div>
      )}

      <div className="points-philosophy">
        <p className="philosophy-text">
          "Os Pontos de Presença não medem quantidade, mas qualidade. 
          Cada ponto representa um momento de consciência genuína, 
          um instante de presença autêntica em sua jornada."
        </p>
      </div>
    </div>
  );
};

export default PresencePoints;


