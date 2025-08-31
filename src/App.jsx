import React, { useState, useEffect } from 'react';
import './App.css';
import MatrixQuadrant from './components/MatrixQuadrant';
import RitualCard from './components/RitualCard';
import ReflectionForm from './components/ReflectionForm';
import ImmersiveEnvironment from './components/ImmersiveEnvironment';
import ScenarioSimulator from './components/ScenarioSimulator';
import PresencePoints from './components/gamification/PresencePoints';
import EmotionalAnalyzer from './services/EmotionalAnalyzer';

function App() {
  const [currentView, setCurrentView] = useState('matrix');
  const [tasks, setTasks] = useState({});
  const [rituals, setRituals] = useState([]);
  const [showReflectionForm, setShowReflectionForm] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  
  // Estados para as novas funcionalidades
  const [showImmersiveEnvironment, setShowImmersiveEnvironment] = useState(false);
  const [showScenarioSimulator, setShowScenarioSimulator] = useState(false);
  const [currentEnvironment, setCurrentEnvironment] = useState(null);
  const [userEmotionalState, setUserEmotionalState] = useState(null);
  const [presencePoints, setPresencePoints] = useState(0);
  const [recentActivities, setRecentActivities] = useState([]);
  const [emotionalAnalyzer] = useState(new EmotionalAnalyzer());

  // Dados de exemplo para demonstração
  useEffect(() => {
    // Simular carregamento de dados
    setTasks({
      urgent_important: [
        {
          id: 1,
          title: 'Reunião com Cliente Importante',
          scheduled_for: '2024-01-15T14:00:00Z',
          contacts: '["Maria Silva", "João Santos"]',
          ai_priority_score: 0.95
        },
        {
          id: 2,
          title: 'Entrega do Projeto Final',
          scheduled_for: '2024-01-15T17:00:00Z',
          contacts: '["Equipe Dev"]',
          ai_priority_score: 0.90
        }
      ],
      important_not_urgent: [
        {
          id: 3,
          title: 'Planejamento Estratégico 2024',
          scheduled_for: '2024-01-16T10:00:00Z',
          contacts: '["CEO", "CTO"]',
          ai_priority_score: 0.75
        },
        {
          id: 4,
          title: 'Estudar Nova Tecnologia',
          ai_priority_score: 0.65
        }
      ],
      urgent_not_important: [
        {
          id: 5,
          title: 'Responder E-mails Pendentes',
          ai_priority_score: 0.45
        }
      ],
      not_urgent_not_important: [
        {
          id: 6,
          title: 'Organizar Desktop',
          ai_priority_score: 0.25
        }
      ],
      presence: [
        {
          id: 7,
          title: 'Pausa Consciente',
          scheduled_for: '2024-01-15T15:30:00Z',
          ai_priority_score: 0.80
        }
      ]
    });

    setRituals([
      {
        id: 1,
        name: 'Respiração Matinal',
        description: 'Comece o dia com clareza e presença',
        ritual_type: 'morning',
        duration_minutes: 5,
        scheduled_time: '07:00',
        is_active: true,
        instructions: '1. Sente-se confortavelmente\n2. Feche os olhos\n3. Respire profundamente 10 vezes\n4. Defina uma intenção para o dia'
      },
      {
        id: 2,
        name: 'Meditação Noturna',
        description: 'Encerre o dia em paz e gratidão',
        ritual_type: 'evening',
        duration_minutes: 10,
        scheduled_time: '22:00',
        is_active: true,
        instructions: '1. Deite-se confortavelmente\n2. Relaxe cada parte do corpo\n3. Reflita sobre 3 coisas boas do dia\n4. Respire suavemente até adormecer'
      }
    ]);

    // Carregar dados de presença do localStorage
    const savedPoints = localStorage.getItem('kairos_presence_points');
    const savedActivities = localStorage.getItem('kairos_recent_activities');
    
    if (savedPoints) {
      setPresencePoints(parseInt(savedPoints));
    } else {
      setPresencePoints(150); // Pontos iniciais para demonstração
    }
    
    if (savedActivities) {
      setRecentActivities(JSON.parse(savedActivities));
    } else {
      // Atividades de exemplo
      setRecentActivities([
        { type: 'daily_reflection_deep', timestamp: new Date().toISOString() },
        { type: 'morning_ritual_completed', timestamp: new Date(Date.now() - 86400000).toISOString() },
        { type: 'presence_axis_choice', timestamp: new Date(Date.now() - 172800000).toISOString() }
      ]);
    }
  }, []);

  // Função para adicionar pontos de presença
  const addPresencePoints = (activity) => {
    const newActivity = {
      ...activity,
      timestamp: new Date().toISOString()
    };
    
    const updatedActivities = [newActivity, ...recentActivities].slice(0, 20);
    setRecentActivities(updatedActivities);
    
    // Calcular pontos baseado no tipo de atividade
    const pointsToAdd = getActivityPoints(activity.type);
    const newPoints = presencePoints + pointsToAdd;
    setPresencePoints(newPoints);
    
    // Salvar no localStorage
    localStorage.setItem('kairos_presence_points', newPoints.toString());
    localStorage.setItem('kairos_recent_activities', JSON.stringify(updatedActivities));
  };

  const getActivityPoints = (activityType) => {
    const pointsMap = {
      daily_reflection_basic: 10,
      daily_reflection_deep: 25,
      daily_reflection_transformative: 50,
      morning_ritual_completed: 15,
      evening_ritual_completed: 15,
      custom_ritual_completed: 20,
      task_completed_mindfully: 5,
      urgent_important_handled: 15,
      presence_axis_choice: 25,
      immersive_experience_completed: 30,
      scenario_completed: 20,
      emotional_processing_session: 35
    };
    return pointsMap[activityType] || 5;
  };

  // Função para analisar texto e detectar emoções
  const analyzeUserInput = (text) => {
    const analysis = emotionalAnalyzer.analyzeText(text);
    if (analysis.dominantEmotion) {
      setUserEmotionalState(analysis.dominantEmotion);
      
      // Gerar ambiente imersivo baseado na emoção
      const environment = emotionalAnalyzer.generateVisualEnvironment(
        analysis.dominantEmotion, 
        analysis.intensity
      );
      
      // Adicionar mantra personalizado
      environment.mantra = emotionalAnalyzer.generatePersonalizedMantra(
        analysis.dominantEmotion, 
        analysis.intensity
      );
      
      setCurrentEnvironment(environment);
    }
    return analysis;
  };

  const handleTaskClick = (task) => {
    console.log('Task clicked:', task);
    // Implementar modal de edição de tarefa
    
    // Adicionar pontos por interação consciente
    addPresencePoints({ type: 'task_completed_mindfully' });
  };

  const handleAddTask = (quadrant) => {
    console.log('Add task to quadrant:', quadrant);
    // Implementar modal de criação de tarefa
    
    if (quadrant === 'presence') {
      addPresencePoints({ type: 'presence_axis_choice' });
    }
  };

  const handleExecuteRitual = async (ritual) => {
    console.log('Executing ritual:', ritual);
    
    return new Promise(resolve => {
      setTimeout(() => {
        alert(`Ritual "${ritual.name}" executado com sucesso!`);
        
        // Adicionar pontos baseado no tipo de ritual
        const activityType = ritual.ritual_type === 'morning' ? 
          'morning_ritual_completed' : 
          ritual.ritual_type === 'evening' ? 
            'evening_ritual_completed' : 
            'custom_ritual_completed';
        
        addPresencePoints({ type: activityType });
        resolve();
      }, 2000);
    });
  };

  const handleEditRitual = (ritual) => {
    console.log('Edit ritual:', ritual);
    // Implementar edição de ritual
  };

  const handleToggleRitualActive = (ritualId, isActive) => {
    setRituals(prev => prev.map(ritual => 
      ritual.id === ritualId ? { ...ritual, is_active: isActive } : ritual
    ));
  };

  const handleSaveReflection = async (reflectionData) => {
    console.log('Saving reflection:', reflectionData);
    
    // Analisar o texto da reflexão para detectar emoções
    const combinedText = `${reflectionData.gratitude} ${reflectionData.forgiveness} ${reflectionData.learning} ${reflectionData.overcoming}`;
    const emotionalAnalysis = analyzeUserInput(combinedText);
    
    return new Promise(resolve => {
      setTimeout(() => {
        alert('Reflexão salva com sucesso!');
        setShowReflectionForm(false);
        
        // Determinar profundidade da reflexão baseada no conteúdo
        const totalLength = combinedText.length;
        let activityType = 'daily_reflection_basic';
        
        if (totalLength > 500) {
          activityType = 'daily_reflection_transformative';
        } else if (totalLength > 200) {
          activityType = 'daily_reflection_deep';
        }
        
        addPresencePoints({ type: activityType });
        
        // Se detectou emoção forte, sugerir experiência imersiva
        if (emotionalAnalysis.dominantEmotion && emotionalAnalysis.intensity !== 'baixa') {
          setTimeout(() => {
            if (window.confirm(`Detectei que você está sentindo ${emotionalAnalysis.dominantEmotion}. Gostaria de fazer uma experiência imersiva para processar essa emoção?`)) {
              setShowImmersiveEnvironment(true);
            }
          }, 1000);
        }
        
        resolve();
      }, 1500);
    });
  };

  const handleImmersiveExperienceComplete = (experienceData) => {
    console.log('Immersive experience completed:', experienceData);
    setShowImmersiveEnvironment(false);
    
    if (experienceData) {
      addPresencePoints({ type: 'immersive_experience_completed' });
      
      // Sugerir simulador de cenários se apropriado
      setTimeout(() => {
        if (window.confirm('Que tal praticar sua presença em situações cotidianas? Gostaria de tentar o simulador de cenários?')) {
          setShowScenarioSimulator(true);
        }
      }, 2000);
    }
  };

  const handleScenarioComplete = (scenarioResult) => {
    console.log('Scenario completed:', scenarioResult);
    
    if (scenarioResult) {
      addPresencePoints({ type: 'scenario_completed' });
      
      // Bonus points for high presence level choices
      if (scenarioResult.presenceLevel >= 4) {
        addPresencePoints({ type: 'emotional_processing_session' });
      }
    } else {
      // User exited simulator
      setShowScenarioSimulator(false);
    }
  };

  const renderMatrixView = () => (
    <div className="matrix-container">
      <div className="matrix-header">
        <h1>Matriz Adaptada de Presença</h1>
        <p>Organize suas tarefas com consciência e propósito</p>
      </div>
      
      <div className="matrix-grid">
        <MatrixQuadrant
          quadrant="urgent_important"
          tasks={tasks.urgent_important || []}
          onTaskClick={handleTaskClick}
          onAddTask={handleAddTask}
        />
        <MatrixQuadrant
          quadrant="important_not_urgent"
          tasks={tasks.important_not_urgent || []}
          onTaskClick={handleTaskClick}
          onAddTask={handleAddTask}
        />
        <MatrixQuadrant
          quadrant="urgent_not_important"
          tasks={tasks.urgent_not_important || []}
          onTaskClick={handleTaskClick}
          onAddTask={handleAddTask}
        />
        <MatrixQuadrant
          quadrant="not_urgent_not_important"
          tasks={tasks.not_urgent_not_important || []}
          onTaskClick={handleTaskClick}
          onAddTask={handleAddTask}
        />
      </div>
      
      <div className="presence-axis">
        <MatrixQuadrant
          quadrant="presence"
          tasks={tasks.presence || []}
          onTaskClick={handleTaskClick}
          onAddTask={handleAddTask}
          className="presence-quadrant"
        />
      </div>
    </div>
  );

  const renderRitualsView = () => (
    <div className="rituals-container">
      <div className="rituals-header">
        <h1>Rituais de Presença</h1>
        <p>Cultive momentos sagrados no seu dia</p>
      </div>
      
      <div className="rituals-grid">
        {rituals.map(ritual => (
          <RitualCard
            key={ritual.id}
            ritual={ritual}
            onExecute={handleExecuteRitual}
            onEdit={handleEditRitual}
            onToggleActive={handleToggleRitualActive}
            stats={{
              total_executions: Math.floor(Math.random() * 50) + 10,
              average_rating: (Math.random() * 2 + 3).toFixed(1),
              consistency_score: Math.floor(Math.random() * 40) + 60
            }}
          />
        ))}
      </div>
      {/* Botões para experiência imersiva e simulador de cenários */}
      <div className="ritual-actions">
        <button 
          className="immersive-experience-btn"
          onClick={() => setShowImmersiveEnvironment(true)}
        >
          🌟 Experiência Imersiva
        </button>
        <button 
          className="scenario-simulator-btn"
          onClick={() => setShowScenarioSimulator(true)}
        >
          🎭 Simulador de Cenários
        </button>
      </div>
    </div>
  );

  const renderReflectionView = () => (
    <div className="reflection-container">
      <div className="reflection-header">
        <h1>Reflexão Diária</h1>
        <p>Um momento para honrar sua jornada</p>
      </div>
      
      {!showReflectionForm ? (
        <div className="reflection-prompt">
          <div className="prompt-card">
            <h2>Como foi seu dia hoje?</h2>
            <p>Reserve alguns minutos para refletir sobre sua jornada diária através dos 4 pilares da presença consciente.</p>
            <button 
              className="start-reflection-btn"
              onClick={() => setShowReflectionForm(true)}
            >
              Iniciar Reflexão
            </button>
          </div>
        </div>
      ) : (
        <ReflectionForm
          onSave={handleSaveReflection}
          onCancel={() => setShowReflectionForm(false)}
          isLoading={isLoading}
        />
      )}
    </div>
  );

  const renderPresenceView = () => (
    <div className="presence-container">
      <div className="presence-header">
        <h1>Jornada de Presença</h1>
        <p>Acompanhe seu crescimento consciente</p>
      </div>
      
      <PresencePoints
        currentPoints={presencePoints}
        recentActivities={recentActivities}
        onPointsUpdate={setPresencePoints}
        showDetails={true}
      />
    </div>
  );

  return (
    <div className="App">
      <header className="app-header">
        <div className="header-content">
          <div className="logo-section">
            <img src="/logo.png" alt="Kairos Logo" className="logo-image" />
            <div className="logo-text-container">
              <span className="logo-text">Kairos</span>
              <span className="tagline">Companion of Presence</span>
            </div>
          </div>
          
          <nav className="main-nav">
            <button 
              className={`nav-btn ${currentView === 'matrix' ? 'active' : ''}`}
              onClick={() => setCurrentView('matrix')}
            >
              <span className="nav-icon">📊</span>
              Matriz
            </button>
            <button 
              className={`nav-btn ${currentView === 'rituals' ? 'active' : ''}`}
              onClick={() => setCurrentView('rituals')}
            >
              <span className="nav-icon">🧘‍♀️</span>
              Rituais
            </button>
            <button 
              className={`nav-btn ${currentView === 'reflection' ? 'active' : ''}`}
              onClick={() => setCurrentView('reflection')}
            >
              <span className="nav-icon">📝</span>
              Reflexão
            </button>
            <button 
              className={`nav-btn ${currentView === 'presence' ? 'active' : ''}`}
              onClick={() => setCurrentView('presence')}
            >
              <span className="nav-icon">✨</span>
              Presença
            </button>
          </nav>
        </div>
      </header>

      <main className="app-main">
        {currentView === 'matrix' && renderMatrixView()}
        {currentView === 'rituals' && renderRitualsView()}
        {currentView === 'reflection' && renderReflectionView()}
        {currentView === 'presence' && renderPresenceView()}

        {showImmersiveEnvironment && (
          <ImmersiveEnvironment
            environment={currentEnvironment}
            onComplete={handleImmersiveExperienceComplete}
            onExit={() => setShowImmersiveEnvironment(false)}
          />
        )}

        {showScenarioSimulator && (
          <ScenarioSimulator
            onComplete={handleScenarioComplete}
            onExit={() => setShowScenarioSimulator(false)}
          />
        )}
      </main>

      <footer className="app-footer">
        <p>&copy; 2025 Kairos. Desenvolvido com presença e propósito.</p>
      </footer>
    </div>
  );
}

export default App;


