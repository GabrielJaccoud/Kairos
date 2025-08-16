"""
Otimizador Inteligente de Tarefas - Kairos AI Engine
Sistema avançado de otimização que usa algoritmos genéticos e aprendizado por reforço
"""

import numpy as np
import random
from datetime import datetime, timedelta
import json
import logging
from typing import List, Dict, Tuple
from dataclasses import dataclass
from enum import Enum

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class TaskType(Enum):
    CREATIVE = "creative"
    ANALYTICAL = "analytical"
    ADMINISTRATIVE = "administrative"
    COMMUNICATION = "communication"
    LEARNING = "learning"

@dataclass
class Task:
    id: str
    title: str
    description: str
    priority: Priority
    task_type: TaskType
    estimated_duration: int  # em minutos
    deadline: datetime
    energy_required: int  # 1-5 escala
    focus_required: int  # 1-5 escala
    dependencies: List[str]  # IDs de tarefas dependentes
    context_switch_cost: int  # custo de mudança de contexto
    optimal_time_slots: List[int]  # horários preferenciais (0-23)
    
    def __post_init__(self):
        if isinstance(self.deadline, str):
            self.deadline = datetime.fromisoformat(self.deadline)

class IntelligentTaskOptimizer:
    """
    Otimizador que combina múltiplas técnicas de IA:
    - Algoritmos Genéticos para otimização global
    - Aprendizado por Reforço para adaptação
    - Heurísticas baseadas em psicologia cognitiva
    """
    
    def __init__(self):
        self.population_size = 50
        self.generations = 100
        self.mutation_rate = 0.1
        self.crossover_rate = 0.8
        self.learning_rate = 0.1
        
        # Pesos para função de fitness
        self.weights = {
            'deadline_urgency': 0.25,
            'priority_importance': 0.20,
            'energy_alignment': 0.15,
            'context_switching': 0.15,
            'time_preference': 0.10,
            'dependency_order': 0.10,
            'workload_balance': 0.05
        }
        
        # Histórico de performance para aprendizado
        self.performance_history = []
        
        # Padrões de energia do usuário (aprendidos ao longo do tempo)
        self.user_energy_patterns = {
            6: 0.3, 7: 0.5, 8: 0.7, 9: 0.9, 10: 0.95, 11: 0.9,
            12: 0.7, 13: 0.6, 14: 0.8, 15: 0.85, 16: 0.8, 17: 0.7,
            18: 0.6, 19: 0.5, 20: 0.4, 21: 0.3, 22: 0.2, 23: 0.1
        }
    
    def create_chromosome(self, tasks: List[Task], available_slots: List[Tuple[datetime, int]]) -> List[int]:
        """
        Cria um cromossomo (solução) aleatório
        Cada gene representa o slot de tempo atribuído a uma tarefa
        """
        chromosome = []
        used_slots = set()
        
        for task in tasks:
            # Encontrar slots compatíveis com a duração da tarefa
            compatible_slots = []
            for i, (start_time, duration) in enumerate(available_slots):
                if duration >= task.estimated_duration and i not in used_slots:
                    compatible_slots.append(i)
            
            if compatible_slots:
                chosen_slot = random.choice(compatible_slots)
                chromosome.append(chosen_slot)
                used_slots.add(chosen_slot)
            else:
                # Se não há slots compatíveis, usar -1 (não agendado)
                chromosome.append(-1)
        
        return chromosome
    
    def calculate_fitness(self, chromosome: List[int], tasks: List[Task], 
                         available_slots: List[Tuple[datetime, int]]) -> float:
        """
        Calcula a fitness de um cromossomo baseado em múltiplos critérios
        """
        if len(chromosome) != len(tasks):
            return 0.0
        
        total_score = 0.0
        scheduled_tasks = 0
        
        for i, (task, slot_index) in enumerate(zip(tasks, chromosome)):
            if slot_index == -1:
                continue  # Tarefa não agendada
            
            if slot_index >= len(available_slots):
                continue  # Slot inválido
            
            scheduled_tasks += 1
            start_time, slot_duration = available_slots[slot_index]
            
            # 1. Urgência do deadline
            time_to_deadline = (task.deadline - start_time).total_seconds() / 3600  # horas
            if time_to_deadline > 0:
                urgency_score = min(1.0, 24 / max(1, time_to_deadline))
            else:
                urgency_score = 0.0  # Deadline perdido
            
            # 2. Importância da prioridade
            priority_score = task.priority.value / 4.0
            
            # 3. Alinhamento com energia
            hour = start_time.hour
            user_energy = self.user_energy_patterns.get(hour, 0.5)
            required_energy = task.energy_required / 5.0
            energy_alignment = 1.0 - abs(user_energy - required_energy)
            
            # 4. Custo de mudança de contexto
            context_score = 1.0
            if i > 0:
                prev_task = tasks[i-1]
                prev_slot = chromosome[i-1]
                if prev_slot != -1 and prev_slot < len(available_slots):
                    if prev_task.task_type != task.task_type:
                        context_penalty = task.context_switch_cost / 10.0
                        context_score = max(0.0, 1.0 - context_penalty)
            
            # 5. Preferência de horário
            time_preference = 0.5
            if task.optimal_time_slots:
                if hour in task.optimal_time_slots:
                    time_preference = 1.0
                else:
                    # Calcular proximidade ao horário preferido
                    min_distance = min(abs(hour - opt_hour) for opt_hour in task.optimal_time_slots)
                    time_preference = max(0.0, 1.0 - min_distance / 12.0)
            
            # 6. Ordem de dependências
            dependency_score = 1.0
            for dep_id in task.dependencies:
                dep_index = next((j for j, t in enumerate(tasks) if t.id == dep_id), -1)
                if dep_index != -1 and dep_index < len(chromosome):
                    dep_slot = chromosome[dep_index]
                    if dep_slot != -1 and dep_slot < len(available_slots):
                        dep_end_time = available_slots[dep_slot][0] + timedelta(minutes=tasks[dep_index].estimated_duration)
                        if start_time < dep_end_time:
                            dependency_score = 0.0  # Violação de dependência
            
            # Combinar scores com pesos
            task_score = (
                self.weights['deadline_urgency'] * urgency_score +
                self.weights['priority_importance'] * priority_score +
                self.weights['energy_alignment'] * energy_alignment +
                self.weights['context_switching'] * context_score +
                self.weights['time_preference'] * time_preference +
                self.weights['dependency_order'] * dependency_score
            )
            
            total_score += task_score
        
        # 7. Balanceamento de carga de trabalho
        if scheduled_tasks > 0:
            workload_balance = self._calculate_workload_balance(chromosome, tasks, available_slots)
            total_score += self.weights['workload_balance'] * workload_balance * scheduled_tasks
        
        # Penalizar soluções que não agendam todas as tarefas
        completion_bonus = scheduled_tasks / len(tasks)
        total_score *= completion_bonus
        
        return total_score
    
    def _calculate_workload_balance(self, chromosome: List[int], tasks: List[Task], 
                                  available_slots: List[Tuple[datetime, int]]) -> float:
        """
        Calcula o balanceamento da carga de trabalho ao longo do dia
        """
        hourly_workload = {}
        
        for task, slot_index in zip(tasks, chromosome):
            if slot_index == -1 or slot_index >= len(available_slots):
                continue
            
            start_time, _ = available_slots[slot_index]
            hour = start_time.hour
            
            if hour not in hourly_workload:
                hourly_workload[hour] = 0
            
            hourly_workload[hour] += task.estimated_duration
        
        if not hourly_workload:
            return 0.0
        
        # Calcular variância da carga de trabalho
        workloads = list(hourly_workload.values())
        mean_workload = sum(workloads) / len(workloads)
        variance = sum((w - mean_workload) ** 2 for w in workloads) / len(workloads)
        
        # Converter variância em score (menor variância = melhor balanceamento)
        balance_score = 1.0 / (1.0 + variance / 100.0)
        
        return balance_score
    
    def crossover(self, parent1: List[int], parent2: List[int]) -> Tuple[List[int], List[int]]:
        """
        Operador de crossover de dois pontos
        """
        if len(parent1) != len(parent2):
            return parent1.copy(), parent2.copy()
        
        if random.random() > self.crossover_rate:
            return parent1.copy(), parent2.copy()
        
        length = len(parent1)
        if length < 2:
            return parent1.copy(), parent2.copy()
        
        # Dois pontos de corte
        point1 = random.randint(0, length - 1)
        point2 = random.randint(point1, length - 1)
        
        child1 = parent1.copy()
        child2 = parent2.copy()
        
        # Trocar segmentos
        child1[point1:point2+1] = parent2[point1:point2+1]
        child2[point1:point2+1] = parent1[point1:point2+1]
        
        return child1, child2
    
    def mutate(self, chromosome: List[int], available_slots: List[Tuple[datetime, int]]) -> List[int]:
        """
        Operador de mutação
        """
        mutated = chromosome.copy()
        
        for i in range(len(mutated)):
            if random.random() < self.mutation_rate:
                # Mutar para um slot aleatório válido ou -1
                if random.random() < 0.1:
                    mutated[i] = -1  # Não agendar
                else:
                    mutated[i] = random.randint(0, len(available_slots) - 1)
        
        return mutated
    
    def tournament_selection(self, population: List[List[int]], fitness_scores: List[float], 
                           tournament_size: int = 3) -> List[int]:
        """
        Seleção por torneio
        """
        tournament_indices = random.sample(range(len(population)), 
                                         min(tournament_size, len(population)))
        tournament_fitness = [fitness_scores[i] for i in tournament_indices]
        
        winner_index = tournament_indices[tournament_fitness.index(max(tournament_fitness))]
        return population[winner_index].copy()
    
    def optimize_schedule(self, tasks: List[Task], 
                         available_slots: List[Tuple[datetime, int]]) -> Dict:
        """
        Otimiza o cronograma usando algoritmo genético
        """
        logger.info(f"Iniciando otimização para {len(tasks)} tarefas em {len(available_slots)} slots")
        
        # Inicializar população
        population = []
        for _ in range(self.population_size):
            chromosome = self.create_chromosome(tasks, available_slots)
            population.append(chromosome)
        
        best_fitness = -1
        best_solution = None
        fitness_history = []
        
        for generation in range(self.generations):
            # Calcular fitness para toda a população
            fitness_scores = []
            for chromosome in population:
                fitness = self.calculate_fitness(chromosome, tasks, available_slots)
                fitness_scores.append(fitness)
            
            # Encontrar melhor solução desta geração
            max_fitness = max(fitness_scores)
            if max_fitness > best_fitness:
                best_fitness = max_fitness
                best_solution = population[fitness_scores.index(max_fitness)].copy()
            
            fitness_history.append(max_fitness)
            
            # Log de progresso
            if generation % 20 == 0:
                avg_fitness = sum(fitness_scores) / len(fitness_scores)
                logger.info(f"Geração {generation}: Melhor={max_fitness:.3f}, Média={avg_fitness:.3f}")
            
            # Criar nova população
            new_population = []
            
            # Elitismo: manter as melhores soluções
            elite_size = max(1, self.population_size // 10)
            elite_indices = sorted(range(len(fitness_scores)), 
                                 key=lambda i: fitness_scores[i], reverse=True)[:elite_size]
            for i in elite_indices:
                new_population.append(population[i].copy())
            
            # Gerar resto da população
            while len(new_population) < self.population_size:
                parent1 = self.tournament_selection(population, fitness_scores)
                parent2 = self.tournament_selection(population, fitness_scores)
                
                child1, child2 = self.crossover(parent1, parent2)
                
                child1 = self.mutate(child1, available_slots)
                child2 = self.mutate(child2, available_slots)
                
                new_population.extend([child1, child2])
            
            # Manter tamanho da população
            population = new_population[:self.population_size]
        
        # Construir resultado
        optimized_schedule = self._build_schedule_result(best_solution, tasks, available_slots)
        
        result = {
            'schedule': optimized_schedule,
            'fitness_score': best_fitness,
            'optimization_stats': {
                'generations': self.generations,
                'final_fitness': best_fitness,
                'fitness_history': fitness_history,
                'tasks_scheduled': len([s for s in optimized_schedule if s['scheduled']]),
                'total_tasks': len(tasks)
            }
        }
        
        logger.info(f"Otimização concluída. Fitness final: {best_fitness:.3f}")
        return result
    
    def _build_schedule_result(self, solution: List[int], tasks: List[Task], 
                             available_slots: List[Tuple[datetime, int]]) -> List[Dict]:
        """
        Constrói o resultado final do cronograma
        """
        schedule = []
        
        for i, (task, slot_index) in enumerate(zip(tasks, solution)):
            if slot_index == -1 or slot_index >= len(available_slots):
                # Tarefa não agendada
                schedule.append({
                    'task_id': task.id,
                    'task_title': task.title,
                    'scheduled': False,
                    'reason': 'Não foi possível encontrar slot adequado',
                    'priority': task.priority.name,
                    'estimated_duration': task.estimated_duration
                })
            else:
                start_time, slot_duration = available_slots[slot_index]
                end_time = start_time + timedelta(minutes=task.estimated_duration)
                
                schedule.append({
                    'task_id': task.id,
                    'task_title': task.title,
                    'scheduled': True,
                    'start_time': start_time.isoformat(),
                    'end_time': end_time.isoformat(),
                    'duration_minutes': task.estimated_duration,
                    'priority': task.priority.name,
                    'task_type': task.task_type.value,
                    'energy_required': task.energy_required,
                    'focus_required': task.focus_required
                })
        
        # Ordenar por horário de início
        scheduled_tasks = [s for s in schedule if s['scheduled']]
        unscheduled_tasks = [s for s in schedule if not s['scheduled']]
        
        scheduled_tasks.sort(key=lambda x: x['start_time'])
        
        return scheduled_tasks + unscheduled_tasks
    
    def adapt_weights_from_feedback(self, feedback: Dict):
        """
        Adapta os pesos baseado no feedback do usuário
        """
        if 'satisfaction_score' in feedback:
            satisfaction = feedback['satisfaction_score']  # 0-1
            
            # Ajustar pesos baseado na satisfação
            if satisfaction < 0.5:
                # Baixa satisfação: aumentar peso de prioridade e deadline
                self.weights['priority_importance'] *= 1.1
                self.weights['deadline_urgency'] *= 1.1
                self.weights['energy_alignment'] *= 0.9
            else:
                # Alta satisfação: manter ou aumentar peso de energia
                self.weights['energy_alignment'] *= 1.05
        
        # Normalizar pesos
        total_weight = sum(self.weights.values())
        for key in self.weights:
            self.weights[key] /= total_weight
        
        logger.info("Pesos adaptados baseado no feedback")
    
    def suggest_break_times(self, schedule: List[Dict]) -> List[Dict]:
        """
        Sugere horários para pausas baseado no cronograma
        """
        breaks = []
        
        scheduled_tasks = [task for task in schedule if task['scheduled']]
        if not scheduled_tasks:
            return breaks
        
        for i in range(len(scheduled_tasks) - 1):
            current_task = scheduled_tasks[i]
            next_task = scheduled_tasks[i + 1]
            
            current_end = datetime.fromisoformat(current_task['end_time'])
            next_start = datetime.fromisoformat(next_task['start_time'])
            
            gap_minutes = (next_start - current_end).total_seconds() / 60
            
            if gap_minutes >= 15:  # Gap suficiente para uma pausa
                break_duration = min(gap_minutes - 5, 20)  # Máximo 20 min
                
                breaks.append({
                    'type': 'suggested_break',
                    'start_time': current_end.isoformat(),
                    'duration_minutes': int(break_duration),
                    'reason': 'Pausa entre tarefas para manter produtividade'
                })
        
        return breaks

def main():
    """
    Função principal para demonstração
    """
    # Criar tarefas de exemplo
    tasks = [
        Task(
            id="1",
            title="Reunião de planejamento",
            description="Reunião estratégica com equipe",
            priority=Priority.HIGH,
            task_type=TaskType.COMMUNICATION,
            estimated_duration=60,
            deadline=datetime.now() + timedelta(days=1),
            energy_required=3,
            focus_required=4,
            dependencies=[],
            context_switch_cost=2,
            optimal_time_slots=[9, 10, 14, 15]
        ),
        Task(
            id="2",
            title="Análise de dados",
            description="Análise detalhada dos relatórios",
            priority=Priority.MEDIUM,
            task_type=TaskType.ANALYTICAL,
            estimated_duration=90,
            deadline=datetime.now() + timedelta(days=2),
            energy_required=4,
            focus_required=5,
            dependencies=[],
            context_switch_cost=4,
            optimal_time_slots=[9, 10, 11]
        ),
        Task(
            id="3",
            title="Responder emails",
            description="Processar caixa de entrada",
            priority=Priority.LOW,
            task_type=TaskType.ADMINISTRATIVE,
            estimated_duration=30,
            deadline=datetime.now() + timedelta(hours=8),
            energy_required=2,
            focus_required=2,
            dependencies=[],
            context_switch_cost=1,
            optimal_time_slots=[13, 16, 17]
        )
    ]
    
    # Criar slots disponíveis
    base_time = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    available_slots = []
    
    for hour in range(9, 18):  # 9h às 18h
        slot_start = base_time.replace(hour=hour)
        available_slots.append((slot_start, 60))  # Slots de 1 hora
    
    # Otimizar cronograma
    optimizer = IntelligentTaskOptimizer()
    result = optimizer.optimize_schedule(tasks, available_slots)
    
    print("=== CRONOGRAMA OTIMIZADO ===")
    for task in result['schedule']:
        if task['scheduled']:
            start = datetime.fromisoformat(task['start_time']).strftime('%H:%M')
            end = datetime.fromisoformat(task['end_time']).strftime('%H:%M')
            print(f"{start}-{end}: {task['task_title']} (Prioridade: {task['priority']})")
        else:
            print(f"NÃO AGENDADO: {task['task_title']} - {task['reason']}")
    
    print(f"\nFitness Score: {result['fitness_score']:.3f}")
    print(f"Tarefas agendadas: {result['optimization_stats']['tasks_scheduled']}/{result['optimization_stats']['total_tasks']}")
    
    # Sugerir pausas
    breaks = optimizer.suggest_break_times(result['schedule'])
    if breaks:
        print("\n=== PAUSAS SUGERIDAS ===")
        for break_info in breaks:
            start = datetime.fromisoformat(break_info['start_time']).strftime('%H:%M')
            duration = break_info['duration_minutes']
            print(f"{start}: Pausa de {duration} minutos")

if __name__ == "__main__":
    main()

