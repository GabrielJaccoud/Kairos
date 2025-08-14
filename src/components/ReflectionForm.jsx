import React, { useState, useEffect } from 'react';
import './ReflectionForm.css';

const ReflectionForm = ({ 
  initialData = null, 
  onSave, 
  onCancel,
  isLoading = false 
}) => {
  const [formData, setFormData] = useState({
    gratitude: '',
    forgiveness: '',
    learning: '',
    overcoming: '',
    day_rating: 5,
    presence_level: 5,
    energy_level: 5
  });

  const [currentStep, setCurrentStep] = useState(0);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (initialData) {
      setFormData({
        gratitude: initialData.gratitude || '',
        forgiveness: initialData.forgiveness || '',
        learning: initialData.learning || '',
        overcoming: initialData.overcoming || '',
        day_rating: initialData.day_rating || 5,
        presence_level: initialData.presence_level || 5,
        energy_level: initialData.energy_level || 5
      });
    }
  }, [initialData]);

  const reflectionSteps = [
    {
      key: 'gratitude',
      title: 'Gratidão',
      icon: '🙏',
      question: 'Pelo que você é grato hoje?',
      placeholder: 'Reflita sobre os momentos, pessoas ou experiências que trouxeram alegria ao seu dia...',
      color: '#27AE60'
    },
    {
      key: 'forgiveness',
      title: 'Perdão',
      icon: '💚',
      question: 'O que você precisa perdoar ou liberar?',
      placeholder: 'Pense em situações, pessoas (incluindo você mesmo) que precisam de perdão para trazer paz...',
      color: '#8BC34A'
    },
    {
      key: 'learning',
      title: 'Aprendizado',
      icon: '🌱',
      question: 'O que você aprendeu hoje?',
      placeholder: 'Considere insights, descobertas ou lições que contribuíram para seu crescimento...',
      color: '#F1C40F'
    },
    {
      key: 'overcoming',
      title: 'Superação',
      icon: '💪',
      question: 'Que desafios você superou hoje?',
      placeholder: 'Reconheça os obstáculos que enfrentou e como você os atravessou com coragem...',
      color: '#E67E22'
    }
  ];

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleNext = () => {
    if (currentStep < reflectionSteps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      setCurrentStep(reflectionSteps.length); // Vai para a tela de ratings
    }
  };

  const handlePrevious = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleSubmit = async () => {
    setIsSubmitting(true);
    try {
      await onSave(formData);
    } finally {
      setIsSubmitting(false);
    }
  };

  const getRatingLabel = (value, type) => {
    const labels = {
      day_rating: {
        1: 'Muito difícil', 2: 'Difícil', 3: 'Desafiador', 4: 'Regular', 5: 'Ok',
        6: 'Bom', 7: 'Muito bom', 8: 'Ótimo', 9: 'Excelente', 10: 'Perfeito'
      },
      presence_level: {
        1: 'Muito disperso', 2: 'Disperso', 3: 'Pouco presente', 4: 'Às vezes presente', 5: 'Moderadamente presente',
        6: 'Presente', 7: 'Bem presente', 8: 'Muito presente', 9: 'Altamente presente', 10: 'Completamente presente'
      },
      energy_level: {
        1: 'Exausto', 2: 'Muito cansado', 3: 'Cansado', 4: 'Baixa energia', 5: 'Energia moderada',
        6: 'Boa energia', 7: 'Muita energia', 8: 'Alta energia', 9: 'Energia elevada', 10: 'Energia máxima'
      }
    };
    return labels[type][value] || '';
  };

  const isStepComplete = (stepIndex) => {
    if (stepIndex >= reflectionSteps.length) return true;
    const step = reflectionSteps[stepIndex];
    return formData[step.key].trim().length > 0;
  };

  const currentStepData = reflectionSteps[currentStep];
  const isRatingStep = currentStep >= reflectionSteps.length;

  return (
    <div className="reflection-form">
      {/* Progress Bar */}
      <div className="progress-container">
        <div className="progress-bar">
          <div 
            className="progress-fill"
            style={{ 
              width: `${((currentStep + 1) / (reflectionSteps.length + 1)) * 100}%` 
            }}
          />
        </div>
        <div className="progress-text">
          {currentStep + 1} de {reflectionSteps.length + 1}
        </div>
      </div>

      <div className="form-content">
        {!isRatingStep ? (
          /* Reflection Steps */
          <div className="reflection-step" key={currentStepData.key}>
            <div 
              className="step-header"
              style={{ background: `linear-gradient(135deg, ${currentStepData.color}, ${currentStepData.color}dd)` }}
            >
              <div className="step-icon">{currentStepData.icon}</div>
              <div className="step-info">
                <h2 className="step-title">{currentStepData.title}</h2>
                <p className="step-question">{currentStepData.question}</p>
              </div>
            </div>

            <div className="step-content">
              <textarea
                value={formData[currentStepData.key]}
                onChange={(e) => handleInputChange(currentStepData.key, e.target.value)}
                placeholder={currentStepData.placeholder}
                className="reflection-textarea"
                rows={6}
                autoFocus
              />
              
              <div className="character-count">
                {formData[currentStepData.key].length} caracteres
              </div>
            </div>
          </div>
        ) : (
          /* Rating Step */
          <div className="rating-step">
            <div className="rating-header">
              <div className="step-icon">📊</div>
              <div className="step-info">
                <h2 className="step-title">Avaliação do Dia</h2>
                <p className="step-question">Como foi seu dia em diferentes aspectos?</p>
              </div>
            </div>

            <div className="ratings-container">
              <div className="rating-item">
                <label className="rating-label">
                  <span className="rating-icon">⭐</span>
                  Avaliação Geral do Dia
                </label>
                <div className="rating-slider">
                  <input
                    type="range"
                    min="1"
                    max="10"
                    value={formData.day_rating}
                    onChange={(e) => handleInputChange('day_rating', parseInt(e.target.value))}
                    className="slider"
                  />
                  <div className="rating-display">
                    <span className="rating-value">{formData.day_rating}</span>
                    <span className="rating-text">{getRatingLabel(formData.day_rating, 'day_rating')}</span>
                  </div>
                </div>
              </div>

              <div className="rating-item">
                <label className="rating-label">
                  <span className="rating-icon">🧘‍♀️</span>
                  Nível de Presença
                </label>
                <div className="rating-slider">
                  <input
                    type="range"
                    min="1"
                    max="10"
                    value={formData.presence_level}
                    onChange={(e) => handleInputChange('presence_level', parseInt(e.target.value))}
                    className="slider presence"
                  />
                  <div className="rating-display">
                    <span className="rating-value">{formData.presence_level}</span>
                    <span className="rating-text">{getRatingLabel(formData.presence_level, 'presence_level')}</span>
                  </div>
                </div>
              </div>

              <div className="rating-item">
                <label className="rating-label">
                  <span className="rating-icon">⚡</span>
                  Nível de Energia
                </label>
                <div className="rating-slider">
                  <input
                    type="range"
                    min="1"
                    max="10"
                    value={formData.energy_level}
                    onChange={(e) => handleInputChange('energy_level', parseInt(e.target.value))}
                    className="slider energy"
                  />
                  <div className="rating-display">
                    <span className="rating-value">{formData.energy_level}</span>
                    <span className="rating-text">{getRatingLabel(formData.energy_level, 'energy_level')}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Navigation */}
      <div className="form-navigation">
        <button
          type="button"
          onClick={onCancel}
          className="nav-btn cancel-btn"
        >
          Cancelar
        </button>

        <div className="nav-buttons">
          {currentStep > 0 && (
            <button
              type="button"
              onClick={handlePrevious}
              className="nav-btn previous-btn"
            >
              ← Anterior
            </button>
          )}

          {!isRatingStep ? (
            <button
              type="button"
              onClick={handleNext}
              className={`nav-btn next-btn ${!isStepComplete(currentStep) ? 'disabled' : ''}`}
              disabled={!isStepComplete(currentStep)}
            >
              Próximo →
            </button>
          ) : (
            <button
              type="button"
              onClick={handleSubmit}
              className={`nav-btn submit-btn ${isSubmitting ? 'submitting' : ''}`}
              disabled={isSubmitting}
            >
              {isSubmitting ? (
                <>
                  <div className="spinner"></div>
                  Salvando...
                </>
              ) : (
                'Salvar Reflexão'
              )}
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default ReflectionForm;

