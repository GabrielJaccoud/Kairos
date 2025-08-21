import React, { useState, useEffect } from 'react';
import './ScenarioSimulator.css';

const ScenarioSimulator = ({ 
  onScenarioComplete, 
  userEmotionalState = null,
  isActive = false 
}) => {
  const [currentScenario, setCurrentScenario] = useState(null);
  const [scenarioPhase, setScenarioPhase] = useState('setup'); // setup, presenting, choosing, reflecting, completed
  const [userChoice, setUserChoice] = useState(null);
  const [userReflection, setUserReflection] = useState('');
  const [scenarioHistory, setScenarioHistory] = useState([]);
  const [showFeedback, setShowFeedback] = useState(false);

  // Biblioteca de cenários categorizados por emoção/situação
  const scenarioLibrary = {
    ansiedade: [
      {
        id: 'work_deadline',
        title: 'Prazo Apertado no Trabalho',
        context: 'Você tem uma apresentação importante em 2 horas e ainda não terminou de preparar. Seu chefe acabou de enviar mais três tarefas "urgentes".',
        situation: 'Você está no seu escritório, sentindo o coração acelerar. O que você faz primeiro?',
        choices: [
          {
            id: 'panic_rush',
            text: 'Entro em pânico e tento fazer tudo ao mesmo tempo',
            presenceLevel: 1,
            consequence: 'Você se sente mais ansioso e comete erros. A qualidade do trabalho diminui.',
            feedback: 'O pânico raramente nos ajuda a ser mais eficientes. Que tal uma pausa para respirar?'
          },
          {
            id: 'prioritize_breathe',
            text: 'Paro, respiro fundo e priorizo as tarefas',
            presenceLevel: 4,
            consequence: 'Você se sente mais centrado e consegue focar no que realmente importa.',
            feedback: 'Excelente! A presença nos permite ver com clareza mesmo sob pressão.'
          },
          {
            id: 'communicate_boundaries',
            text: 'Comunico ao chefe sobre o conflito de prioridades',
            presenceLevel: 5,
            consequence: 'Seu chefe aprecia a transparência e ajuda a redefinir as prioridades.',
            feedback: 'Comunicação consciente é um ato de coragem e sabedoria. Você honrou suas limitações.'
          }
        ],
        environment: 'Busy office with papers scattered, computer screen glowing, clock ticking loudly',
        learningFocus: 'Gestão de ansiedade e priorização consciente'
      },
      {
        id: 'social_anxiety',
        title: 'Ansiedade Social em Evento',
        context: 'Você está em um evento de networking importante para sua carreira, mas se sente desconfortável e fora do lugar.',
        situation: 'Você está parado no canto da sala, observando as pessoas conversarem. Como você se aproxima da situação?',
        choices: [
          {
            id: 'avoid_hide',
            text: 'Fico no celular evitando contato visual',
            presenceLevel: 1,
            consequence: 'Você perde oportunidades valiosas e se sente ainda mais isolado.',
            feedback: 'Evitar pode parecer seguro, mas nos impede de crescer. Que tal um pequeno passo?'
          },
          {
            id: 'mindful_observation',
            text: 'Observo conscientemente o ambiente e respiro',
            presenceLevel: 3,
            consequence: 'Você se sente mais calmo e nota oportunidades naturais de conversa.',
            feedback: 'A observação consciente transforma ansiedade em curiosidade. Bem feito!'
          },
          {
            id: 'authentic_approach',
            text: 'Me aproximo de alguém com autenticidade',
            presenceLevel: 4,
            consequence: 'Você tem uma conversa genuína e faz uma conexão real.',
            feedback: 'Autenticidade é magnética. Você escolheu a coragem sobre o conforto.'
          }
        ],
        environment: 'Crowded networking event, soft lighting, people in small groups talking',
        learningFocus: 'Transformação de ansiedade social em presença autêntica'
      }
    ],
    raiva: [
      {
        id: 'traffic_frustration',
        title: 'Trânsito Engarrafado',
        context: 'Você está atrasado para um compromisso importante e preso em um engarrafamento. Um motorista acabou de "furar" sua frente.',
        situation: 'Você sente a raiva subindo. Suas mãos apertam o volante. O que você escolhe fazer?',
        choices: [
          {
            id: 'road_rage',
            text: 'Buzino, grito e faço gestos para o motorista',
            presenceLevel: 1,
            consequence: 'Você se sente ainda mais estressado e o conflito escala.',
            feedback: 'A raiva expressa impulsivamente raramente resolve algo. Ela apenas alimenta mais raiva.'
          },
          {
            id: 'breathing_acceptance',
            text: 'Respiro profundamente e aceito a situação',
            presenceLevel: 4,
            consequence: 'Você se sente mais calmo e consegue pensar em soluções.',
            feedback: 'Que transformação! Você escolheu a paz sobre a reatividade.'
          },
          {
            id: 'compassionate_understanding',
            text: 'Imagino que o motorista também pode estar passando por dificuldades',
            presenceLevel: 5,
            consequence: 'Sua raiva se transforma em compreensão e você se sente em paz.',
            feedback: 'Compaixão é o antídoto mais poderoso para a raiva. Você encontrou sabedoria.'
          }
        ],
        environment: 'Heavy traffic, car horns honking, tension in the air, red traffic lights',
        learningFocus: 'Transformação de raiva em compreensão e aceitação'
      }
    ],
    tristeza: [
      {
        id: 'relationship_ending',
        title: 'Fim de Relacionamento',
        context: 'Você acabou de terminar um relacionamento importante. Está em casa, sozinho, sentindo o peso da perda.',
        situation: 'As lágrimas vêm e você sente um vazio no peito. Como você escolhe estar com essa dor?',
        choices: [
          {
            id: 'numb_distract',
            text: 'Tento me distrair com TV, comida ou redes sociais',
            presenceLevel: 2,
            consequence: 'A distração oferece alívio temporário, mas a dor permanece não processada.',
            feedback: 'Distrações podem ajudar momentaneamente, mas a cura vem do acolhimento.'
          },
          {
            id: 'feel_fully',
            text: 'Permito-me sentir completamente a tristeza',
            presenceLevel: 4,
            consequence: 'Você sente a dor, mas também uma estranha sensação de alívio e autenticidade.',
            feedback: 'Que coragem! Sentir plenamente é o primeiro passo para a cura genuína.'
          },
          {
            id: 'gratitude_love',
            text: 'Honro o relacionamento com gratidão pelo que foi vivido',
            presenceLevel: 5,
            consequence: 'A tristeza permanece, mas é acompanhada por uma sensação de completude e amor.',
            feedback: 'Que sabedoria profunda! Você transformou perda em gratidão e amor.'
          }
        ],
        environment: 'Quiet apartment, soft lighting, tissues nearby, rain outside the window',
        learningFocus: 'Processamento consciente da tristeza e transformação em gratidão'
      }
    ],
    confusao: [
      {
        id: 'career_crossroads',
        title: 'Encruzilhada na Carreira',
        context: 'Você recebeu duas ofertas de emprego muito diferentes. Uma é segura mas entediante, outra é arriscada mas alinhada com seus sonhos.',
        situation: 'Você está na mesa da cozinha com os dois contratos à sua frente. Sua mente está em turbilhão. Como você aborda essa decisão?',
        choices: [
          {
            id: 'overthink_pros_cons',
            text: 'Faço listas intermináveis de prós e contras',
            presenceLevel: 2,
            consequence: 'Você se sente mais confuso e ansioso com tantas variáveis.',
            feedback: 'A mente analítica tem seu lugar, mas às vezes precisamos ouvir o coração.'
          },
          {
            id: 'body_wisdom',
            text: 'Imagino-me em cada situação e sinto as sensações no corpo',
            presenceLevel: 4,
            consequence: 'Você sente uma clareza sutil emergindo através das sensações corporais.',
            feedback: 'O corpo é um sábio conselheiro. Você acessou uma inteligência mais profunda.'
          },
          {
            id: 'values_alignment',
            text: 'Reflito sobre meus valores mais profundos e o que realmente importa',
            presenceLevel: 5,
            consequence: 'A decisão se torna clara quando alinhada com seus valores essenciais.',
            feedback: 'Quando nos conectamos com nossos valores, a confusão se dissolve em clareza.'
          }
        ],
        environment: 'Kitchen table with two contracts, morning coffee, sunlight streaming through window',
        learningFocus: 'Tomada de decisão consciente através de valores e sabedoria corporal'
      }
    ]
  };

  // Cenários universais que se aplicam a qualquer estado emocional
  const universalScenarios = [
    {
      id: 'unexpected_interruption',
      title: 'Interrupção Inesperada',
      context: 'Você está profundamente concentrado em uma tarefa importante quando alguém interrompe com uma "urgência".',
      situation: 'Você sente sua concentração se quebrar. Como você responde a essa interrupção?',
      choices: [
        {
          id: 'reactive_irritation',
          text: 'Demonstro irritação e respondo de forma brusca',
          presenceLevel: 1,
          consequence: 'A pessoa se sente mal e você perde ainda mais tempo com o conflito.',
          feedback: 'Reatividade cria mais problemas. Que tal uma pausa consciente?'
        },
        {
          id: 'mindful_pause',
          text: 'Faço uma pausa, respiro e pergunto sobre a urgência',
          presenceLevel: 4,
          consequence: 'Você descobre que não era tão urgente e negocia um melhor momento.',
          feedback: 'A pausa consciente cria espaço para sabedoria. Excelente escolha!'
        },
        {
          id: 'compassionate_presence',
          text: 'Ofereço presença total, mesmo que por alguns minutos',
          presenceLevel: 5,
          consequence: 'A pessoa se sente ouvida e você retorna ao trabalho com o coração leve.',
          feedback: 'Presença genuína é o presente mais valioso que podemos oferecer.'
        }
      ],
      environment: 'Focused workspace suddenly disrupted, person standing at door, scattered attention',
      learningFocus: 'Gestão consciente de interrupções e presença relacional'
    }
  ];

  useEffect(() => {
    if (isActive && !currentScenario) {
      selectScenario();
    }
  }, [isActive]);

  const selectScenario = () => {
    let availableScenarios = [...universalScenarios];
    
    // Adicionar cenários específicos baseados no estado emocional
    if (userEmotionalState && scenarioLibrary[userEmotionalState]) {
      availableScenarios = [...availableScenarios, ...scenarioLibrary[userEmotionalState]];
    }
    
    // Filtrar cenários já vivenciados recentemente
    const recentScenarioIds = scenarioHistory.slice(-3).map(s => s.id);
    availableScenarios = availableScenarios.filter(s => !recentScenarioIds.includes(s.id));
    
    // Selecionar cenário aleatório
    const selectedScenario = availableScenarios[Math.floor(Math.random() * availableScenarios.length)];
    
    setCurrentScenario(selectedScenario);
    setScenarioPhase('presenting');
    setUserChoice(null);
    setUserReflection('');
    setShowFeedback(false);
  };

  const handleChoiceSelection = (choice) => {
    setUserChoice(choice);
    setScenarioPhase('reflecting');
    setShowFeedback(true);
  };

  const handleScenarioCompletion = () => {
    const scenarioResult = {
      scenario: currentScenario,
      choice: userChoice,
      reflection: userReflection,
      presenceLevel: userChoice.presenceLevel,
      timestamp: new Date().toISOString(),
      emotionalState: userEmotionalState
    };

    // Adicionar ao histórico
    setScenarioHistory(prev => [...prev, scenarioResult]);

    // Callback para componente pai
    if (onScenarioComplete) {
      onScenarioComplete(scenarioResult);
    }

    setScenarioPhase('completed');
  };

  const startNewScenario = () => {
    setCurrentScenario(null);
    selectScenario();
  };

  const getPresenceLevelColor = (level) => {
    const colors = {
      1: '#ff6b6b', // Vermelho - Reativo
      2: '#ffa726', // Laranja - Consciente mas limitado
      3: '#ffeb3b', // Amarelo - Crescendo em consciência
      4: '#66bb6a', // Verde - Presença consciente
      5: '#42a5f5'  // Azul - Sabedoria profunda
    };
    return colors[level] || '#9e9e9e';
  };

  const getPresenceLevelName = (level) => {
    const names = {
      1: 'Reativo',
      2: 'Consciente',
      3: 'Crescendo',
      4: 'Presente',
      5: 'Sábio'
    };
    return names[level] || 'Indefinido';
  };

  if (!isActive || !currentScenario) {
    return null;
  }

  return (
    <div className="scenario-simulator">
      <div className="scenario-container">
        
        {scenarioPhase === 'presenting' && (
          <div className="scenario-presentation">
            <div className="scenario-header">
              <h2>{currentScenario.title}</h2>
              <div className="scenario-focus">
                <span>Foco: {currentScenario.learningFocus}</span>
              </div>
            </div>
            
            <div className="scenario-content">
              <div className="scenario-context">
                <h3>Contexto</h3>
                <p>{currentScenario.context}</p>
              </div>
              
              <div className="scenario-situation">
                <h3>Situação</h3>
                <p>{currentScenario.situation}</p>
              </div>
              
              <div className="scenario-environment">
                <em>Ambiente: {currentScenario.environment}</em>
              </div>
            </div>
            
            <div className="scenario-choices">
              <h3>Como você responde?</h3>
              <div className="choices-grid">
                {currentScenario.choices.map((choice) => (
                  <button
                    key={choice.id}
                    className="choice-button"
                    onClick={() => handleChoiceSelection(choice)}
                    style={{ borderLeft: `4px solid ${getPresenceLevelColor(choice.presenceLevel)}` }}
                  >
                    <div className="choice-text">{choice.text}</div>
                    <div className="choice-level">
                      Nível: {getPresenceLevelName(choice.presenceLevel)}
                    </div>
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        {scenarioPhase === 'reflecting' && showFeedback && (
          <div className="scenario-feedback">
            <div className="feedback-header">
              <h2>Resultado da sua escolha</h2>
              <div 
                className="presence-level-badge"
                style={{ backgroundColor: getPresenceLevelColor(userChoice.presenceLevel) }}
              >
                Nível {userChoice.presenceLevel}: {getPresenceLevelName(userChoice.presenceLevel)}
              </div>
            </div>
            
            <div className="feedback-content">
              <div className="choice-recap">
                <h3>Você escolheu:</h3>
                <p>"{userChoice.text}"</p>
              </div>
              
              <div className="consequence">
                <h3>Consequência:</h3>
                <p>{userChoice.consequence}</p>
              </div>
              
              <div className="feedback-message">
                <h3>Reflexão:</h3>
                <p>{userChoice.feedback}</p>
              </div>
            </div>
            
            <div className="reflection-prompt">
              <h3>Como você se sente sobre essa experiência?</h3>
              <textarea
                value={userReflection}
                onChange={(e) => setUserReflection(e.target.value)}
                placeholder="Compartilhe seus insights, sentimentos ou aprendizados..."
                className="reflection-textarea"
                rows={4}
              />
            </div>
            
            <div className="scenario-actions">
              <button 
                onClick={handleScenarioCompletion}
                className="complete-scenario-button"
              >
                Finalizar Cenário
              </button>
            </div>
          </div>
        )}

        {scenarioPhase === 'completed' && (
          <div className="scenario-completion">
            <div className="completion-header">
              <h2>Cenário Concluído!</h2>
              <div className="completion-stats">
                <div className="stat">
                  <span className="stat-label">Nível de Presença:</span>
                  <span 
                    className="stat-value"
                    style={{ color: getPresenceLevelColor(userChoice.presenceLevel) }}
                  >
                    {userChoice.presenceLevel}/5
                  </span>
                </div>
                <div className="stat">
                  <span className="stat-label">Cenários Completados:</span>
                  <span className="stat-value">{scenarioHistory.length}</span>
                </div>
              </div>
            </div>
            
            <div className="completion-message">
              <p>
                Cada cenário é uma oportunidade de praticar presença consciente. 
                Você está desenvolvendo a habilidade de responder ao invés de reagir.
              </p>
            </div>
            
            <div className="completion-actions">
              <button 
                onClick={startNewScenario}
                className="new-scenario-button"
              >
                Novo Cenário
              </button>
              <button 
                onClick={() => onScenarioComplete && onScenarioComplete(null)}
                className="exit-simulator-button"
              >
                Sair do Simulador
              </button>
            </div>
          </div>
        )}
        
      </div>
    </div>
  );
};

export default ScenarioSimulator;

