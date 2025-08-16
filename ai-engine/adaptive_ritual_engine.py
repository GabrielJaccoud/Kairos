"""
Motor de Rituais Adaptativos - Kairos AI Engine
Sistema inteligente que personaliza e adapta rituais baseado no estado do usuário
"""

import numpy as np
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RitualType(Enum):
    MORNING = "morning"
    EVENING = "evening"
    FOCUS = "focus"
    STRESS_RELIEF = "stress_relief"
    ENERGY_BOOST = "energy_boost"
    TRANSITION = "transition"
    MINDFULNESS = "mindfulness"

class RitualComponent(Enum):
    BREATHING = "breathing"
    MEDITATION = "meditation"
    MOVEMENT = "movement"
    VISUALIZATION = "visualization"
    AFFIRMATION = "affirmation"
    JOURNALING = "journaling"
    MUSIC = "music"
    NATURE_SOUNDS = "nature_sounds"

@dataclass
class RitualStep:
    id: str
    name: str
    description: str
    component: RitualComponent
    duration_seconds: int
    instructions: str
    audio_cue: Optional[str] = None
    visual_cue: Optional[str] = None
    breathing_pattern: Optional[Dict] = None
    
class AdaptiveRitualEngine:
    """
    Motor que cria e adapta rituais baseado em:
    - Estado atual do usuário (energia, stress, foco)
    - Histórico de efetividade dos rituais
    - Contexto temporal e ambiental
    - Preferências pessoais aprendidas
    """
    
    def __init__(self):
        self.ritual_library = self._initialize_ritual_library()
        self.user_preferences = {}
        self.effectiveness_history = {}
        self.adaptation_weights = {
            'user_state': 0.4,
            'historical_effectiveness': 0.3,
            'time_context': 0.2,
            'personal_preferences': 0.1
        }
        
        # Padrões de respiração
        self.breathing_patterns = {
            'calm': {'inhale': 4, 'hold': 4, 'exhale': 6, 'pause': 2},
            'energizing': {'inhale': 4, 'hold': 2, 'exhale': 4, 'pause': 1},
            'focus': {'inhale': 4, 'hold': 7, 'exhale': 8, 'pause': 0},
            'stress_relief': {'inhale': 4, 'hold': 4, 'exhale': 8, 'pause': 2}
        }
    
    def _initialize_ritual_library(self) -> Dict[RitualType, List[RitualStep]]:
        """
        Inicializa a biblioteca de componentes de rituais
        """
        library = {
            RitualType.MORNING: [
                RitualStep(
                    id="morning_breath",
                    name="Respiração Matinal",
                    description="Respiração energizante para começar o dia",
                    component=RitualComponent.BREATHING,
                    duration_seconds=180,
                    instructions="Respire profundamente seguindo o padrão energizante",
                    breathing_pattern=self.breathing_patterns['energizing']
                ),
                RitualStep(
                    id="morning_intention",
                    name="Intenção do Dia",
                    description="Definir intenção e foco para o dia",
                    component=RitualComponent.VISUALIZATION,
                    duration_seconds=120,
                    instructions="Visualize como você quer que seu dia transcorra"
                ),
                RitualStep(
                    id="morning_affirmation",
                    name="Afirmações Positivas",
                    description="Afirmações para energia e confiança",
                    component=RitualComponent.AFFIRMATION,
                    duration_seconds=60,
                    instructions="Repita mentalmente: 'Estou presente, focado e capaz'"
                ),
                RitualStep(
                    id="morning_stretch",
                    name="Alongamento Suave",
                    description="Movimentos para despertar o corpo",
                    component=RitualComponent.MOVEMENT,
                    duration_seconds=240,
                    instructions="Faça alongamentos suaves para ativar a circulação"
                )
            ],
            
            RitualType.EVENING: [
                RitualStep(
                    id="evening_reflection",
                    name="Reflexão do Dia",
                    description="Revisão consciente do dia",
                    component=RitualComponent.JOURNALING,
                    duration_seconds=300,
                    instructions="Reflita sobre 3 momentos positivos do dia"
                ),
                RitualStep(
                    id="evening_breath",
                    name="Respiração Calmante",
                    description="Respiração para relaxamento",
                    component=RitualComponent.BREATHING,
                    duration_seconds=240,
                    instructions="Respire lentamente para acalmar o sistema nervoso",
                    breathing_pattern=self.breathing_patterns['calm']
                ),
                RitualStep(
                    id="evening_gratitude",
                    name="Gratidão",
                    description="Prática de gratidão",
                    component=RitualComponent.AFFIRMATION,
                    duration_seconds=120,
                    instructions="Liste mentalmente 3 coisas pelas quais é grato"
                ),
                RitualStep(
                    id="evening_release",
                    name="Liberação do Dia",
                    description="Soltar as tensões do dia",
                    component=RitualComponent.VISUALIZATION,
                    duration_seconds=180,
                    instructions="Visualize liberando todas as tensões e preocupações"
                )
            ],
            
            RitualType.FOCUS: [
                RitualStep(
                    id="focus_breath",
                    name="Respiração para Foco",
                    description="Técnica de respiração para concentração",
                    component=RitualComponent.BREATHING,
                    duration_seconds=120,
                    instructions="Use a respiração 4-7-8 para aumentar o foco",
                    breathing_pattern=self.breathing_patterns['focus']
                ),
                RitualStep(
                    id="focus_intention",
                    name="Intenção de Foco",
                    description="Definir intenção clara para a tarefa",
                    component=RitualComponent.VISUALIZATION,
                    duration_seconds=60,
                    instructions="Visualize-se completando a tarefa com total concentração"
                ),
                RitualStep(
                    id="focus_anchor",
                    name="Âncora de Atenção",
                    description="Estabelecer ponto de ancoragem mental",
                    component=RitualComponent.MEDITATION,
                    duration_seconds=90,
                    instructions="Foque na respiração como âncora para a atenção"
                )
            ],
            
            RitualType.STRESS_RELIEF: [
                RitualStep(
                    id="stress_breath",
                    name="Respiração Anti-Stress",
                    description="Respiração para reduzir stress",
                    component=RitualComponent.BREATHING,
                    duration_seconds=300,
                    instructions="Respire lentamente, focando na expiração longa",
                    breathing_pattern=self.breathing_patterns['stress_relief']
                ),
                RitualStep(
                    id="stress_body_scan",
                    name="Escaneamento Corporal",
                    description="Relaxamento progressivo",
                    component=RitualComponent.MEDITATION,
                    duration_seconds=480,
                    instructions="Escaneie o corpo da cabeça aos pés, relaxando cada parte"
                ),
                RitualStep(
                    id="stress_release",
                    name="Liberação de Tensão",
                    description="Visualização para liberar stress",
                    component=RitualComponent.VISUALIZATION,
                    duration_seconds=240,
                    instructions="Visualize o stress saindo do corpo como fumaça"
                ),
                RitualStep(
                    id="stress_affirmation",
                    name="Afirmações Calmantes",
                    description="Frases para tranquilidade",
                    component=RitualComponent.AFFIRMATION,
                    duration_seconds=120,
                    instructions="Repita: 'Estou calmo, seguro e no controle'"
                )
            ],
            
            RitualType.ENERGY_BOOST: [
                RitualStep(
                    id="energy_breath",
                    name="Respiração Energizante",
                    description="Técnica para aumentar energia",
                    component=RitualComponent.BREATHING,
                    duration_seconds=120,
                    instructions="Respiração rápida e ritmada para ativar energia",
                    breathing_pattern=self.breathing_patterns['energizing']
                ),
                RitualStep(
                    id="energy_movement",
                    name="Movimento Ativador",
                    description="Exercícios para despertar energia",
                    component=RitualComponent.MOVEMENT,
                    duration_seconds=180,
                    instructions="Faça movimentos dinâmicos: pular, alongar, balançar braços"
                ),
                RitualStep(
                    id="energy_visualization",
                    name="Visualização de Energia",
                    description="Imaginar energia fluindo pelo corpo",
                    component=RitualComponent.VISUALIZATION,
                    duration_seconds=90,
                    instructions="Visualize luz dourada preenchendo seu corpo com energia"
                ),
                RitualStep(
                    id="energy_affirmation",
                    name="Afirmações Energéticas",
                    description="Frases para vitalidade",
                    component=RitualComponent.AFFIRMATION,
                    duration_seconds=60,
                    instructions="Repita: 'Estou cheio de energia e vitalidade'"
                )
            ]
        }
        
        return library
    
    def analyze_user_state(self, user_data: Dict) -> Dict:
        """
        Analisa o estado atual do usuário para personalizar rituais
        """
        state = {
            'energy_level': user_data.get('energy_level', 3),  # 1-5
            'stress_level': user_data.get('stress_level', 3),  # 1-5
            'focus_level': user_data.get('focus_level', 3),    # 1-5
            'mood': user_data.get('mood', 'neutral'),
            'time_of_day': user_data.get('time_of_day', datetime.now().hour),
            'available_time': user_data.get('available_time_minutes', 10),
            'environment': user_data.get('environment', 'office'),  # office, home, outdoor
            'recent_activities': user_data.get('recent_activities', [])
        }
        
        # Calcular necessidades baseadas no estado
        needs = self._calculate_needs(state)
        
        return {
            'current_state': state,
            'identified_needs': needs,
            'recommended_ritual_types': self._recommend_ritual_types(needs)
        }
    
    def _calculate_needs(self, state: Dict) -> Dict:
        """
        Calcula as necessidades do usuário baseado no estado atual
        """
        needs = {
            'energy_boost': 0,
            'stress_relief': 0,
            'focus_enhancement': 0,
            'relaxation': 0,
            'grounding': 0
        }
        
        # Necessidade de energia
        if state['energy_level'] <= 2:
            needs['energy_boost'] = 0.8
        elif state['energy_level'] == 3:
            needs['energy_boost'] = 0.3
        
        # Necessidade de alívio de stress
        if state['stress_level'] >= 4:
            needs['stress_relief'] = 0.9
        elif state['stress_level'] == 3:
            needs['stress_relief'] = 0.4
        
        # Necessidade de foco
        if state['focus_level'] <= 2:
            needs['focus_enhancement'] = 0.7
        elif state['focus_level'] == 3:
            needs['focus_enhancement'] = 0.3
        
        # Necessidade de relaxamento (baseada no horário)
        if state['time_of_day'] >= 19:  # Noite
            needs['relaxation'] = 0.6
        elif state['time_of_day'] <= 7:  # Manhã cedo
            needs['relaxation'] = 0.3
        
        # Necessidade de grounding (baseada em atividades recentes)
        if 'meeting' in state['recent_activities'] or 'presentation' in state['recent_activities']:
            needs['grounding'] = 0.5
        
        return needs
    
    def _recommend_ritual_types(self, needs: Dict) -> List[RitualType]:
        """
        Recomenda tipos de rituais baseado nas necessidades
        """
        recommendations = []
        
        # Ordenar necessidades por prioridade
        sorted_needs = sorted(needs.items(), key=lambda x: x[1], reverse=True)
        
        for need, intensity in sorted_needs:
            if intensity > 0.5:
                if need == 'energy_boost':
                    recommendations.append(RitualType.ENERGY_BOOST)
                elif need == 'stress_relief':
                    recommendations.append(RitualType.STRESS_RELIEF)
                elif need == 'focus_enhancement':
                    recommendations.append(RitualType.FOCUS)
                elif need == 'relaxation':
                    recommendations.append(RitualType.EVENING)
                elif need == 'grounding':
                    recommendations.append(RitualType.MINDFULNESS)
        
        # Se nenhuma necessidade específica, usar contexto temporal
        if not recommendations:
            hour = datetime.now().hour
            if 6 <= hour <= 10:
                recommendations.append(RitualType.MORNING)
            elif 19 <= hour <= 23:
                recommendations.append(RitualType.EVENING)
            else:
                recommendations.append(RitualType.MINDFULNESS)
        
        return recommendations[:2]  # Máximo 2 tipos
    
    def create_adaptive_ritual(self, user_data: Dict) -> Dict:
        """
        Cria um ritual personalizado baseado no estado do usuário
        """
        analysis = self.analyze_user_state(user_data)
        state = analysis['current_state']
        recommended_types = analysis['recommended_ritual_types']
        
        # Selecionar tipo principal de ritual
        primary_type = recommended_types[0] if recommended_types else RitualType.MINDFULNESS
        
        # Obter componentes base
        base_components = self.ritual_library.get(primary_type, [])
        
        # Adaptar componentes baseado no tempo disponível
        adapted_components = self._adapt_for_time_constraint(
            base_components, state['available_time']
        )
        
        # Personalizar baseado no histórico
        personalized_components = self._personalize_components(
            adapted_components, user_data.get('user_id', 'default')
        )
        
        # Calcular duração total
        total_duration = sum(comp.duration_seconds for comp in personalized_components)
        
        ritual = {
            'id': f"adaptive_ritual_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'name': f"Ritual Personalizado - {primary_type.value.title()}",
            'description': f"Ritual adaptado para suas necessidades atuais",
            'type': primary_type.value,
            'total_duration_seconds': total_duration,
            'total_duration_minutes': round(total_duration / 60, 1),
            'components': [asdict(comp) for comp in personalized_components],
            'adaptation_reasoning': self._generate_adaptation_reasoning(analysis),
            'effectiveness_tracking': {
                'pre_ritual_state': state,
                'expected_outcomes': self._predict_outcomes(primary_type, state)
            }
        }
        
        return ritual
    
    def _adapt_for_time_constraint(self, components: List[RitualStep], 
                                 available_minutes: int) -> List[RitualStep]:
        """
        Adapta os componentes para o tempo disponível
        """
        available_seconds = available_minutes * 60
        total_duration = sum(comp.duration_seconds for comp in components)
        
        if total_duration <= available_seconds:
            return components  # Não precisa adaptar
        
        # Calcular fator de redução
        reduction_factor = available_seconds / total_duration
        
        adapted_components = []
        for comp in components:
            # Criar nova instância com duração reduzida
            new_duration = max(30, int(comp.duration_seconds * reduction_factor))
            
            adapted_comp = RitualStep(
                id=comp.id,
                name=comp.name,
                description=comp.description,
                component=comp.component,
                duration_seconds=new_duration,
                instructions=comp.instructions,
                audio_cue=comp.audio_cue,
                visual_cue=comp.visual_cue,
                breathing_pattern=comp.breathing_pattern
            )
            
            adapted_components.append(adapted_comp)
        
        return adapted_components
    
    def _personalize_components(self, components: List[RitualStep], 
                              user_id: str) -> List[RitualStep]:
        """
        Personaliza componentes baseado no histórico do usuário
        """
        user_prefs = self.user_preferences.get(user_id, {})
        user_effectiveness = self.effectiveness_history.get(user_id, {})
        
        personalized = []
        
        for comp in components:
            # Verificar preferências do usuário
            component_type = comp.component.value
            
            # Ajustar duração baseado na efetividade histórica
            if component_type in user_effectiveness:
                avg_effectiveness = np.mean(user_effectiveness[component_type])
                if avg_effectiveness > 0.7:
                    # Componente efetivo: manter ou aumentar duração
                    duration_multiplier = 1.1
                elif avg_effectiveness < 0.4:
                    # Componente pouco efetivo: reduzir duração
                    duration_multiplier = 0.8
                else:
                    duration_multiplier = 1.0
                
                new_duration = int(comp.duration_seconds * duration_multiplier)
            else:
                new_duration = comp.duration_seconds
            
            # Personalizar instruções baseado em preferências
            instructions = comp.instructions
            if user_prefs.get('detailed_instructions', False):
                instructions = self._add_detailed_instructions(comp)
            
            personalized_comp = RitualStep(
                id=comp.id,
                name=comp.name,
                description=comp.description,
                component=comp.component,
                duration_seconds=new_duration,
                instructions=instructions,
                audio_cue=comp.audio_cue,
                visual_cue=comp.visual_cue,
                breathing_pattern=comp.breathing_pattern
            )
            
            personalized.append(personalized_comp)
        
        return personalized
    
    def _add_detailed_instructions(self, component: RitualStep) -> str:
        """
        Adiciona instruções mais detalhadas para usuários que preferem
        """
        base_instructions = component.instructions
        
        if component.component == RitualComponent.BREATHING:
            if component.breathing_pattern:
                pattern = component.breathing_pattern
                detailed = f"{base_instructions}\n\nPadrão específico:\n"
                detailed += f"• Inspire por {pattern['inhale']} segundos\n"
                detailed += f"• Segure por {pattern['hold']} segundos\n"
                detailed += f"• Expire por {pattern['exhale']} segundos\n"
                detailed += f"• Pause por {pattern['pause']} segundos\n"
                detailed += "Repita este ciclo durante toda a prática."
                return detailed
        
        elif component.component == RitualComponent.MEDITATION:
            detailed = f"{base_instructions}\n\nDicas adicionais:\n"
            detailed += "• Sente-se confortavelmente com a coluna ereta\n"
            detailed += "• Feche os olhos suavemente\n"
            detailed += "• Se a mente divagar, gentilmente retorne o foco\n"
            detailed += "• Não julgue os pensamentos, apenas observe"
            return detailed
        
        elif component.component == RitualComponent.VISUALIZATION:
            detailed = f"{base_instructions}\n\nComo visualizar:\n"
            detailed += "• Use todos os sentidos na visualização\n"
            detailed += "• Torne as imagens vívidas e coloridas\n"
            detailed += "• Inclua sons, cheiros e sensações\n"
            detailed += "• Mantenha as imagens positivas e inspiradoras"
            return detailed
        
        return base_instructions
    
    def _generate_adaptation_reasoning(self, analysis: Dict) -> str:
        """
        Gera explicação sobre por que o ritual foi adaptado desta forma
        """
        state = analysis['current_state']
        needs = analysis['identified_needs']
        
        reasoning = "Este ritual foi personalizado baseado em:\n\n"
        
        # Estado atual
        reasoning += f"• Nível de energia: {state['energy_level']}/5\n"
        reasoning += f"• Nível de stress: {state['stress_level']}/5\n"
        reasoning += f"• Nível de foco: {state['focus_level']}/5\n"
        reasoning += f"• Tempo disponível: {state['available_time']} minutos\n\n"
        
        # Necessidades identificadas
        top_needs = sorted(needs.items(), key=lambda x: x[1], reverse=True)[:2]
        reasoning += "Principais necessidades identificadas:\n"
        for need, intensity in top_needs:
            if intensity > 0.3:
                reasoning += f"• {need.replace('_', ' ').title()}: {intensity:.1f}/1.0\n"
        
        reasoning += "\nO ritual foi estruturado para atender essas necessidades específicas."
        
        return reasoning
    
    def _predict_outcomes(self, ritual_type: RitualType, current_state: Dict) -> Dict:
        """
        Prediz os resultados esperados do ritual
        """
        outcomes = {
            'expected_energy_change': 0,
            'expected_stress_change': 0,
            'expected_focus_change': 0,
            'confidence_level': 0.7
        }
        
        if ritual_type == RitualType.ENERGY_BOOST:
            outcomes['expected_energy_change'] = min(2, 5 - current_state['energy_level'])
            outcomes['expected_stress_change'] = -0.5
            outcomes['confidence_level'] = 0.8
        
        elif ritual_type == RitualType.STRESS_RELIEF:
            outcomes['expected_stress_change'] = -min(2, current_state['stress_level'] - 1)
            outcomes['expected_energy_change'] = 0.5
            outcomes['confidence_level'] = 0.9
        
        elif ritual_type == RitualType.FOCUS:
            outcomes['expected_focus_change'] = min(2, 5 - current_state['focus_level'])
            outcomes['expected_stress_change'] = -0.3
            outcomes['confidence_level'] = 0.8
        
        elif ritual_type in [RitualType.MORNING, RitualType.EVENING]:
            outcomes['expected_energy_change'] = 1 if ritual_type == RitualType.MORNING else -0.5
            outcomes['expected_stress_change'] = -1
            outcomes['expected_focus_change'] = 0.5
            outcomes['confidence_level'] = 0.7
        
        return outcomes
    
    def record_ritual_feedback(self, ritual_id: str, user_id: str, feedback: Dict):
        """
        Registra feedback do usuário sobre a efetividade do ritual
        """
        if user_id not in self.effectiveness_history:
            self.effectiveness_history[user_id] = {}
        
        # Extrair componentes do ritual (seria obtido do banco de dados)
        # Por simplicidade, assumindo que temos acesso aos componentes
        
        effectiveness_score = feedback.get('effectiveness_score', 0.5)  # 0-1
        
        # Registrar efetividade por tipo de componente
        for component_type in ['breathing', 'meditation', 'movement', 'visualization']:
            if component_type not in self.effectiveness_history[user_id]:
                self.effectiveness_history[user_id][component_type] = []
            
            # Adicionar score (em implementação real, seria mais específico)
            self.effectiveness_history[user_id][component_type].append(effectiveness_score)
            
            # Manter apenas os últimos 20 registros
            if len(self.effectiveness_history[user_id][component_type]) > 20:
                self.effectiveness_history[user_id][component_type].pop(0)
        
        # Atualizar preferências do usuário
        self._update_user_preferences(user_id, feedback)
        
        logger.info(f"Feedback registrado para ritual {ritual_id} do usuário {user_id}")
    
    def _update_user_preferences(self, user_id: str, feedback: Dict):
        """
        Atualiza preferências do usuário baseado no feedback
        """
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {
                'preferred_duration': 10,  # minutos
                'detailed_instructions': False,
                'preferred_components': [],
                'avoided_components': []
            }
        
        prefs = self.user_preferences[user_id]
        
        # Atualizar duração preferida
        if 'duration_feedback' in feedback:
            if feedback['duration_feedback'] == 'too_short':
                prefs['preferred_duration'] = min(30, prefs['preferred_duration'] + 2)
            elif feedback['duration_feedback'] == 'too_long':
                prefs['preferred_duration'] = max(5, prefs['preferred_duration'] - 2)
        
        # Atualizar preferência por instruções detalhadas
        if 'instruction_clarity' in feedback:
            if feedback['instruction_clarity'] < 0.5:
                prefs['detailed_instructions'] = True
        
        logger.info(f"Preferências atualizadas para usuário {user_id}")

def main():
    """
    Função principal para demonstração
    """
    engine = AdaptiveRitualEngine()
    
    # Simular dados do usuário
    user_data = {
        'user_id': 'user_123',
        'energy_level': 2,  # Baixa energia
        'stress_level': 4,  # Alto stress
        'focus_level': 2,   # Baixo foco
        'mood': 'tired',
        'time_of_day': 14,  # 14h
        'available_time_minutes': 8,
        'environment': 'office',
        'recent_activities': ['meeting', 'email_processing']
    }
    
    # Criar ritual adaptativo
    ritual = engine.create_adaptive_ritual(user_data)
    
    print("=== RITUAL ADAPTATIVO CRIADO ===")
    print(f"Nome: {ritual['name']}")
    print(f"Duração: {ritual['total_duration_minutes']} minutos")
    print(f"Tipo: {ritual['type']}")
    
    print("\n=== COMPONENTES ===")
    for i, comp in enumerate(ritual['components'], 1):
        duration_min = comp['duration_seconds'] / 60
        print(f"{i}. {comp['name']} ({duration_min:.1f} min)")
        print(f"   {comp['instructions']}")
        print()
    
    print("=== RACIOCÍNIO DA ADAPTAÇÃO ===")
    print(ritual['adaptation_reasoning'])
    
    print("\n=== RESULTADOS ESPERADOS ===")
    outcomes = ritual['effectiveness_tracking']['expected_outcomes']
    print(f"Mudança esperada na energia: {outcomes['expected_energy_change']:+.1f}")
    print(f"Mudança esperada no stress: {outcomes['expected_stress_change']:+.1f}")
    print(f"Mudança esperada no foco: {outcomes['expected_focus_change']:+.1f}")
    print(f"Confiança na predição: {outcomes['confidence_level']:.1%}")
    
    # Simular feedback
    feedback = {
        'effectiveness_score': 0.8,
        'duration_feedback': 'perfect',
        'instruction_clarity': 0.9,
        'overall_satisfaction': 0.85
    }
    
    engine.record_ritual_feedback(ritual['id'], user_data['user_id'], feedback)
    print(f"\nFeedback registrado com sucesso!")

if __name__ == "__main__":
    main()

