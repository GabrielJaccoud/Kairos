# Kairos - Companion of Presence

## Visão Geral

Kairos é mais que um simples planner - é um companheiro de jornada inteligente que une organização produtiva com presença mindfulness. Enquanto a maioria dos aplicativos foca apenas em "fazer mais", o Kairos se preocupa em fazer melhor e viver mais plenamente cada momento.

## Filosofia

**Kairos** representa o tempo qualitativo, o momento certo, a oportunidade perfeita. Diferente de *Chronos* (tempo quantitativo), Kairos é sobre presença, significado e conexão.

Acreditamos que a verdadeira produtividade nasce da presença consciente e do equilíbrio entre fazer e ser, entre eficiência e humanidade, entre planejamento e espontaneidade sagrada.

## Funcionalidades Principais

### 🎯 Matriz Adaptada de Presença
Uma evolução da matriz de Eisenhower que inclui o **Eixo da Presença** para momentos de improviso consciente e conexão humana profunda.

**Os 5 Quadrantes:**
- **Urgente + Importante**: Crises e emergências
- **Importante + Não Urgente**: Planejamento e prevenção  
- **Urgente + Não Importante**: Interrupções e distrações
- **Não Urgente + Não Importante**: Atividades triviais
- **Eixo da Presença**: Improvisos conscientes - porque a vida acontece

### 🤖 IA como Mentor de Vida
Inteligência artificial que aprende seus padrões e oferece insights personalizados para otimizar seu tempo e energia:
- Reorganização automática quando imprevistos surgem
- Sugestões de pausas antes que o estresse apareça
- Aprendizado do seu ritmo pessoal único
- Otimização baseada em padrões de produtividade

### 🤝 Integração Humana Profunda
Conecte suas tarefas com pessoas importantes, fortalecendo relacionamentos:
- Contatos diretamente vinculados aos eventos
- Facilitação de interações significativas
- Transformação de tarefas em experiências compartilhadas
- Sistema de lembretes para nutrir relacionamentos

### 🧘‍♀️ Rituais Personalizados
Crie e mantenha rituais diários que nutrem sua presença e bem-estar:
- **Respiração Matinal**: Comece o dia com clareza
- **Meditações Guiadas**: Momentos de paz estruturados
- **Pausas Conscientes**: Intervalos de presença durante o dia
- **Sistema de Criação**: Desenvolva seus próprios rituais

### 📝 Reflexão Diária Guiada
Momentos estruturados de autoconhecimento baseados nos **4 Pilares da Presença**:
- **🙏 Gratidão**: Reconhecer e celebrar o que temos
- **💚 Perdão**: Liberar o que não serve mais
- **🌱 Aprendizado**: Crescer continuamente
- **💪 Superação**: Atravessar desafios com coragem

### 📈 Insights Inteligentes
Análises profundas dos seus padrões de comportamento e sugestões para otimização contínua da sua jornada.

## Tecnologias Utilizadas

### Frontend
- **React 18**: Interface de usuário moderna e responsiva
- **CSS3**: Estilização avançada com gradientes e animações
- **JavaScript ES6+**: Lógica de aplicação moderna

### Backend
- **Flask**: Framework web Python para APIs RESTful
- **SQLAlchemy**: ORM para gerenciamento de banco de dados
- **SQLite**: Banco de dados leve e eficiente
- **Flask-CORS**: Suporte para requisições cross-origin

### IA Engine
- **Python**: Linguagem principal para algoritmos de IA
- **NumPy**: Computação numérica e análise de dados
- **Scikit-learn**: Machine learning e análise preditiva
- **Algoritmos Personalizados**: Otimização de tarefas e análise de presença

## Estrutura do Projeto

```
Kairos/
├── README.md                    # Documentação principal
├── package.json                 # Dependências do frontend
├── package-lock.json           # Lock file das dependências
├── public/                     # Arquivos públicos do React
│   ├── index.html
│   ├── manifest.json
│   └── robots.txt
├── src/                        # Código fonte do frontend
│   ├── components/             # Componentes React
│   │   ├── MatrixQuadrant.jsx
│   │   ├── MatrixQuadrant.css
│   │   ├── RitualCard.jsx
│   │   ├── RitualCard.css
│   │   ├── ReflectionForm.jsx
│   │   └── ReflectionForm.css
│   ├── App.jsx                 # Componente principal
│   ├── App.css                 # Estilos principais
│   ├── index.js                # Ponto de entrada
│   └── index.css               # Estilos globais
├── backend/                    # Backend Flask
│   └── kairos-backend/
│       ├── src/
│       │   ├── models/         # Modelos de dados
│       │   ├── routes/         # Rotas da API
│       │   ├── static/         # Arquivos estáticos
│       │   └── main.py         # Aplicação principal
│       ├── venv/               # Ambiente virtual Python
│       └── requirements.txt    # Dependências Python
├── ai-engine/                  # Motor de IA
│   ├── task-optimizer.py       # Otimização de tarefas
│   ├── presence-analyzer.py    # Análise de presença
│   ├── recommendation-engine.py # Sistema de recomendações
│   ├── venv/                   # Ambiente virtual Python
│   └── requirements.txt        # Dependências Python
├── docs/                       # Documentação
│   ├── README.md               # Este arquivo
│   ├── API.md                  # Documentação da API
│   ├── DEPLOYMENT.md           # Guia de implantação
│   └── DEVELOPMENT.md          # Guia de desenvolvimento
└── dist/                       # Build de produção
```

## Instalação e Configuração

### Pré-requisitos
- Node.js 18+
- Python 3.11+
- Git

### Frontend
```bash
# Instalar dependências
npm install

# Executar em desenvolvimento
npm start

# Build para produção
npm run build
```

### Backend
```bash
# Navegar para o backend
cd backend/kairos-backend

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Executar servidor
python src/main.py
```

### IA Engine
```bash
# Navegar para o AI engine
cd ai-engine

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Testar componentes
python task-optimizer.py
python presence-analyzer.py
python recommendation-engine.py
```

## Uso

### Interface Principal
1. **Matriz**: Visualize e organize suas tarefas nos 5 quadrantes
2. **Rituais**: Gerencie e execute seus rituais de presença
3. **Reflexão**: Realize sua reflexão diária guiada

### API Endpoints
- `GET /api/health` - Status da API
- `GET /api/tasks` - Listar tarefas
- `POST /api/tasks` - Criar tarefa
- `GET /api/rituals` - Listar rituais
- `POST /api/rituals` - Criar ritual
- `GET /api/reflections/daily` - Reflexão diária

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Contato

Projeto Kairos - Companion of Presence
- Website: https://ohgoxmtg.manus.space
- Repositório: https://github.com/GabrielJaccoud/Kairos

---

*Desenvolvido com presença e propósito* ✨

