"""
Analisador Avançado de Presença - Kairos AI Engine
Utiliza algoritmos de machine learning para análise profunda de padrões de presença
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
from datetime import datetime, timedelta
import json
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedPresenceAnalyzer:
    """
    Analisador avançado que combina múltiplos algoritmos de ML para:
    - Detectar padrões de presença
    - Identificar anomalias comportamentais
    - Prever estados de energia e foco
    - Recomendar pausas e rituais
    """
    
    def __init__(self):
        self.presence_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
        self.energy_clusterer = KMeans(n_clusters=4, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        
        # Estados de presença
        self.presence_states = {
            0: 'Disperso',
            1: 'Focado',
            2: 'Estressado',
            3: 'Equilibrado',
            4: 'Criativo'
        }
        
        # Clusters de energia
        self.energy_clusters = {
            0: 'Energia Baixa',
            1: 'Energia Moderada',
            2: 'Energia Alta',
            3: 'Energia Pico'
        }
    
    def extract_features(self, user_data):
        """
        Extrai features relevantes dos dados do usuário
        """
        features = []
        
        for session in user_data:
            # Features temporais
            hour = session.get('hour', 12)
            day_of_week = session.get('day_of_week', 1)
            
            # Features de atividade
            tasks_completed = session.get('tasks_completed', 0)
            time_focused = session.get('time_focused_minutes', 0)
            interruptions = session.get('interruptions', 0)
            
            # Features fisiológicas (simuladas)
            heart_rate_var = session.get('heart_rate_variability', 50)
            stress_level = session.get('stress_level', 3)
            
            # Features comportamentais
            pause_frequency = session.get('pause_frequency', 0)
            ritual_completion = session.get('ritual_completion_rate', 0.5)
            
            # Features contextuais
            environment_noise = session.get('environment_noise_level', 3)
            social_interactions = session.get('social_interactions', 2)
            
            feature_vector = [
                hour, day_of_week, tasks_completed, time_focused,
                interruptions, heart_rate_var, stress_level,
                pause_frequency, ritual_completion, environment_noise,
                social_interactions
            ]
            
            features.append(feature_vector)
        
        return np.array(features)
    
    def generate_synthetic_training_data(self, n_samples=1000):
        """
        Gera dados sintéticos para treinamento inicial
        """
        np.random.seed(42)
        
        data = []
        labels = []
        
        for _ in range(n_samples):
            # Simular diferentes padrões de presença
            hour = np.random.randint(6, 23)
            day_of_week = np.random.randint(1, 8)
            
            # Padrões baseados no horário
            if 9 <= hour <= 11:  # Manhã produtiva
                base_focus = 0.8
                base_energy = 0.7
            elif 14 <= hour <= 16:  # Tarde focada
                base_focus = 0.6
                base_energy = 0.6
            elif hour >= 20:  # Noite relaxada
                base_focus = 0.3
                base_energy = 0.4
            else:
                base_focus = 0.5
                base_energy = 0.5
            
            # Adicionar variabilidade
            focus_noise = np.random.normal(0, 0.2)
            energy_noise = np.random.normal(0, 0.15)
            
            tasks_completed = max(0, int((base_focus + focus_noise) * 10))
            time_focused = max(0, int((base_focus + focus_noise) * 120))
            interruptions = max(0, int((1 - base_focus) * 8))
            
            heart_rate_var = 40 + (base_energy + energy_noise) * 30
            stress_level = max(1, min(5, int((1 - base_focus) * 5)))
            
            pause_frequency = max(0, int((1 - base_focus) * 6))
            ritual_completion = min(1, max(0, base_focus + np.random.normal(0, 0.1)))
            
            environment_noise = np.random.randint(1, 6)
            social_interactions = np.random.randint(0, 8)
            
            feature_vector = [
                hour, day_of_week, tasks_completed, time_focused,
                interruptions, heart_rate_var, stress_level,
                pause_frequency, ritual_completion, environment_noise,
                social_interactions
            ]
            
            # Determinar label baseado nas features
            if base_focus > 0.7 and stress_level <= 2:
                label = 3  # Equilibrado
            elif base_focus > 0.6 and stress_level <= 3:
                label = 1  # Focado
            elif stress_level >= 4:
                label = 2  # Estressado
            elif base_focus < 0.4:
                label = 0  # Disperso
            else:
                label = 4  # Criativo
            
            data.append(feature_vector)
            labels.append(label)
        
        return np.array(data), np.array(labels)
    
    def train_models(self, user_data=None):
        """
        Treina todos os modelos de ML
        """
        logger.info("Iniciando treinamento dos modelos...")
        
        if user_data is None:
            # Usar dados sintéticos para treinamento inicial
            X, y = self.generate_synthetic_training_data()
        else:
            X = self.extract_features(user_data)
            y = [session.get('presence_state', 1) for session in user_data]
        
        # Normalizar features
        X_scaled = self.scaler.fit_transform(X)
        
        # Treinar classificador de presença
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42
        )
        
        self.presence_classifier.fit(X_train, y_train)
        
        # Avaliar modelo
        y_pred = self.presence_classifier.predict(X_test)
        logger.info("Relatório de classificação:")
        logger.info(classification_report(y_test, y_pred))
        
        # Treinar detector de anomalias
        self.anomaly_detector.fit(X_scaled)
        
        # Treinar clusterer de energia
        self.energy_clusterer.fit(X_scaled)
        
        self.is_trained = True
        logger.info("Treinamento concluído com sucesso!")
    
    def analyze_current_state(self, current_session):
        """
        Analisa o estado atual de presença do usuário
        """
        if not self.is_trained:
            logger.warning("Modelos não treinados. Executando treinamento...")
            self.train_models()
        
        # Extrair features da sessão atual
        features = self.extract_features([current_session])
        features_scaled = self.scaler.transform(features)
        
        # Predições
        presence_state = self.presence_classifier.predict(features_scaled)[0]
        presence_prob = self.presence_classifier.predict_proba(features_scaled)[0]
        
        energy_cluster = self.energy_clusterer.predict(features_scaled)[0]
        
        anomaly_score = self.anomaly_detector.decision_function(features_scaled)[0]
        is_anomaly = self.anomaly_detector.predict(features_scaled)[0] == -1
        
        # Análise detalhada
        analysis = {
            'presence_state': self.presence_states[presence_state],
            'presence_confidence': float(max(presence_prob)),
            'energy_level': self.energy_clusters[energy_cluster],
            'anomaly_score': float(anomaly_score),
            'is_anomalous_behavior': bool(is_anomaly),
            'recommendations': self._generate_recommendations(
                presence_state, energy_cluster, is_anomaly, current_session
            ),
            'insights': self._generate_insights(features_scaled[0], current_session)
        }
        
        return analysis
    
    def _generate_recommendations(self, presence_state, energy_cluster, is_anomaly, session):
        """
        Gera recomendações baseadas no estado atual
        """
        recommendations = []
        
        # Recomendações baseadas no estado de presença
        if presence_state == 0:  # Disperso
            recommendations.extend([
                "Considere fazer uma pausa de 5 minutos para respiração consciente",
                "Tente a técnica Pomodoro para melhorar o foco",
                "Verifique se o ambiente está adequado para concentração"
            ])
        elif presence_state == 2:  # Estressado
            recommendations.extend([
                "Faça uma pausa mais longa (15-20 minutos)",
                "Pratique exercícios de relaxamento muscular",
                "Considere adiar tarefas não urgentes"
            ])
        elif presence_state == 1:  # Focado
            recommendations.extend([
                "Continue no ritmo atual, você está bem focado",
                "Lembre-se de fazer pausas regulares para manter a qualidade"
            ])
        
        # Recomendações baseadas na energia
        if energy_cluster == 0:  # Energia Baixa
            recommendations.extend([
                "Considere uma pausa para lanche saudável",
                "Faça alguns alongamentos ou exercícios leves",
                "Hidrate-se adequadamente"
            ])
        elif energy_cluster == 3:  # Energia Pico
            recommendations.extend([
                "Aproveite este momento para tarefas mais desafiadoras",
                "Mantenha o ritmo, mas não se esqueça das pausas"
            ])
        
        # Recomendações para comportamento anômalo
        if is_anomaly:
            recommendations.append(
                "Padrão incomum detectado. Considere avaliar fatores externos que podem estar influenciando seu desempenho"
            )
        
        return recommendations
    
    def _generate_insights(self, features, session):
        """
        Gera insights baseados nas features extraídas
        """
        insights = []
        
        hour = features[0]
        tasks_completed = features[2]
        time_focused = features[3]
        stress_level = features[6]
        
        # Insights temporais
        if 9 <= hour <= 11:
            insights.append("Você está em seu horário de pico matinal")
        elif 14 <= hour <= 16:
            insights.append("Período da tarde - bom para tarefas de revisão")
        elif hour >= 20:
            insights.append("Período noturno - considere atividades mais leves")
        
        # Insights de produtividade
        if tasks_completed > 7:
            insights.append("Excelente produtividade hoje!")
        elif tasks_completed < 3:
            insights.append("Produtividade abaixo do esperado - verifique possíveis distrações")
        
        # Insights de foco
        if time_focused > 90:
            insights.append("Ótima capacidade de foco sustentado")
        elif time_focused < 30:
            insights.append("Dificuldade de manter foco - considere técnicas de concentração")
        
        # Insights de stress
        if stress_level >= 4:
            insights.append("Nível de stress elevado - priorize técnicas de relaxamento")
        elif stress_level <= 2:
            insights.append("Nível de stress baixo - bom estado para aprendizado")
        
        return insights
    
    def predict_optimal_schedule(self, user_preferences, upcoming_tasks):
        """
        Prediz o cronograma ótimo baseado nos padrões do usuário
        """
        if not self.is_trained:
            self.train_models()
        
        optimal_schedule = []
        
        for task in upcoming_tasks:
            best_time = None
            best_score = -1
            
            # Testar diferentes horários
            for hour in range(6, 23):
                # Simular sessão neste horário
                test_session = {
                    'hour': hour,
                    'day_of_week': datetime.now().weekday() + 1,
                    'tasks_completed': 3,
                    'time_focused_minutes': 60,
                    'interruptions': 2,
                    'heart_rate_variability': 50,
                    'stress_level': 2,
                    'pause_frequency': 1,
                    'ritual_completion_rate': 0.7,
                    'environment_noise_level': 2,
                    'social_interactions': 3
                }
                
                features = self.extract_features([test_session])
                features_scaled = self.scaler.transform(features)
                
                # Calcular score de adequação
                presence_prob = self.presence_classifier.predict_proba(features_scaled)[0]
                focus_score = presence_prob[1] + presence_prob[3]  # Focado + Equilibrado
                
                if focus_score > best_score:
                    best_score = focus_score
                    best_time = hour
            
            optimal_schedule.append({
                'task': task,
                'optimal_time': best_time,
                'confidence_score': best_score,
                'reasoning': f"Melhor horário baseado em padrões de foco (score: {best_score:.2f})"
            })
        
        return optimal_schedule
    
    def save_models(self, filepath_prefix="kairos_ai_models"):
        """
        Salva os modelos treinados
        """
        if not self.is_trained:
            logger.warning("Modelos não treinados. Nada para salvar.")
            return
        
        joblib.dump(self.presence_classifier, f"{filepath_prefix}_presence_classifier.pkl")
        joblib.dump(self.anomaly_detector, f"{filepath_prefix}_anomaly_detector.pkl")
        joblib.dump(self.energy_clusterer, f"{filepath_prefix}_energy_clusterer.pkl")
        joblib.dump(self.scaler, f"{filepath_prefix}_scaler.pkl")
        
        logger.info(f"Modelos salvos com prefixo: {filepath_prefix}")
    
    def load_models(self, filepath_prefix="kairos_ai_models"):
        """
        Carrega modelos previamente treinados
        """
        try:
            self.presence_classifier = joblib.load(f"{filepath_prefix}_presence_classifier.pkl")
            self.anomaly_detector = joblib.load(f"{filepath_prefix}_anomaly_detector.pkl")
            self.energy_clusterer = joblib.load(f"{filepath_prefix}_energy_clusterer.pkl")
            self.scaler = joblib.load(f"{filepath_prefix}_scaler.pkl")
            
            self.is_trained = True
            logger.info("Modelos carregados com sucesso!")
        except FileNotFoundError:
            logger.warning("Arquivos de modelo não encontrados. Execute o treinamento primeiro.")

def main():
    """
    Função principal para demonstração
    """
    analyzer = AdvancedPresenceAnalyzer()
    
    # Treinar modelos
    analyzer.train_models()
    
    # Simular análise de sessão atual
    current_session = {
        'hour': 10,
        'day_of_week': 2,
        'tasks_completed': 5,
        'time_focused_minutes': 75,
        'interruptions': 2,
        'heart_rate_variability': 55,
        'stress_level': 2,
        'pause_frequency': 1,
        'ritual_completion_rate': 0.8,
        'environment_noise_level': 2,
        'social_interactions': 3
    }
    
    analysis = analyzer.analyze_current_state(current_session)
    
    print("=== ANÁLISE DE PRESENÇA AVANÇADA ===")
    print(f"Estado de Presença: {analysis['presence_state']}")
    print(f"Confiança: {analysis['presence_confidence']:.2f}")
    print(f"Nível de Energia: {analysis['energy_level']}")
    print(f"Comportamento Anômalo: {analysis['is_anomalous_behavior']}")
    
    print("\n=== RECOMENDAÇÕES ===")
    for rec in analysis['recommendations']:
        print(f"• {rec}")
    
    print("\n=== INSIGHTS ===")
    for insight in analysis['insights']:
        print(f"• {insight}")
    
    # Demonstrar predição de cronograma
    upcoming_tasks = ["Reunião estratégica", "Análise de dados", "Escrita criativa"]
    schedule = analyzer.predict_optimal_schedule({}, upcoming_tasks)
    
    print("\n=== CRONOGRAMA OTIMIZADO ===")
    for item in schedule:
        print(f"{item['task']}: {item['optimal_time']}h (Score: {item['confidence_score']:.2f})")

if __name__ == "__main__":
    main()

