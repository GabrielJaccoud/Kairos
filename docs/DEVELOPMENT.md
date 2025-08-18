# Guia de Desenvolvimento - Kairos

## Configuração do Ambiente de Desenvolvimento

### Pré-requisitos

- **Node.js** 18.0.0 ou superior
- **Python** 3.11.0 ou superior
- **Git** 2.30.0 ou superior
- **npm** 8.0.0 ou superior
- **pip** 21.0.0 ou superior

### Clonando o Repositório

```bash
git clone https://github.com/GabrielJaccoud/Kairos.git
cd Kairos
```

## Configuração do Frontend

### Instalação das Dependências

```bash
npm install
```

### Scripts Disponíveis

```bash
# Executar em modo de desenvolvimento
npm start

# Executar testes
npm test

# Build para produção
npm run build

# Ejetar configuração (não recomendado)
npm run eject
```

### Estrutura de Componentes

```
src/
├── components/
│   ├── MatrixQuadrant.jsx      # Quadrante da matriz
│   ├── MatrixQuadrant.css      # Estilos do quadrante
│   ├── RitualCard.jsx          # Card de ritual
│   ├── RitualCard.css          # Estilos do ritual
│   ├── ReflectionForm.jsx      # Formulário de reflexão
│   └── ReflectionForm.css      # Estilos da reflexão
├── App.jsx                     # Componente principal
├── App.css                     # Estilos principais
├── index.js                    # Ponto de entrada
└── index.css                   # Estilos globais
```

### Padrões de Código Frontend

#### Componentes React
- Use componentes funcionais com hooks
- Implemente PropTypes para validação
- Mantenha componentes pequenos e focados
- Use CSS Modules ou styled-components para estilos

```jsx
import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import './ComponentName.css';

const ComponentName = ({ prop1, prop2, onAction }) => {
  const [state, setState] = useState(initialValue);

  useEffect(() => {
    // Efeitos colaterais
  }, [dependencies]);

  const handleAction = () => {
    // Lógica do handler
    onAction(data);
  };

  return (
    <div className="component-name">
      {/* JSX */}
    </div>
  );
};

ComponentName.propTypes = {
  prop1: PropTypes.string.isRequired,
  prop2: PropTypes.number,
  onAction: PropTypes.func.isRequired
};

ComponentName.defaultProps = {
  prop2: 0
};

export default ComponentName;
```

#### Estilos CSS
- Use BEM methodology para nomenclatura
- Implemente variáveis CSS para consistência
- Mantenha responsividade mobile-first
- Use animações suaves para transições

```css
.component-name {
  /* Estilos base */
}

.component-name__element {
  /* Elemento do componente */
}

.component-name__element--modifier {
  /* Modificador do elemento */
}

.component-name:hover {
  /* Estados interativos */
}

@media (max-width: 768px) {
  /* Responsividade */
}
```

## Configuração do Backend

### Configuração do Ambiente Virtual

```bash
cd backend/kairos-backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### Instalação das Dependências

```bash
pip install -r requirements.txt
```

### Estrutura do Backend

```
backend/kairos-backend/
├── src/
│   ├── models/
│   │   ├── task.py         # Modelo de tarefa
│   │   ├── ritual.py       # Modelo de ritual
│   │   └── reflection.py   # Modelo de reflexão
│   ├── routes/
│   │   ├── tasks.py        # Rotas de tarefas
│   │   ├── rituals.py      # Rotas de rituais
│   │   └── reflections.py  # Rotas de reflexões
│   ├── static/             # Arquivos estáticos
│   └── main.py             # Aplicação principal
├── venv/                   # Ambiente virtual
└── requirements.txt        # Dependências
```

### Padrões de Código Backend

#### Modelos SQLAlchemy
```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ModelName(db.Model):
    __tablename__ = 'model_names'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<ModelName {self.name}>'
```

#### Rotas Flask
```python
from flask import Blueprint, request, jsonify
from models.model_name import ModelName, db

bp = Blueprint('model_name', __name__)

@bp.route('/api/models', methods=['GET'])
def get_models():
    try:
        models = ModelName.query.all()
        return jsonify({
            'success': True,
            'models': [model.to_dict() for model in models]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/api/models', methods=['POST'])
def create_model():
    try:
        data = request.get_json()
        
        # Validação
        if not data.get('name'):
            return jsonify({
                'success': False,
                'error': 'Nome é obrigatório'
            }), 400
        
        # Criação
        model = ModelName(name=data['name'])
        db.session.add(model)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'model': model.to_dict(),
            'message': 'Modelo criado com sucesso'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
```

## Configuração do AI Engine

### Configuração do Ambiente

```bash
cd ai-engine
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Estrutura do AI Engine

```
ai-engine/
├── advanced_presence_analyzer.py  # Análise avançada de presença
├── intelligent_task_optimizer.py  # Otimização inteligente de tarefas
├── adaptive_ritual_engine.py      # Motor de rituais adaptativos
├── venv/                          # Ambiente virtual
└── requirements.txt               # Dependências
```

### Padrões de Código AI

#### Algoritmos de Machine Learning
```python
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from datetime import datetime, timedelta

class PresenceAnalyzer(BaseEstimator, TransformerMixin):
    def __init__(self, window_size=7):
        self.window_size = window_size
        self.model = None
        
    def fit(self, X, y=None):
        """Treina o modelo com dados históricos"""
        # Implementação do treinamento
        return self
        
    def transform(self, X):
        """Transforma dados de entrada"""
        # Implementação da transformação
        return X
        
    def predict(self, X):
        """Faz predições"""
        # Implementação da predição
        return predictions
        
    def analyze_patterns(self, user_data):
        """Analisa padrões de presença"""
        patterns = {
            'peak_hours': self._find_peak_hours(user_data),
            'energy_cycles': self._analyze_energy_cycles(user_data),
            'stress_indicators': self._detect_stress_patterns(user_data)
        }
        return patterns
```

## Fluxo de Desenvolvimento

### 1. Configuração Inicial
```bash
# Clone e configure o projeto
git clone https://github.com/GabrielJaccoud/Kairos.git
cd Kairos

# Configure frontend
npm install

# Configure backend
cd backend/kairos-backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure AI engine
cd ../../ai-engine
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Desenvolvimento Local
```bash
# Terminal 1: Frontend
npm start

# Terminal 2: Backend
cd backend/kairos-backend
source venv/bin/activate
python src/main.py

# Terminal 3: AI Engine (se necessário)
cd ai-engine
source venv/bin/activate
python task-optimizer.py
```

### 3. Testes

#### Frontend
```bash
npm test
npm run test:coverage
```

#### Backend
```bash
cd backend/kairos-backend
source venv/bin/activate
python -m pytest tests/
python -m pytest tests/ --cov=src
```

#### AI Engine
```bash
cd ai-engine
source venv/bin/activate
python -m pytest tests/
```

### 4. Build e Deploy
```bash
# Build frontend
npm run build

# Deploy
# (Instruções específicas no DEPLOYMENT.md)
```

## Padrões de Commit

Use Conventional Commits:

```
feat: adiciona nova funcionalidade
fix: corrige bug
docs: atualiza documentação
style: mudanças de formatação
refactor: refatoração de código
test: adiciona ou atualiza testes
chore: tarefas de manutenção
```

Exemplos:
```bash
git commit -m "feat: adiciona componente MatrixQuadrant"
git commit -m "fix: corrige bug na validação de tarefas"
git commit -m "docs: atualiza documentação da API"
```

## Debugging

### Frontend
- Use React Developer Tools
- Console.log para debugging simples
- Breakpoints no navegador
- Error Boundaries para captura de erros

### Backend
- Use Flask Debug Mode
- Logging com diferentes níveis
- Debugger Python (pdb)
- Postman/Insomnia para testar APIs

### AI Engine
- Jupyter Notebooks para experimentação
- Matplotlib/Seaborn para visualização
- Unit tests para algoritmos
- Logging detalhado para análise

## Performance

### Frontend
- Lazy loading de componentes
- Memoização com React.memo
- Otimização de re-renders
- Code splitting

### Backend
- Indexação de banco de dados
- Cache de queries frequentes
- Paginação de resultados
- Conexão pool

### AI Engine
- Vectorização com NumPy
- Cache de modelos treinados
- Processamento assíncrono
- Otimização de algoritmos

## Segurança

### Geral
- Nunca commitar credenciais
- Use variáveis de ambiente
- Validação de entrada
- Sanitização de dados

### Backend
- CORS configurado corretamente
- Rate limiting
- Validação de JWT (quando implementado)
- SQL injection prevention

## Monitoramento

### Logs
- Estruturados em JSON
- Diferentes níveis (DEBUG, INFO, WARN, ERROR)
- Rotação automática
- Centralização (quando em produção)

### Métricas
- Performance de endpoints
- Uso de recursos
- Erros e exceções
- Métricas de negócio

## Contribuição

1. Fork o repositório
2. Crie uma branch feature
3. Desenvolva seguindo os padrões
4. Escreva testes
5. Atualize documentação
6. Submit Pull Request

## Recursos Úteis

### Documentação
- [React Docs](https://reactjs.org/docs)
- [Flask Docs](https://flask.palletsprojects.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Scikit-learn Docs](https://scikit-learn.org/stable/)

### Ferramentas
- [VS Code](https://code.visualstudio.com/)
- [Postman](https://www.postman.com/)
- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/)

---

*Guia atualizado em: Janeiro 2024*

