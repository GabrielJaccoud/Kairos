# Documentação da API - Kairos

## Visão Geral

A API do Kairos fornece endpoints RESTful para gerenciar tarefas, rituais, reflexões e análises de presença. Todas as respostas são em formato JSON e seguem padrões REST.

## Base URL

```
http://localhost:5000/api
```

## Autenticação

Atualmente, a API não requer autenticação para desenvolvimento. Em produção, será implementado sistema de autenticação JWT.

## Endpoints

### Health Check

#### GET /health
Verifica o status da API.

**Resposta:**
```json
{
  "status": "healthy",
  "message": "Kairos API está funcionando",
  "version": "1.0.0"
}
```

---

## Tarefas (Tasks)

### GET /tasks
Lista todas as tarefas do usuário.

**Parâmetros de Query:**
- `user_id` (opcional): ID do usuário (padrão: 1)

**Resposta:**
```json
{
  "success": true,
  "tasks": [
    {
      "id": 1,
      "title": "Reunião com Cliente",
      "description": "Apresentar proposta do projeto",
      "importance_level": "high",
      "urgency_level": "high",
      "presence_axis": false,
      "contacts": "[\"Maria Silva\", \"João Santos\"]",
      "created_at": "2024-01-15T10:00:00",
      "updated_at": "2024-01-15T10:00:00",
      "scheduled_for": "2024-01-15T14:00:00",
      "completed_at": null,
      "status": "pending",
      "ai_priority_score": 0.95,
      "ai_energy_requirement": "high",
      "ai_suggested_time": "2024-01-15T09:00:00",
      "user_id": 1
    }
  ]
}
```

### POST /tasks
Cria uma nova tarefa.

**Body:**
```json
{
  "title": "Nova Tarefa",
  "description": "Descrição da tarefa",
  "importance_level": "high|medium|low",
  "urgency_level": "high|medium|low",
  "presence_axis": false,
  "contacts": ["Contato 1", "Contato 2"],
  "scheduled_for": "2024-01-15T14:00:00Z",
  "user_id": 1
}
```

**Resposta:**
```json
{
  "success": true,
  "task": { /* objeto da tarefa criada */ },
  "message": "Tarefa criada com sucesso"
}
```

### PUT /tasks/{task_id}
Atualiza uma tarefa existente.

**Body:** (campos opcionais)
```json
{
  "title": "Título atualizado",
  "status": "completed|in_progress|pending"
}
```

### DELETE /tasks/{task_id}
Remove uma tarefa.

**Resposta:**
```json
{
  "success": true,
  "message": "Tarefa deletada com sucesso"
}
```

### GET /tasks/matrix
Retorna tarefas organizadas pela matriz adaptada.

**Resposta:**
```json
{
  "success": true,
  "matrix": {
    "urgent_important": [/* tarefas */],
    "important_not_urgent": [/* tarefas */],
    "urgent_not_important": [/* tarefas */],
    "not_urgent_not_important": [/* tarefas */],
    "presence": [/* tarefas */]
  }
}
```

### POST /tasks/ai-optimize
Otimiza tarefas usando IA.

**Resposta:**
```json
{
  "success": true,
  "optimized_tasks": [/* tarefas otimizadas */],
  "message": "Tarefas otimizadas pela IA"
}
```

---

## Rituais (Rituals)

### GET /rituals
Lista todos os rituais do usuário.

**Resposta:**
```json
{
  "success": true,
  "rituals": [
    {
      "id": 1,
      "name": "Respiração Matinal",
      "description": "Comece o dia com clareza",
      "ritual_type": "morning",
      "duration_minutes": 5,
      "instructions": "1. Sente-se confortavelmente\n2. Respire profundamente",
      "is_active": true,
      "frequency": "daily",
      "scheduled_time": "07:00",
      "created_at": "2024-01-15T10:00:00",
      "updated_at": "2024-01-15T10:00:00",
      "user_id": 1
    }
  ]
}
```

### POST /rituals
Cria um novo ritual.

**Body:**
```json
{
  "name": "Novo Ritual",
  "description": "Descrição do ritual",
  "ritual_type": "morning|evening|break|custom",
  "duration_minutes": 5,
  "instructions": "Instruções do ritual",
  "frequency": "daily|weekly|custom",
  "scheduled_time": "07:00",
  "user_id": 1
}
```

### POST /rituals/{ritual_id}/execute
Registra execução de um ritual.

**Body:**
```json
{
  "duration_actual": 5,
  "completion_rating": 4,
  "notes": "Ritual executado com sucesso"
}
```

### GET /rituals/templates
Retorna templates de rituais predefinidos.

**Resposta:**
```json
{
  "success": true,
  "templates": [
    {
      "name": "Respiração Matinal",
      "description": "Comece o dia com clareza e presença",
      "ritual_type": "morning",
      "duration_minutes": 5,
      "instructions": "1. Sente-se confortavelmente...",
      "scheduled_time": "07:00"
    }
  ]
}
```

### GET /rituals/{ritual_id}/stats
Estatísticas de execução de um ritual.

**Resposta:**
```json
{
  "success": true,
  "stats": {
    "total_executions": 25,
    "average_rating": 4.2,
    "average_duration": 5.5,
    "consistency_score": 85.0,
    "recent_executions": 5
  }
}
```

---

## Reflexões (Reflections)

### GET /reflections/daily
Obtém reflexão diária.

**Parâmetros de Query:**
- `user_id` (opcional): ID do usuário
- `date` (opcional): Data no formato YYYY-MM-DD

**Resposta:**
```json
{
  "success": true,
  "reflection": {
    "id": 1,
    "reflection_date": "2024-01-15",
    "gratitude": "Grato pela família e saúde",
    "forgiveness": "Perdoo minha impaciência hoje",
    "learning": "Aprendi sobre paciência",
    "overcoming": "Superei o medo da apresentação",
    "day_rating": 8,
    "presence_level": 7,
    "energy_level": 6,
    "ai_insights": "Você teve um dia produtivo...",
    "ai_suggestions": "Considere mais pausas amanhã...",
    "created_at": "2024-01-15T22:00:00",
    "updated_at": "2024-01-15T22:00:00",
    "user_id": 1
  }
}
```

### POST /reflections/daily
Cria ou atualiza reflexão diária.

**Body:**
```json
{
  "gratitude": "Texto da gratidão",
  "forgiveness": "Texto do perdão",
  "learning": "Texto do aprendizado",
  "overcoming": "Texto da superação",
  "day_rating": 8,
  "presence_level": 7,
  "energy_level": 6,
  "reflection_date": "2024-01-15",
  "user_id": 1
}
```

### POST /reflections/presence-log
Registra um momento de presença.

**Body:**
```json
{
  "activity": "Meditação",
  "presence_score": 8,
  "mood": "calmo",
  "context": "casa",
  "notes": "Momento muito presente",
  "user_id": 1
}
```

### GET /reflections/presence-stats
Estatísticas de presença.

**Parâmetros de Query:**
- `user_id` (opcional): ID do usuário
- `days` (opcional): Número de dias para análise (padrão: 7)

**Resposta:**
```json
{
  "success": true,
  "stats": {
    "average_presence": 7.5,
    "total_logs": 15,
    "mood_distribution": {
      "calmo": 5,
      "focado": 3,
      "relaxado": 7
    },
    "context_distribution": {
      "trabalho": 8,
      "casa": 7
    },
    "daily_averages": [
      {
        "date": "2024-01-15",
        "average_presence": 7.8
      }
    ]
  }
}
```

### GET /reflections/weekly-report
Relatório semanal de presença.

**Resposta:**
```json
{
  "success": true,
  "report": {
    "total_reflections": 5,
    "average_day_rating": 7.2,
    "average_presence_level": 7.8,
    "average_energy_level": 6.5,
    "consistency_score": 71.4,
    "insights": ["Insight 1", "Insight 2"],
    "reflections": [/* reflexões da semana */]
  }
}
```

---

## AI Engine Endpoints (Integrados via Backend)

O AI Engine não expõe endpoints diretamente, mas suas funcionalidades são acessadas através dos endpoints do Backend Flask. As chamadas para os modelos de IA são feitas internamente pela API.

### POST /tasks/ai-optimize
Otimiza tarefas usando o `Intelligent Task Optimizer` do AI Engine.

**Body:**
```json
{
  "tasks": [
    { "id": 1, "title": "Tarefa A", "duration": 60, "priority": "high" },
    { "id": 2, "title": "Tarefa B", "duration": 30, "priority": "medium" }
  ]
}
```

**Resposta:**
```json
{
  "success": true,
  "optimized_tasks": [/* tarefas otimizadas com sugestões de agendamento e prioridade */],
  "message": "Tarefas otimizadas pela IA"
}
```

### POST /reflections/analyze-presence
Analisa dados de presença usando o `Advanced Presence Analyzer`.

**Body:**
```json
{
  "user_data": [
    { "date": "2024-01-01", "presence_score": 7, "energy_level": 8 },
    { "date": "2024-01-02", "presence_score": 6, "energy_level": 7 }
  ]
}
```

**Resposta:**
```json
{
  "success": true,
  "analysis_results": {
    "peak_hours": "10:00-12:00",
    "energy_cycles": "manhã alta, tarde baixa",
    "stress_indicators": "nenhum"
  },
  "message": "Análise de presença concluída"
}
```

### POST /rituals/suggest-adaptive
Sugere rituais adaptativos usando o `Adaptive Ritual Engine`.

**Body:**
```json
{
  "user_state": {
    "current_energy": 7,
    "time_available": 15,
    "mood": "estressado"
  }
}
```

**Resposta:**
```json
{
  "success": true,
  "suggested_rituals": [
    { "name": "Respiração Rápida", "duration": 5, "type": "break" }
  ],
  "message": "Rituais adaptativos sugeridos"
}
```

---

## Códigos de Status HTTP

- `200 OK`: Requisição bem-sucedida
- `201 Created`: Recurso criado com sucesso
- `400 Bad Request`: Dados inválidos na requisição
- `404 Not Found`: Recurso não encontrado
- `500 Internal Server Error`: Erro interno do servidor

## Tratamento de Erros

Todas as respostas de erro seguem o formato:

```json
{
  "success": false,
  "error": "Mensagem de erro descritiva"
}
```

## Exemplos de Uso

### Criar uma tarefa no Eixo da Presença

```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Pausa Consciente",
    "description": "Momento de respiração e presença",
    "importance_level": "medium",
    "urgency_level": "low",
    "presence_axis": true,
    "user_id": 1
  }'
```

### Executar um ritual

```bash
curl -X POST http://localhost:5000/api/rituals/1/execute \
  -H "Content-Type: application/json" \
  -d '{
    "duration_actual": 5,
    "completion_rating": 5,
    "notes": "Ritual muito relaxante"
  }'
```

### Salvar reflexão diária

```bash
curl -X POST http://localhost:5000/api/reflections/daily \
  -H "Content-Type: application/json" \
  -d '{
    "gratitude": "Grato pela oportunidade de crescer",
    "forgiveness": "Perdoo minha autocrítica excessiva",
    "learning": "Aprendi sobre a importância da paciência",
    "overcoming": "Superei o medo de falar em público",
    "day_rating": 8,
    "presence_level": 7,
    "energy_level": 6
  }'
```

## Versionamento

A API segue versionamento semântico. A versão atual é `v1.0.0`.

## Rate Limiting

Atualmente não há limitação de taxa implementada. Em produção, será implementado rate limiting para proteger a API.

---

*Documentação atualizada em: Janeiro 2024*

