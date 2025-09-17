import React, { useState, useEffect, useRef } from 'react';
import './ImmersiveEnvironment.css';

const ImmersiveEnvironment = ({ 
  environment, 
  onComplete, 
  isActive = false,
  userInput = ""
}) => {
  const [currentPhase, setCurrentPhase] = useState('entering'); // entering, experiencing, completing
  const [breathingCycle, setBreathingCycle] = useState('inhale');
  const [cycleCount, setCycleCount] = useState(0);
  const [timeRemaining, setTimeRemaining] = useState(0);
  const [isBreathingActive, setIsBreathingActive] = useState(false);
  const [userReflection, setUserReflection] = useState('');
  const [showReflectionPrompt, setShowReflectionPrompt] = useState(false);
  
  const timerRef = useRef(null);
  const breathingRef = useRef(null);
  const audioRef = useRef(null);

  useEffect(() => {
    if (isActive && environment) {
      setTimeRemaining(environment.suggestedDuration * 60); // Converter para segundos
      setCurrentPhase('entering');
      
      // Iniciar timer de entrada
      setTimeout(() => {
        setCurrentPhase('experiencing');
        startBreathingGuide();
      }, 3000);
    }

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
      if (breathingRef.current) clearInterval(breathingRef.current);
    };
  }, [isActive, environment]);

  useEffect(() => {
    if (currentPhase === 'experiencing' && timeRemaining > 0) {
      timerRef.current = setInterval(() => {
        setTimeRemaining(prev => {
          if (prev <= 1) {
            setCurrentPhase('completing');
            setShowReflectionPrompt(true);
            stopBreathingGuide();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    }

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [currentPhase, timeRemaining]);

  const startBreathingGuide = () => {
    if (!environment?.breathingPattern) return;
    
    setIsBreathingActive(true);
    const { inhale, hold, exhale } = environment.breathingPattern;
    let phase = 'inhale';
    let phaseTime = 0;
    
    breathingRef.current = setInterval(() => {
      phaseTime++;
      
      if (phase === 'inhale' && phaseTime >= inhale) {
        phase = 'hold';
        phaseTime = 0;
        setBreathingCycle('hold');
      } else if (phase === 'hold' && phaseTime >= hold) {
        phase = 'exhale';
        phaseTime = 0;
        setBreathingCycle('exhale');
      } else if (phase === 'exhale' && phaseTime >= exhale) {
        phase = 'inhale';
        phaseTime = 0;
        setBreathingCycle('inhale');
        setCycleCount(prev => prev + 1);
      }
    }, 1000);
  };

  const stopBreathingGuide = () => {
    setIsBreathingActive(false);
    if (breathingRef.current) {
      clearInterval(breathingRef.current);
    }
  };

  const handleReflectionSubmit = () => {
    const experienceData = {
      environment: environment.emotion,
      intensity: environment.intensity,
      duration: environment.suggestedDuration,
      breathingCycles: cycleCount,
      userReflection,
      userInput,
      timestamp: new Date().toISOString(),
      completed: true
    };

    if (onComplete) {
      onComplete(experienceData);
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const getBreathingInstruction = () => {
    const instructions = {
      inhale: `Inspire (${environment?.breathingPattern?.inhale}s)`,
      hold: `Segure (${environment?.breathingPattern?.hold}s)`,
      exhale: `Expire (${environment?.breathingPattern?.exhale}s)`
    };
    return instructions[breathingCycle] || 'Respire naturalmente';
  };

  const getPhaseContent = () => {
    switch (currentPhase) {
      case 'entering':
        return (
          <div className="phase-entering">
            <div className="environment-preview">
              <h2>Preparando seu espaço de presença...</h2>
              <p className="environment-description">{environment?.description}</p>
              <div className="loading-animation">
                <div className="pulse-circle"></div>
              </div>
            </div>
          </div>
        );

      case 'experiencing':
        return (
          <div className="phase-experiencing">
            <div className="environment-display">
              <div 
                className="environment-background"
                style={{
                  background: `linear-gradient(135deg, ${environment?.colors?.join(', ') || '#87CEEB, #E6F3FF'})`
                }}
              >
                <div className="environment-overlay">
                  <div className="breathing-guide">
                    <div className={`breathing-circle ${breathingCycle} ${isBreathingActive ? 'active' : ''}`}>
                      <div className="breathing-inner">
                        <span className="breathing-instruction">
                          {getBreathingInstruction()}
                        </span>
                        <div className="cycle-counter">
                          Ciclo {cycleCount}
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div className="environment-text">
                    <p className="environment-description">{environment?.description}</p>
                    <div className="mantra-display">
                      <em>"{environment?.mantra || 'Respire e esteja presente neste momento'}"</em>
                    </div>
                  </div>
                  
                  <div className="session-info">
                    <div className="time-remaining">
                      {formatTime(timeRemaining)}
                    </div>
                    <div className="breathing-pattern-name">
                      {environment?.breathingPattern?.name}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        );

      case 'completing':
        return (
          <div className="phase-completing">
            <div className="completion-content">
              <h2>Experiência Concluída</h2>
              <div className="session-summary">
                <p>Você completou {cycleCount} ciclos de respiração</p>
                <p>Duração: {environment?.suggestedDuration} minutos</p>
                <p>Emoção trabalhada: {environment?.emotion}</p>
              </div>
              
              {showReflectionPrompt && (
                <div className="reflection-prompt">
                  <h3>Como você se sente agora?</h3>
                  <textarea
                    value={userReflection}
                    onChange={(e) => setUserReflection(e.target.value)}
                    placeholder="Compartilhe como esta experiência te afetou..."
                    className="reflection-textarea"
                    rows={4}
                  />
                  <div className="completion-actions">
                    <button 
                      onClick={handleReflectionSubmit}
                      className="complete-button"
                    >
                      Finalizar Experiência
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  if (!isActive || !environment) {
    return null;
  }

  return (
    <div className="immersive-environment">
      <div className="environment-container">
        {getPhaseContent()}
        
        <div className="environment-controls">
          <button 
            onClick={() => setIsBreathingActive(!isBreathingActive)}
            className="breathing-toggle"
          >
            {isBreathingActive ? 'Pausar Respiração' : 'Retomar Respiração'}
          </button>
          
          <button 
            onClick={() => {
              setCurrentPhase('completing');
              setShowReflectionPrompt(true);
              stopBreathingGuide();
            }}
            className="skip-button"
          >
            Finalizar Agora
          </button>
        </div>
      </div>
      
      {/* Audio element for ambient sounds (placeholder) */}
      <audio ref={audioRef} loop>
        {/* Aqui seriam carregados os sons ambientais baseados em environment.sounds */}
      </audio>
    </div>
  );
};

export default ImmersiveEnvironment;


