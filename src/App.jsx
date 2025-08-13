import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>Kairos App</h1>
          <p>Companion of Presence</p>
        </header>
        <main>
          <Routes>
            <Route path="/" element={
              <div>
                <h2>Bem-vindo ao Kairos</h2>
                <p>Seu companheiro de jornada consciente</p>
              </div>
            } />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
