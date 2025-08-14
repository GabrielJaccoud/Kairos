# ai-engine/recommendation-engine.py
import json
from typing import List, Dict, Any
from datetime import datetime, timedelta

class RecommendationEngine:
    def __init__(self):
        self.recommendation_rules = {
            "low_energy_morning": {
                "condition": lambda profile: profile.get("energy_pattern") == "low_morning",
                "suggestions": [
                    "Comece o dia com um ritual de 5 minutos de respiração consciente.",
                    "Agende tarefas de baixa energia para a primeira hora da manhã."
                ]
            },
            "high_stress_context": {
                "condition": lambda profile: profile.get("stress_contexts") and "work" in profile["stress_contexts"],
                "suggestions": [
                    "Inclua pausas de 3 minutos a cada hora durante o trabalho.",
                    "Experimente a técnica Pomodoro para gerenciar o tempo de forma mais eficaz."
                ]
            },
            "inconsistent_reflection": {
                "condition": lambda profile: profile.get("reflection_consistency") < 0.7,
                "suggestions": [
                    "Tente fazer sua reflexão diária sempre no mesmo horário, antes de dormir.",
                    "Use os prompts de gratidão e aprendizado para facilitar a reflexão."
                ]
            },
            "relationship_neglect": {
                "condition": lambda profile: profile.get("last_social_interaction_days") > 7,
                "suggestions": [
                    "Envie uma mensagem para um amigo ou familiar hoje.",
                    "Agende um café virtual com alguém que você não vê há um tempo."
                ]
            }
        }

    def generate_recommendations(self, user_profile: Dict[str, Any], 
                                 recent_activities: List[Dict[str, Any]]) -> List[str]:
        """Gera recomendações personalizadas para o usuário."""
        recommendations = []
        
        # Recomendações baseadas em regras predefinidas
        for rule_name, rule_data in self.recommendation_rules.items():
            if rule_data["condition"](user_profile):
                recommendations.extend(rule_data["suggestions"])
        
        # Recomendações baseadas em análise de atividades recentes
        activity_based_recs = self._analyze_recent_activities(recent_activities)
        recommendations.extend(activity_based_recs)
        
        # Remover duplicatas e limitar a quantidade
        unique_recommendations = list(dict.fromkeys(recommendations))[:5] # Limita a 5 recomendações
        
        return unique_recommendations

    def _analyze_recent_activities(self, activities: List[Dict[str, Any]]) -> List[str]:
        """Analisa atividades recentes para gerar recomendações contextuais."""
        recs = []
        
        # Exemplo: Se muitas tarefas urgentes foram concluídas, sugerir descanso
        urgent_completed = [a for a in activities 
                            if a.get("type") == "task" and a.get("urgency_level") == "high" and a.get("status") == "completed"]
        if len(urgent_completed) > 3:
            recs.append("Você concluiu muitas tarefas urgentes recentemente. Considere uma pausa para recarregar as energias.")
        
        # Exemplo: Se poucos rituais foram executados, sugerir um
        ritual_executions = [a for a in activities if a.get("type") == "ritual_execution"]
        if len(ritual_executions) < 1 and datetime.now().hour > 12: # Se nenhum ritual hoje e já passou do meio-dia
            recs.append("Que tal um ritual rápido para reequilibrar o dia? Experimente a Pausa Consciente.")
            
        return recs

    def get_daily_focus_suggestion(self, user_profile: Dict[str, Any], 
                                   upcoming_tasks: List[Dict[str, Any]]) -> str:
        """Sugere um foco diário baseado no perfil e nas tarefas futuras."""
        focus_areas = []
        
        # Foco baseado em tarefas de alta prioridade
        high_priority_tasks = [t for t in upcoming_tasks if t.get("ai_priority_score", 0) > 0.7]
        if high_priority_tasks:
            focus_areas.append("Priorizar tarefas de alta importância e urgência.")
        
        # Foco baseado em padrões de energia
        if user_profile.get("energy_pattern") == "morning_person":
            focus_areas.append("Aproveitar o pico de energia da manhã para atividades complexas.")
        
        # Foco em bem-estar se o nível de estresse for alto
        if user_profile.get("current_stress_level", 0) > 0.6:
            focus_areas.append("Focar em autocuidado e momentos de presença para reduzir o estresse.")
            
        if focus_areas:
            return "Seu foco para hoje: " + ", ".join(focus_areas) + "."
        else:
            return "Seu foco para hoje: Mantenha a presença e o equilíbrio em todas as suas atividades."

    def suggest_relationship_nurturing(self, user_profile: Dict[str, Any]) -> List[str]:
        """Sugere ações para nutrir relacionamentos."""
        suggestions = []
        
        # Exemplo: Se o usuário não interagiu com contatos importantes recentemente
        if user_profile.get("important_contacts_last_interaction"):
            for contact, last_interaction_date in user_profile["important_contacts_last_interaction"].items():
                if (datetime.now() - datetime.fromisoformat(last_interaction_date)).days > 14:
                    suggestions.append(f"Entre em contato com {contact}. Já faz um tempo desde a última interação.")
        
        if not suggestions:
            suggestions.append("Conecte-se com alguém que te inspira hoje.")
            
        return suggestions

def generate_recommendations_api(user_profile: Dict[str, Any], 
                                 recent_activities: List[Dict[str, Any]]) -> List[str]:
    """Função de API para geração de recomendações"""
    engine = RecommendationEngine()
    return engine.generate_recommendations(user_profile, recent_activities)

if __name__ == "__main__":
    # Exemplo de uso
    sample_user_profile = {
        "energy_pattern": "morning_person",
        "stress_contexts": ["work"],
        "reflection_consistency": 0.5,
        "last_social_interaction_days": 10,
        "current_stress_level": 0.7,
        "important_contacts_last_interaction": {
            "Maria": "2024-07-01T10:00:00Z",
            "João": "2024-08-05T15:30:00Z"
        }
    }
    
    sample_recent_activities = [
        {"type": "task", "title": "Relatório Mensal", "urgency_level": "high", "status": "completed"},
        {"type": "task", "title": "Apresentação Cliente", "urgency_level": "high", "status": "completed"},
        {"type": "ritual_execution", "ritual_name": "Pausa Consciente"}
    ]
    
    engine = RecommendationEngine()
    recommendations = engine.generate_recommendations(sample_user_profile, sample_recent_activities)
    daily_focus = engine.get_daily_focus_suggestion(sample_user_profile, [])
    relationship_nurturing = engine.suggest_relationship_nurturing(sample_user_profile)
    
    print("=== RECOMENDAÇÕES ===")
    for rec in recommendations:
        print(f"- {rec}")
    
    print(f"\n{daily_focus}")
    
    print("\n=== NUTRIÇÃO DE RELACIONAMENTOS ===")
    for rel_rec in relationship_nurturing:
        print(f"- {rel_rec}")


