# ai-engine/presence-analyzer.py
import json
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple
from collections import defaultdict

class PresenceAnalyzer:
    def __init__(self):
        self.mindfulness_keywords = [
            'respiração', 'meditação', 'presente', 'consciente', 'atenção',
            'foco', 'calma', 'paz', 'gratidão', 'reflexão'
        ]
        self.stress_indicators = [
            'ansioso', 'estressado', 'pressa', 'urgente', 'preocupado',
            'tenso', 'cansado', 'sobrecarregado', 'frustrado'
        ]
    
    def analyze_presence_patterns(self, presence_logs: List[Dict]) -> Dict[str, Any]:
        """Analisa padrões de presença ao longo do tempo"""
        if not presence_logs:
            return {'message': 'Dados insuficientes para análise de presença'}
        
        # Organizar dados por período
        daily_patterns = self._analyze_daily_patterns(presence_logs)
        weekly_patterns = self._analyze_weekly_patterns(presence_logs)
        contextual_patterns = self._analyze_contextual_patterns(presence_logs)
        mood_patterns = self._analyze_mood_patterns(presence_logs)
        
        # Calcular métricas gerais
        overall_metrics = self._calculate_overall_metrics(presence_logs)
        
        # Gerar insights e recomendações
        insights = self._generate_presence_insights(daily_patterns, contextual_patterns, mood_patterns)
        recommendations = self._generate_presence_recommendations(overall_metrics, daily_patterns)
        
        return {
            'overall_metrics': overall_metrics,
            'daily_patterns': daily_patterns,
            'weekly_patterns': weekly_patterns,
            'contextual_patterns': contextual_patterns,
            'mood_patterns': mood_patterns,
            'insights': insights,
            'recommendations': recommendations,
            'analysis_date': datetime.now().isoformat()
        }
    
    def _analyze_daily_patterns(self, logs: List[Dict]) -> Dict[str, Any]:
        """Analisa padrões diários de presença"""
        hourly_scores = defaultdict(list)
        
        for log in logs:
            if log.get('logged_at') and log.get('presence_score'):
                try:
                    log_time = datetime.fromisoformat(log['logged_at'].replace('Z', '+00:00'))
                    hour = log_time.hour
                    hourly_scores[hour].append(log['presence_score'])
                except:
                    continue
        
        # Calcular médias por hora
        hourly_averages = {
            hour: {
                'average_score': np.mean(scores),
                'count': len(scores),
                'std_dev': np.std(scores)
            }
            for hour, scores in hourly_scores.items()
        }
        
        # Identificar picos e vales
        if hourly_averages:
            best_hours = sorted(hourly_averages.items(), 
                              key=lambda x: x[1]['average_score'], reverse=True)[:3]
            worst_hours = sorted(hourly_averages.items(), 
                               key=lambda x: x[1]['average_score'])[:3]
        else:
            best_hours = worst_hours = []
        
        return {
            'hourly_averages': hourly_averages,
            'peak_presence_hours': [{'hour': h, 'score': data['average_score']} 
                                  for h, data in best_hours],
            'low_presence_hours': [{'hour': h, 'score': data['average_score']} 
                                 for h, data in worst_hours],
            'total_daily_logs': len(logs)
        }
    
    def _analyze_weekly_patterns(self, logs: List[Dict]) -> Dict[str, Any]:
        """Analisa padrões semanais de presença"""
        weekday_scores = defaultdict(list)
        
        for log in logs:
            if log.get('logged_at') and log.get('presence_score'):
                try:
                    log_time = datetime.fromisoformat(log['logged_at'].replace('Z', '+00:00'))
                    weekday = log_time.weekday()  # 0=Monday, 6=Sunday
                    weekday_scores[weekday].append(log['presence_score'])
                except:
                    continue
        
        weekday_names = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        
        weekly_averages = {}
        for weekday, scores in weekday_scores.items():
            if scores:
                weekly_averages[weekday_names[weekday]] = {
                    'average_score': np.mean(scores),
                    'count': len(scores),
                    'trend': self._calculate_trend(scores)
                }
        
        return {
            'weekly_averages': weekly_averages,
            'best_weekday': max(weekly_averages.items(), 
                              key=lambda x: x[1]['average_score'])[0] if weekly_averages else None,
            'challenging_weekday': min(weekly_averages.items(), 
                                     key=lambda x: x[1]['average_score'])[0] if weekly_averages else None
        }
    
    def _analyze_contextual_patterns(self, logs: List[Dict]) -> Dict[str, Any]:
        """Analisa presença por contexto (trabalho, casa, lazer, etc.)"""
        context_scores = defaultdict(list)
        
        for log in logs:
            context = log.get('context', 'unknown')
            score = log.get('presence_score')
            if score is not None:
                context_scores[context].append(score)
        
        context_analysis = {}
        for context, scores in context_scores.items():
            if scores:
                context_analysis[context] = {
                    'average_score': np.mean(scores),
                    'count': len(scores),
                    'consistency': 1.0 - (np.std(scores) / 10.0),  # Normalizado para 0-1
                    'improvement_trend': self._calculate_trend(scores)
                }
        
        # Identificar melhor e pior contexto
        if context_analysis:
            best_context = max(context_analysis.items(), key=lambda x: x[1]['average_score'])
            worst_context = min(context_analysis.items(), key=lambda x: x[1]['average_score'])
        else:
            best_context = worst_context = None
        
        return {
            'context_analysis': context_analysis,
            'most_present_context': best_context[0] if best_context else None,
            'least_present_context': worst_context[0] if worst_context else None,
            'context_recommendations': self._generate_context_recommendations(context_analysis)
        }
    
    def _analyze_mood_patterns(self, logs: List[Dict]) -> Dict[str, Any]:
        """Analisa correlação entre humor e presença"""
        mood_presence = defaultdict(list)
        
        for log in logs:
            mood = log.get('mood')
            score = log.get('presence_score')
            if mood and score is not None:
                mood_presence[mood].append(score)
        
        mood_analysis = {}
        for mood, scores in mood_presence.items():
            if scores:
                mood_analysis[mood] = {
                    'average_presence': np.mean(scores),
                    'count': len(scores),
                    'presence_range': {
                        'min': min(scores),
                        'max': max(scores)
                    }
                }
        
        # Identificar humores mais e menos conducentes à presença
        if mood_analysis:
            best_mood = max(mood_analysis.items(), key=lambda x: x[1]['average_presence'])
            challenging_mood = min(mood_analysis.items(), key=lambda x: x[1]['average_presence'])
        else:
            best_mood = challenging_mood = None
        
        return {
            'mood_analysis': mood_analysis,
            'most_present_mood': best_mood[0] if best_mood else None,
            'challenging_mood': challenging_mood[0] if challenging_mood else None,
            'mood_presence_correlation': self._calculate_mood_correlation(mood_analysis)
        }
    
    def _calculate_overall_metrics(self, logs: List[Dict]) -> Dict[str, Any]:
        """Calcula métricas gerais de presença"""
        if not logs:
            return {}
        
        scores = [log['presence_score'] for log in logs if log.get('presence_score') is not None]
        
        if not scores:
            return {}
        
        # Métricas básicas
        avg_presence = np.mean(scores)
        consistency = 1.0 - (np.std(scores) / 10.0)  # Normalizado
        improvement_trend = self._calculate_trend(scores)
        
        # Distribuição de scores
        high_presence_count = len([s for s in scores if s >= 8])
        medium_presence_count = len([s for s in scores if 5 <= s < 8])
        low_presence_count = len([s for s in scores if s < 5])
        
        # Frequência de logging (logs por dia)
        if len(logs) > 1:
            first_log = datetime.fromisoformat(logs[0]['logged_at'].replace('Z', '+00:00'))
            last_log = datetime.fromisoformat(logs[-1]['logged_at'].replace('Z', '+00:00'))
            days_span = (last_log - first_log).days + 1
            logs_per_day = len(logs) / days_span
        else:
            logs_per_day = 1
        
        return {
            'average_presence': round(avg_presence, 2),
            'consistency_score': round(consistency, 2),
            'improvement_trend': improvement_trend,
            'total_logs': len(logs),
            'logs_per_day': round(logs_per_day, 2),
            'presence_distribution': {
                'high': high_presence_count,
                'medium': medium_presence_count,
                'low': low_presence_count
            },
            'presence_percentiles': {
                '25th': np.percentile(scores, 25),
                '50th': np.percentile(scores, 50),
                '75th': np.percentile(scores, 75)
            }
        }
    
    def _calculate_trend(self, scores: List[float]) -> str:
        """Calcula tendência de melhoria/piora"""
        if len(scores) < 3:
            return 'insufficient_data'
        
        # Usar regressão linear simples
        x = np.arange(len(scores))
        slope = np.polyfit(x, scores, 1)[0]
        
        if slope > 0.1:
            return 'improving'
        elif slope < -0.1:
            return 'declining'
        else:
            return 'stable'
    
    def _calculate_mood_correlation(self, mood_analysis: Dict) -> float:
        """Calcula correlação geral entre humor e presença"""
        if len(mood_analysis) < 2:
            return 0.0
        
        # Simplificado: variação entre o melhor e pior humor
        scores = [data['average_presence'] for data in mood_analysis.values()]
        return (max(scores) - min(scores)) / 10.0  # Normalizado
    
    def _generate_presence_insights(self, daily_patterns: Dict, contextual_patterns: Dict, 
                                  mood_patterns: Dict) -> List[str]:
        """Gera insights baseados nos padrões identificados"""
        insights = []
        
        # Insights sobre padrões diários
        if daily_patterns.get('peak_presence_hours'):
            best_hours = [str(h['hour']) for h in daily_patterns['peak_presence_hours'][:2]]
            insights.append(f"Sua presença é mais elevada entre {' e '.join(best_hours)}h. "
                          f"Aproveite esses momentos para atividades importantes.")
        
        if daily_patterns.get('low_presence_hours'):
            worst_hours = [str(h['hour']) for h in daily_patterns['low_presence_hours'][:2]]
            insights.append(f"Você tende a ter menor presença entre {' e '.join(worst_hours)}h. "
                          f"Considere pausas conscientes nesses horários.")
        
        # Insights sobre contextos
        best_context = contextual_patterns.get('most_present_context')
        worst_context = contextual_patterns.get('least_present_context')
        
        if best_context:
            insights.append(f"Você demonstra maior presença no contexto '{best_context}'. "
                          f"Tente aplicar as mesmas práticas em outros contextos.")
        
        if worst_context and worst_context != best_context:
            insights.append(f"O contexto '{worst_context}' apresenta desafios para sua presença. "
                          f"Experimente técnicas específicas para esse ambiente.")
        
        # Insights sobre humor
        best_mood = mood_patterns.get('most_present_mood')
        if best_mood:
            insights.append(f"Quando você se sente '{best_mood}', sua presença é naturalmente elevada. "
                          f"Cultive esse estado emocional.")
        
        return insights
    
    def _generate_presence_recommendations(self, metrics: Dict, daily_patterns: Dict) -> List[str]:
        """Gera recomendações personalizadas para melhorar a presença"""
        recommendations = []
        
        avg_presence = metrics.get('average_presence', 0)
        consistency = metrics.get('consistency_score', 0)
        logs_per_day = metrics.get('logs_per_day', 0)
        
        # Recomendações baseadas na presença média
        if avg_presence < 5:
            recommendations.append("Sua presença média está baixa. Comece com 3 pausas conscientes "
                                 "de 2 minutos por dia: manhã, tarde e noite.")
        elif avg_presence < 7:
            recommendations.append("Você está no caminho certo! Tente aumentar a frequência de "
                                 "momentos de presença para 5-6 vezes por dia.")
        else:
            recommendations.append("Excelente nível de presença! Foque agora na consistência e "
                                 "em aprofundar a qualidade dos momentos conscientes.")
        
        # Recomendações baseadas na consistência
        if consistency < 0.6:
            recommendations.append("Sua presença varia bastante. Estabeleça rituais fixos: "
                                 "respiração matinal e reflexão noturna para criar mais estabilidade.")
        
        # Recomendações baseadas na frequência de logging
        if logs_per_day < 2:
            recommendations.append("Registre sua presença mais frequentemente (3-4 vezes/dia) "
                                 "para desenvolver maior consciência dos seus padrões.")
        elif logs_per_day > 10:
            recommendations.append("Você está muito atento aos registros! Foque na qualidade "
                                 "dos momentos de presença em vez da quantidade de registros.")
        
        # Recomendações baseadas nos horários
        if daily_patterns.get('low_presence_hours'):
            worst_hour = daily_patterns['low_presence_hours'][0]['hour']
            recommendations.append(f"Às {worst_hour}h você tende a ter menor presença. "
                                 f"Configure um lembrete para uma pausa consciente nesse horário.")
        
        return recommendations
    
    def _generate_context_recommendations(self, context_analysis: Dict) -> List[str]:
        """Gera recomendações específicas por contexto"""
        recommendations = []
        
        for context, data in context_analysis.items():
            avg_score = data['average_presence']
            consistency = data['consistency']
            
            if avg_score < 5:
                recommendations.append(f"{context.title()}: Implemente âncoras de presença "
                                     f"(respiração profunda ao entrar no ambiente).")
            elif consistency < 0.6:
                recommendations.append(f"{context.title()}: Crie rituais específicos para "
                                     f"manter presença consistente neste contexto.")
        
        return recommendations

    def predict_presence_challenges(self, logs: List[Dict], days_ahead: int = 7) -> Dict[str, Any]:
        """Prediz possíveis desafios de presença nos próximos dias"""
        if not logs:
            return {'message': 'Dados insuficientes para predição'}
        
        # Analisar padrões recentes
        recent_logs = [log for log in logs 
                      if datetime.fromisoformat(log['logged_at'].replace('Z', '+00:00')) 
                      > datetime.now() - timedelta(days=14)]
        
        if not recent_logs:
            return {'message': 'Dados recentes insuficientes'}
        
        # Identificar tendências
        recent_scores = [log['presence_score'] for log in recent_logs 
                        if log.get('presence_score') is not None]
        
        trend = self._calculate_trend(recent_scores)
        avg_recent = np.mean(recent_scores) if recent_scores else 0
        
        # Gerar predições
        predictions = []
        
        if trend == 'declining':
            predictions.append({
                'type': 'warning',
                'message': 'Tendência de declínio na presença detectada',
                'recommendation': 'Intensifique práticas de mindfulness nos próximos dias',
                'confidence': 0.7
            })
        
        if avg_recent < 5:
            predictions.append({
                'type': 'alert',
                'message': 'Presença média baixa nas últimas duas semanas',
                'recommendation': 'Considere reduzir compromissos e focar em autocuidado',
                'confidence': 0.8
            })
        
        # Predições baseadas em padrões semanais
        weekly_patterns = self._analyze_weekly_patterns(recent_logs)
        challenging_day = weekly_patterns.get('challenging_weekday')
        
        if challenging_day:
            predictions.append({
                'type': 'insight',
                'message': f'{challenging_day} tende a ser desafiador para sua presença',
                'recommendation': f'Prepare rituais extras para {challenging_day}',
                'confidence': 0.6
            })
        
        return {
            'predictions': predictions,
            'trend_analysis': {
                'current_trend': trend,
                'recent_average': round(avg_recent, 2),
                'data_points': len(recent_scores)
            },
            'prediction_date': datetime.now().isoformat()
        }

def analyze_presence_api(presence_logs: List[Dict]) -> Dict[str, Any]:
    """Função de API para análise de presença"""
    analyzer = PresenceAnalyzer()
    return analyzer.analyze_presence_patterns(presence_logs)

if __name__ == "__main__":
    # Exemplo de uso
    sample_logs = [
        {
            'logged_at': '2024-01-15T09:30:00Z',
            'presence_score': 8,
            'mood': 'calmo',
            'context': 'trabalho',
            'activity': 'reunião matinal'
        },
        {
            'logged_at': '2024-01-15T14:15:00Z',
            'presence_score': 6,
            'mood': 'focado',
            'context': 'trabalho',
            'activity': 'desenvolvimento'
        },
        {
            'logged_at': '2024-01-15T18:45:00Z',
            'presence_score': 9,
            'mood': 'relaxado',
            'context': 'casa',
            'activity': 'meditação'
        }
    ]
    
    analyzer = PresenceAnalyzer()
    analysis = analyzer.analyze_presence_patterns(sample_logs)
    
    print("=== ANÁLISE DE PRESENÇA ===")
    print(json.dumps(analysis, indent=2, ensure_ascii=False))

