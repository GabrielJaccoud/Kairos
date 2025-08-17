import React, { useState, useEffect } from 'react';
import './App.css';
import MatrixQuadrant from './components/MatrixQuadrant';
import RitualCard from './components/RitualCard';
import ReflectionForm from './components/ReflectionForm';

function App() {
  const [currentView, setCurrentView] = useState('matrix');
  const [tasks, setTasks] = useState({});
  const [rituals, setRituals] = useState([]);
  const [showReflectionForm, setShowReflectionForm] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

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
  }, []);

  const handleTaskClick = (task) => {
    console.log('Task clicked:', task);
    // Implementar modal de edição de tarefa
  };

  const handleAddTask = (quadrant) => {
    console.log('Add task to quadrant:', quadrant);
    // Implementar modal de criação de tarefa
  };

  const handleExecuteRitual = async (ritual) => {
    console.log('Executing ritual:', ritual);
    // Implementar execução de ritual
    return new Promise(resolve => {
      setTimeout(() => {
        alert(`Ritual "${ritual.name}" executado com sucesso!`);
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
    // Implementar salvamento de reflexão
    return new Promise(resolve => {
      setTimeout(() => {
        alert('Reflexão salva com sucesso!');
        setShowReflectionForm(false);
        resolve();
      }, 1500);
    });
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
          </nav>
        </div>
      </header>

      <main className="app-main">
        {currentView === 'matrix' && renderMatrixView()}
        {currentView === 'rituals' && renderRitualsView()}
        {currentView === 'reflection' && renderReflectionView()}
      </main>

      <footer className="app-footer">
        <p>Desenvolvido com presença e propósito • Kairos v1.0</p>
      </footer>
    </div>
  );
}

export default App;


