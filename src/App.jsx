import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>🕰️ Kairos</h1>
          <p>Companion of Presence</p>
        </header>
        <main>
          <Routes>
            <Route path="/" element={<HomePage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

function HomePage() {
  return (
    <>
      <section className="welcome-section">
        <h2>Bem-vindo ao Kairos</h2>
        <p>
          Muito mais que um simples planner - é um companheiro de jornada inteligente 
          que une organização produtiva com presença mindfulness. Enquanto a maioria 
          dos aplicativos foca apenas em "fazer mais", o Kairos se preocupa em fazer 
          melhor e viver mais plenamente cada momento.
        </p>
      </section>

      <section className="features-grid">
        <div className="feature-card">
          <h3><span className="icon">🎯</span> Matriz Adaptada de Presença</h3>
          <p>
            Sistema 5D: Importante/Urgente + Eixo da Presença. Quadrantes que 
            consideram não só o que fazer, mas como estar ao fazê-lo.
          </p>
        </div>

        <div className="feature-card">
          <h3><span className="icon">🤖</span> IA como Mentor de Vida</h3>
          <p>
            Reorganiza automaticamente quando imprevistos surgem, sugere pausas 
            antes que o estresse apareça e aprende seu ritmo pessoal.
          </p>
        </div>

        <div className="feature-card">
          <h3><span className="icon">🧘‍♀️</span> Integração Humana Profunda</h3>
          <p>
            Conecta contatos diretamente aos eventos, facilita interações e 
            transforma tarefas em experiências compartilhadas.
          </p>
        </div>

        <div className="feature-card">
          <h3><span className="icon">🌅</span> Rituais Personalizados</h3>
          <p>
            Respiração matinal, meditações guiadas, pausas conscientes e 
            sistema de criação para seus próprios rituais de bem-estar.
          </p>
        </div>
      </section>

      <section className="matrix-preview">
        <h3>Matriz Adaptada de Presença</h3>
        <div className="matrix-grid">
          <div className="matrix-quadrant quadrant-1">
            <strong>Urgente + Importante</strong><br/>
            Crises e emergências
          </div>
          <div className="matrix-quadrant quadrant-2">
            <strong>Importante + Não Urgente</strong><br/>
            Planejamento e prevenção
          </div>
          <div className="matrix-quadrant quadrant-3">
            <strong>Urgente + Não Importante</strong><br/>
            Interrupções e distrações
          </div>
          <div className="matrix-quadrant quadrant-4">
            <strong>Não Urgente + Não Importante</strong><br/>
            Atividades triviais
          </div>
        </div>
        <div className="presence-axis">
          <strong>🌟 Eixo da Presença</strong><br/>
          Improvisos conscientes - porque a vida acontece
        </div>
      </section>

      <section className="cta-section">
        <h3>Organize seu tempo. Eduque sua presença. Viva seus momentos.</h3>
        <p>Transforme a maneira como você se relaciona com o tempo</p>
        <button className="cta-button">Começar Jornada</button>
      </section>
    </>
  );
}

export default App;
