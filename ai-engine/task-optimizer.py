# ai-engine/task-optimizer.py
import json
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any

class TaskOptimizer:
    def __init__(self):
        self.user_preferences = {}
        self.energy_patterns = {}
        self.presence_weights = {
            'morning': 0.8,
            'afternoon': 0.6,
            'evening': 0.9
        }
    
    def optimize_schedule(self, tasks: List[Dict], user_profile: Dict = None) -> List[Dict]:
        """Reorganiza tarefas com base em prioridades, energia e presença"""
        if not tasks:
            return []
        
        # Calcular scores de prioridade usando algoritmo avançado
        for task in tasks:
            task['ai_priority_score'] = self._calculate_priority_score(task, user_profile)
            task['ai_energy_requirement'] = self._determine_energy_requirement(task)
            task['ai_suggested_time'] = self._suggest_optimal_time(task, user_profile)
        
        # Ordenar por score de prioridade
        optimized_tasks = sorted(tasks, key=lambda x: x.get('ai_priority_score', 0), reverse=True)
        
        # Aplicar algoritmo de balanceamento de carga cognitiva
        balanced_tasks = self._balance_cognitive_load(optimized_tasks)
        
        return balanced_tasks
    
    def _calculate_priority_score(self, task: Dict, user_profile: Dict = None) -> float:
        """Calcula score de prioridade usando múltiplos fatores"""
        base_score = 0.0
        
        # Fator de importância (peso: 40%)
        if task.get('importance_level') == 'high':
            base_score += 0.4
        elif task.get('importance_level') == 'medium':
            base_score += 0.2
        
        # Fator de urgência (peso: 30%)
        if task.get('urgency_level') == 'high':
            base_score += 0.3
        elif task.get('urgency_level') == 'medium':
            base_score += 0.15
        
        # Fator de presença (peso: 20%)
        if task.get('presence_axis'):
            base_score += 0.2
        
        # Fator temporal - proximidade do deadline (peso: 10%)
        if task.get('scheduled_for'):
            try:
                scheduled_time = datetime.fromisoformat(task['scheduled_for'].replace('Z', '+00:00'))
                time_diff = (scheduled_time - datetime.now()).total_seconds() / 3600  # horas
                if time_diff < 2:  # Menos de 2 horas
                    base_score += 0.1
                elif time_diff < 24:  # Menos de 1 dia
                    base_score += 0.05
            except:
                pass
        
        # Ajustes baseados no perfil do usuário
        if user_profile:
            # Se o usuário tem preferência por tarefas criativas de manhã
            if user_profile.get('creative_peak') == 'morning' and task.get('type') == 'creative':
                base_score += 0.05
            
            # Se o usuário prefere tarefas administrativas à tarde
            if user_profile.get('admin_peak') == 'afternoon' and task.get('type') == 'administrative':
                base_score += 0.05
        
        return min(base_score, 1.0)  # Máximo de 1.0
    
    def _determine_energy_requirement(self, task: Dict) -> str:
        """Determina o nível de energia necessário para a tarefa"""
        score = task.get('ai_priority_score', 0)
        duration = task.get('estimated_duration_hours', 1)
        complexity = task.get('complexity_level', 'medium')
        
        # Algoritmo baseado em múltiplos fatores
        energy_score = 0
        
        if score > 0.8:
            energy_score += 3
        elif score > 0.5:
            energy_score += 2
        else:
            energy_score += 1
        
        if duration > 3:
            energy_score += 2
        elif duration > 1:
            energy_score += 1
        
        if complexity == 'high':
            energy_score += 2
        elif complexity == 'medium':
            energy_score += 1
        
        if energy_score >= 6:
            return 'high'
        elif energy_score >= 4:
            return 'medium'
        else:
            return 'low'
    
    def _suggest_optimal_time(self, task: Dict, user_profile: Dict = None) -> str:
        """Sugere o horário ótimo para a tarefa"""
        current_time = datetime.now()
        energy_req = task.get('ai_energy_requirement', 'medium')
        
        # Horários padrão baseados em energia
        if energy_req == 'high':
            # Tarefas de alta energia: manhã (9h-11h)
            suggested_time = current_time.replace(hour=9, minute=0, second=0, microsecond=0)
            if suggested_time < current_time:
                suggested_time += timedelta(days=1)
        elif energy_req == 'medium':
            # Tarefas de média energia: meio da manhã ou início da tarde (10h-12h ou 14h-16h)
            suggested_time = current_time.replace(hour=10, minute=0, second=0, microsecond=0)
            if suggested_time < current_time:
                suggested_time = current_time.replace(hour=14, minute=0, second=0, microsecond=0)
                if suggested_time < current_time:
                    suggested_time += timedelta(days=1)
                    suggested_time = suggested_time.replace(hour=10)
        else:
            # Tarefas de baixa energia: qualquer horário disponível
            suggested_time = current_time + timedelta(hours=1)
        
        # Ajustar para horário comercial se necessário
        if task.get('requires_business_hours', False):
            if suggested_time.hour < 9:
                suggested_time = suggested_time.replace(hour=9)
            elif suggested_time.hour > 17:
                suggested_time = suggested_time.replace(hour=9) + timedelta(days=1)
        
        return suggested_time.isoformat()
    
    def _balance_cognitive_load(self, tasks: List[Dict]) -> List[Dict]:
        """Balanceia a carga cognitiva ao longo do dia"""
        if len(tasks) <= 1:
            return tasks
        
        high_energy_tasks = [t for t in tasks if t.get('ai_energy_requirement') == 'high']
        medium_energy_tasks = [t for t in tasks if t.get('ai_energy_requirement') == 'medium']
        low_energy_tasks = [t for t in tasks if t.get('ai_energy_requirement') == 'low']
        
        # Intercalar tarefas de diferentes níveis de energia
        balanced = []
        max_len = max(len(high_energy_tasks), len(medium_energy_tasks), len(low_energy_tasks))
        
        for i in range(max_len):
            if i < len(high_energy_tasks):
                balanced.append(high_energy_tasks[i])
            if i < len(low_energy_tasks):
                balanced.append(low_energy_tasks[i])
            if i < len(medium_energy_tasks):
                balanced.append(medium_energy_tasks[i])
        
        return balanced
    
    def suggest_breaks(self, tasks: List[Dict]) -> List[Dict]:
        """Sugere pausas estratégicas baseadas na carga cognitiva"""
        breaks = []
        cumulative_energy = 0
        
        for i, task in enumerate(tasks):
            # Calcular energia cumulativa
            if task.get('ai_energy_requirement') == 'high':
                cumulative_energy += 3
            elif task.get('ai_energy_requirement') == 'medium':
                cumulative_energy += 2
            else:
                cumulative_energy += 1
            
            # Sugerir pausa se energia cumulativa for alta
            if cumulative_energy >= 6 and i < len(tasks) - 1:
                break_type = self._determine_break_type(cumulative_energy)
                breaks.append({
                    'position': i + 1,
                    'type': break_type['type'],
                    'duration': break_type['duration'],
                    'suggestion': break_type['suggestion'],
                    'ai_reasoning': f'Pausa recomendada após {cumulative_energy} pontos de energia cumulativa'
                })
                cumulative_energy = 0  # Reset após a pausa
        
        return breaks
    
    def _determine_break_type(self, energy_level: int) -> Dict[str, Any]:
        """Determina o tipo de pausa baseado no nível de energia"""
        if energy_level >= 9:
            return {
                'type': 'long_presence_break',
                'duration': 15,
                'suggestion': 'Meditação guiada de 15 minutos ou caminhada consciente'
            }
        elif energy_level >= 6:
            return {
                'type': 'medium_presence_break',
                'duration': 10,
                'suggestion': 'Respiração profunda e alongamento suave'
            }
        else:
            return {
                'type': 'short_presence_break',
                'duration': 5,
                'suggestion': 'Pausa respiratória consciente'
            }
    
    def analyze_productivity_patterns(self, completed_tasks: List[Dict]) -> Dict[str, Any]:
        """Analisa padrões de produtividade para melhorar futuras otimizações"""
        if not completed_tasks:
            return {'message': 'Dados insuficientes para análise'}
        
        # Análise de horários mais produtivos
        hourly_productivity = {}
        for task in completed_tasks:
            if task.get('completed_at'):
                try:
                    completed_time = datetime.fromisoformat(task['completed_at'].replace('Z', '+00:00'))
                    hour = completed_time.hour
                    if hour not in hourly_productivity:
                        hourly_productivity[hour] = []
                    
                    # Score baseado na eficiência (assumindo que temos dados de tempo estimado vs real)
                    efficiency_score = task.get('efficiency_score', 0.8)  # Default 80%
                    hourly_productivity[hour].append(efficiency_score)
                except:
                    continue
        
        # Calcular médias por hora
        hourly_averages = {
            hour: np.mean(scores) for hour, scores in hourly_productivity.items()
        }
        
        # Identificar picos de produtividade
        if hourly_averages:
            best_hour = max(hourly_averages, key=hourly_averages.get)
            worst_hour = min(hourly_averages, key=hourly_averages.get)
        else:
            best_hour = worst_hour = None
        
        return {
            'hourly_productivity': hourly_averages,
            'peak_productivity_hour': best_hour,
            'lowest_productivity_hour': worst_hour,
            'total_tasks_analyzed': len(completed_tasks),
            'recommendations': self._generate_productivity_recommendations(hourly_averages)
        }
    
    def _generate_productivity_recommendations(self, hourly_data: Dict[int, float]) -> List[str]:
        """Gera recomendações baseadas nos padrões de produtividade"""
        recommendations = []
        
        if not hourly_data:
            return ['Colete mais dados completando tarefas para receber recomendações personalizadas']
        
        # Encontrar padrões
        morning_hours = [h for h in hourly_data.keys() if 6 <= h <= 11]
        afternoon_hours = [h for h in hourly_data.keys() if 12 <= h <= 17]
        evening_hours = [h for h in hourly_data.keys() if 18 <= h <= 22]
        
        if morning_hours:
            morning_avg = np.mean([hourly_data[h] for h in morning_hours])
            if morning_avg > 0.8:
                recommendations.append('Você é mais produtivo pela manhã. Agende tarefas importantes entre 6h-11h.')
        
        if afternoon_hours:
            afternoon_avg = np.mean([hourly_data[h] for h in afternoon_hours])
            if afternoon_avg > 0.8:
                recommendations.append('Sua produtividade à tarde é excelente. Use este período para tarefas complexas.')
        
        if evening_hours:
            evening_avg = np.mean([hourly_data[h] for h in evening_hours])
            if evening_avg < 0.6:
                recommendations.append('Evite tarefas complexas à noite. Use este período para reflexão e planejamento.')
        
        return recommendations if recommendations else ['Continue coletando dados para recomendações mais precisas']

def optimize_tasks_api(tasks: List[Dict], user_profile: Dict = None) -> List[Dict]:
    """Função de API para otimização de tarefas"""
    optimizer = TaskOptimizer()
    return optimizer.optimize_schedule(tasks, user_profile)

if __name__ == "__main__":
    # Exemplo de uso avançado
    sample_tasks = [
        {
            "title": "Reunião Estratégica",
            "importance_level": "high",
            "urgency_level": "high",
            "presence_axis": False,
            "estimated_duration_hours": 2,
            "complexity_level": "high",
            "type": "meeting",
            "requires_business_hours": True
        },
        {
            "title": "Estudos Profundos",
            "importance_level": "high",
            "urgency_level": "low",
            "presence_axis": False,
            "estimated_duration_hours": 3,
            "complexity_level": "high",
            "type": "creative"
        },
        {
            "title": "Organizar emails",
            "importance_level": "low",
            "urgency_level": "high",
            "presence_axis": False,
            "estimated_duration_hours": 1,
            "complexity_level": "low",
            "type": "administrative"
        },
        {
            "title": "Pausa respiratória",
            "importance_level": "medium",
            "urgency_level": "low",
            "presence_axis": True,
            "estimated_duration_hours": 0.1,
            "complexity_level": "low",
            "type": "wellness"
        }
    ]
    
    user_profile = {
        "creative_peak": "morning",
        "admin_peak": "afternoon",
        "energy_pattern": "morning_person"
    }
    
    optimizer = TaskOptimizer()
    optimized_tasks = optimizer.optimize_schedule(sample_tasks, user_profile)
    suggested_breaks = optimizer.suggest_breaks(optimized_tasks)
    
    print("=== TAREFAS OTIMIZADAS ===")
    for i, task in enumerate(optimized_tasks, 1):
        print(f"{i}. {task['title']}")
        print(f"   Score: {task['ai_priority_score']}")
        print(f"   Energia: {task['ai_energy_requirement']}")
        print(f"   Horário sugerido: {task['ai_suggested_time']}")
        print()
    
    print("=== PAUSAS SUGERIDAS ===")
    for break_info in suggested_breaks:
        print(f"Posição {break_info['position']}: {break_info['suggestion']} ({break_info['duration']} min)")
        print(f"   Razão: {break_info['ai_reasoning']}")
        print()
