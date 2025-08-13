
4. Role para baixo e clique em **"Commit new file"**
5. Na mensagem de commit, escreva: "Initial commit: Project structure and basic configuration"
6. Clique em **"Commit changes"**

---

### **2.2 Criar package.json**
1. Clique em **"Add file"** → **"Create new file"**
2. No campo "Name your file...", digite: `package.json`
3. Cole o seguinte conteúdo:

```json
{
  "name": "kairos-app",
  "version": "1.0.0",
  "description": "Companion of Presence - Mindful productivity tool",
  "main": "src/App.jsx",
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject",
    "ai-dev": "cd ai-engine && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt",
    "ai-start": "cd ai-engine && python3 task-optimizer.py"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "styled-components": "^5.3.6",
    "axios": "^1.3.4",
    "moment": "^2.29.4",
    "react-router-dom": "^6.8.1"
  },
  "devDependencies": {
    "@testing-library/jest-dom": "^5.16.5",
    "@testing-library/react": "^13.4.0",
    "@testing-library/user-event": "^13.5.0"
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}
