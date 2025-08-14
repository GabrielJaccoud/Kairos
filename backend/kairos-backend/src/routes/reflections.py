from flask import Blueprint, request, jsonify
from datetime import datetime, date, timedelta
from src.models.user import db
from src.models.reflection import DailyReflection, PresenceLog

reflections_bp = Blueprint('reflections', __name__)

@reflections_bp.route('/reflections/daily', methods=['GET'])
def get_daily_reflection():
    """Obter reflexão diária (hoje ou data específica)"""
    try:
        user_id = request.args.get('user_id', 1, type=int)
        reflection_date = request.args.get('date')
        
        if reflection_date:
            target_date = datetime.strptime(reflection_date, '%Y-%m-%d').date()
        else:
            target_date = date.today()
        
        reflection = DailyReflection.query.filter_by(
            user_id=user_id, 
            reflection_date=target_date
        ).first()
        
        if reflection:
            return jsonify({
                'success': True,
                'reflection': reflection.to_dict()
            })
        else:
            return jsonify({
                'success': True,
                'reflection': None,
                'message': 'Nenhuma reflexão encontrada para esta data'
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@reflections_bp.route('/reflections/daily', methods=['POST'])
def create_or_update_daily_reflection():
    """Criar ou atualizar reflexão diária"""
    try:
        data = request.get_json()
        user_id = data.get('user_id', 1)
        reflection_date = date.today()
        
        if data.get('reflection_date'):
            reflection_date = datetime.strptime(data['reflection_date'], '%Y-%m-%d').date()
        
        # Buscar reflexão existente ou criar nova
        reflection = DailyReflection.query.filter_by(
            user_id=user_id,
            reflection_date=reflection_date
        ).first()
        
        if not reflection:
            reflection = DailyReflection(
                user_id=user_id,
                reflection_date=reflection_date
            )
            db.session.add(reflection)
        
        # Atualizar campos
        if 'gratitude' in data:
            reflection.gratitude = data['gratitude']
        if 'forgiveness' in data:
            reflection.forgiveness = data['forgiveness']
        if 'learning' in data:
            reflection.learning = data['learning']
        if 'overcoming' in data:
            reflection.overcoming = data['overcoming']
        if 'day_rating' in data:
            reflection.day_rating = data['day_rating']
        if 'presence_level' in data:
            reflection.presence_level = data['presence_level']
        if 'energy_level' in data:
            reflection.energy_level = data['energy_level']
        
        # Gerar insights da IA (simulação)
        reflection.ai_insights = generate_ai_insights(reflection)
        reflection.ai_suggestions = generate_ai_suggestions(reflection)
        
        reflection.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'reflection': reflection.to_dict(),
            'message': 'Reflexão salva com sucesso'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@reflections_bp.route('/reflections/presence-log', methods=['POST'])
def log_presence_moment():
    """Registrar um momento de presença"""
    try:
        data = request.get_json()
        
        presence_log = PresenceLog(
            user_id=data.get('user_id', 1),
            activity=data.get('activity', ''),
            presence_score=data.get('presence_score', 5),
            mood=data.get('mood', ''),
            context=data.get('context', ''),
            notes=data.get('notes', '')
        )
        
        db.session.add(presence_log)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'presence_log': presence_log.to_dict(),
            'message': 'Momento de presença registrado'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@reflections_bp.route('/reflections/presence-stats', methods=['GET'])
def get_presence_stats():
    """Obter estatísticas de presença"""
    try:
        user_id = request.args.get('user_id', 1, type=int)
        days = request.args.get('days', 7, type=int)
        
        # Buscar logs de presença dos últimos N dias
        start_date = datetime.utcnow() - timedelta(days=days)
        presence_logs = PresenceLog.query.filter(
            PresenceLog.user_id == user_id,
            PresenceLog.logged_at >= start_date
        ).all()
        
        if not presence_logs:
            return jsonify({
                'success': True,
                'stats': {
                    'average_presence': 0,
                    'total_logs': 0,
                    'mood_distribution': {},
                    'context_distribution': {},
                    'daily_averages': []
                }
            })
        
        # Calcular estatísticas
        total_logs = len(presence_logs)
        average_presence = sum(log.presence_score for log in presence_logs) / total_logs
        
        # Distribuição de humor
        mood_counts = {}
        for log in presence_logs:
            if log.mood:
                mood_counts[log.mood] = mood_counts.get(log.mood, 0) + 1
        
        # Distribuição de contexto
        context_counts = {}
        for log in presence_logs:
            if log.context:
                context_counts[log.context] = context_counts.get(log.context, 0) + 1
        
        # Médias diárias
        daily_scores = {}
        for log in presence_logs:
            day_key = log.logged_at.date().isoformat()
            if day_key not in daily_scores:
                daily_scores[day_key] = []
            daily_scores[day_key].append(log.presence_score)
        
        daily_averages = [
            {
                'date': day,
                'average_presence': sum(scores) / len(scores)
            }
            for day, scores in daily_scores.items()
        ]
        
        return jsonify({
            'success': True,
            'stats': {
                'average_presence': round(average_presence, 2),
                'total_logs': total_logs,
                'mood_distribution': mood_counts,
                'context_distribution': context_counts,
                'daily_averages': sorted(daily_averages, key=lambda x: x['date'])
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@reflections_bp.route('/reflections/weekly-report', methods=['GET'])
def get_weekly_report():
    """Obter relatório semanal de presença"""
    try:
        user_id = request.args.get('user_id', 1, type=int)
        
        # Buscar reflexões da última semana
        week_ago = date.today() - timedelta(days=7)
        reflections = DailyReflection.query.filter(
            DailyReflection.user_id == user_id,
            DailyReflection.reflection_date >= week_ago
        ).all()
        
        if not reflections:
            return jsonify({
                'success': True,
                'report': {
                    'total_reflections': 0,
                    'average_day_rating': 0,
                    'average_presence_level': 0,
                    'average_energy_level': 0,
                    'consistency_score': 0,
                    'insights': []
                }
            })
        
        total_reflections = len(reflections)
        avg_day_rating = sum(r.day_rating for r in reflections if r.day_rating) / total_reflections
        avg_presence = sum(r.presence_level for r in reflections if r.presence_level) / total_reflections
        avg_energy = sum(r.energy_level for r in reflections if r.energy_level) / total_reflections
        consistency_score = (total_reflections / 7) * 100
        
        # Coletar insights únicos
        all_insights = []
        for reflection in reflections:
            if reflection.ai_insights:
                all_insights.extend(reflection.ai_insights.split('\n'))
        
        unique_insights = list(set(filter(None, all_insights)))[:5]  # Top 5 insights únicos
        
        return jsonify({
            'success': True,
            'report': {
                'total_reflections': total_reflections,
                'average_day_rating': round(avg_day_rating, 2),
                'average_presence_level': round(avg_presence, 2),
                'average_energy_level': round(avg_energy, 2),
                'consistency_score': round(consistency_score, 1),
                'insights': unique_insights,
                'reflections': [r.to_dict() for r in reflections]
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def generate_ai_insights(reflection):
    """Gerar insights da IA baseados na reflexão (simulação)"""
    insights = []
    
    if reflection.day_rating and reflection.day_rating >= 8:
        insights.append("Você teve um dia excelente! Continue cultivando as práticas que te trouxeram essa sensação.")
    elif reflection.day_rating and reflection.day_rating <= 4:
        insights.append("Dias difíceis fazem parte da jornada. Seja gentil consigo mesmo.")
    
    if reflection.presence_level and reflection.presence_level >= 8:
        insights.append("Seu nível de presença está elevado. Isso reflete em maior clareza e bem-estar.")
    elif reflection.presence_level and reflection.presence_level <= 4:
        insights.append("Considere incluir mais momentos de pausa consciente no seu dia.")
    
    if reflection.gratitude:
        insights.append("A prática da gratidão fortalece sua resiliência emocional.")
    
    if reflection.learning:
        insights.append("Seu compromisso com o aprendizado contínuo é admirável.")
    
    return '\n'.join(insights) if insights else "Continue observando seus padrões para insights mais personalizados."

def generate_ai_suggestions(reflection):
    """Gerar sugestões da IA para o próximo dia (simulação)"""
    suggestions = []
    
    if reflection.energy_level and reflection.energy_level <= 4:
        suggestions.append("Priorize atividades de baixa energia amanhã e inclua momentos de descanso.")
    
    if reflection.presence_level and reflection.presence_level <= 5:
        suggestions.append("Experimente fazer 3 pausas conscientes de 2 minutos ao longo do dia.")
    
    if not reflection.gratitude:
        suggestions.append("Que tal começar o dia listando 3 coisas pelas quais você é grato?")
    
    if reflection.day_rating and reflection.day_rating <= 5:
        suggestions.append("Considere incluir uma atividade que te traga alegria na sua agenda de amanhã.")
    
    suggestions.append("Lembre-se: cada momento é uma nova oportunidade de presença.")
    
    return '\n'.join(suggestions)

