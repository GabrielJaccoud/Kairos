from flask import Blueprint, request, jsonify
from datetime import datetime, time
from src.models.user import db
from src.models.ritual import Ritual, RitualExecution

rituals_bp = Blueprint('rituals', __name__)

@rituals_bp.route('/rituals', methods=['GET'])
def get_rituals():
    """Obter todos os rituais do usuário"""
    try:
        user_id = request.args.get('user_id', 1, type=int)
        
        rituals = Ritual.query.filter_by(user_id=user_id).all()
        return jsonify({
            'success': True,
            'rituals': [ritual.to_dict() for ritual in rituals]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@rituals_bp.route('/rituals', methods=['POST'])
def create_ritual():
    """Criar um novo ritual"""
    try:
        data = request.get_json()
        
        if not data.get('name'):
            return jsonify({'success': False, 'error': 'Nome é obrigatório'}), 400
        
        # Converter string de tempo para objeto time se fornecido
        scheduled_time = None
        if data.get('scheduled_time'):
            time_str = data['scheduled_time']
            scheduled_time = datetime.strptime(time_str, '%H:%M').time()
        
        ritual = Ritual(
            name=data['name'],
            description=data.get('description', ''),
            ritual_type=data.get('ritual_type', 'custom'),
            duration_minutes=data.get('duration_minutes', 5),
            instructions=data.get('instructions', ''),
            frequency=data.get('frequency', 'daily'),
            scheduled_time=scheduled_time,
            user_id=data.get('user_id', 1)
        )
        
        db.session.add(ritual)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'ritual': ritual.to_dict(),
            'message': 'Ritual criado com sucesso'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@rituals_bp.route('/rituals/<int:ritual_id>/execute', methods=['POST'])
def execute_ritual(ritual_id):
    """Registrar execução de um ritual"""
    try:
        ritual = Ritual.query.get_or_404(ritual_id)
        data = request.get_json()
        
        execution = RitualExecution(
            ritual_id=ritual_id,
            user_id=ritual.user_id,
            duration_actual=data.get('duration_actual'),
            completion_rating=data.get('completion_rating'),
            notes=data.get('notes', '')
        )
        
        db.session.add(execution)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'execution': execution.to_dict(),
            'message': 'Execução de ritual registrada'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@rituals_bp.route('/rituals/templates', methods=['GET'])
def get_ritual_templates():
    """Obter templates de rituais predefinidos"""
    templates = [
        {
            'name': 'Respiração Matinal',
            'description': 'Comece o dia com clareza e presença',
            'ritual_type': 'morning',
            'duration_minutes': 5,
            'instructions': '1. Sente-se confortavelmente\n2. Feche os olhos\n3. Respire profundamente 10 vezes\n4. Defina uma intenção para o dia',
            'scheduled_time': '07:00'
        },
        {
            'name': 'Meditação Noturna',
            'description': 'Encerre o dia em paz e gratidão',
            'ritual_type': 'evening',
            'duration_minutes': 10,
            'instructions': '1. Deite-se confortavelmente\n2. Relaxe cada parte do corpo\n3. Reflita sobre 3 coisas boas do dia\n4. Respire suavemente até adormecer',
            'scheduled_time': '22:00'
        },
        {
            'name': 'Pausa Consciente',
            'description': 'Momento de presença durante o dia',
            'ritual_type': 'break',
            'duration_minutes': 3,
            'instructions': '1. Pare o que está fazendo\n2. Respire 5 vezes profundamente\n3. Observe seus pensamentos sem julgamento\n4. Retome as atividades com presença',
            'scheduled_time': None
        },
        {
            'name': 'Gratidão Diária',
            'description': 'Cultive a gratidão e aprecie o presente',
            'ritual_type': 'custom',
            'duration_minutes': 5,
            'instructions': '1. Liste 3 coisas pelas quais é grato\n2. Sinta genuinamente a gratidão\n3. Compartilhe mentalmente com alguém especial\n4. Sorria e continue o dia',
            'scheduled_time': '12:00'
        }
    ]
    
    return jsonify({
        'success': True,
        'templates': templates
    })

@rituals_bp.route('/rituals/<int:ritual_id>/stats', methods=['GET'])
def get_ritual_stats(ritual_id):
    """Obter estatísticas de execução de um ritual"""
    try:
        ritual = Ritual.query.get_or_404(ritual_id)
        executions = RitualExecution.query.filter_by(ritual_id=ritual_id).all()
        
        if not executions:
            return jsonify({
                'success': True,
                'stats': {
                    'total_executions': 0,
                    'average_rating': 0,
                    'average_duration': 0,
                    'consistency_score': 0
                }
            })
        
        total_executions = len(executions)
        average_rating = sum(e.completion_rating for e in executions if e.completion_rating) / total_executions
        average_duration = sum(e.duration_actual for e in executions if e.duration_actual) / total_executions
        
        # Calcular consistência (execuções nos últimos 7 dias)
        from datetime import datetime, timedelta
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_executions = [e for e in executions if e.executed_at >= week_ago]
        consistency_score = min(len(recent_executions) / 7.0, 1.0) * 100
        
        return jsonify({
            'success': True,
            'stats': {
                'total_executions': total_executions,
                'average_rating': round(average_rating, 2),
                'average_duration': round(average_duration, 1),
                'consistency_score': round(consistency_score, 1),
                'recent_executions': len(recent_executions)
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@rituals_bp.route('/rituals/<int:ritual_id>', methods=['PUT'])
def update_ritual(ritual_id):
    """Atualizar um ritual"""
    try:
        ritual = Ritual.query.get_or_404(ritual_id)
        data = request.get_json()
        
        if 'name' in data:
            ritual.name = data['name']
        if 'description' in data:
            ritual.description = data['description']
        if 'duration_minutes' in data:
            ritual.duration_minutes = data['duration_minutes']
        if 'instructions' in data:
            ritual.instructions = data['instructions']
        if 'is_active' in data:
            ritual.is_active = data['is_active']
        if 'scheduled_time' in data and data['scheduled_time']:
            ritual.scheduled_time = datetime.strptime(data['scheduled_time'], '%H:%M').time()
        
        ritual.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'ritual': ritual.to_dict(),
            'message': 'Ritual atualizado com sucesso'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

