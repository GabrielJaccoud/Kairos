from flask import Blueprint, request, jsonify
from datetime import datetime
import json
from src.models.user import db
from src.models.task import Task

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks', methods=['GET'])
def get_tasks():
    """Obter todas as tarefas do usuário"""
    try:
        # Por simplicidade, usando user_id = 1. Em produção, usar autenticação
        user_id = request.args.get('user_id', 1, type=int)
        
        tasks = Task.query.filter_by(user_id=user_id).all()
        return jsonify({
            'success': True,
            'tasks': [task.to_dict() for task in tasks]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@tasks_bp.route('/tasks', methods=['POST'])
def create_task():
    """Criar uma nova tarefa"""
    try:
        data = request.get_json()
        
        # Validação básica
        if not data.get('title'):
            return jsonify({'success': False, 'error': 'Título é obrigatório'}), 400
        
        task = Task(
            title=data['title'],
            description=data.get('description', ''),
            importance_level=data.get('importance_level', 'low'),
            urgency_level=data.get('urgency_level', 'low'),
            presence_axis=data.get('presence_axis', False),
            contacts=json.dumps(data.get('contacts', [])),
            scheduled_for=datetime.fromisoformat(data['scheduled_for']) if data.get('scheduled_for') else None,
            user_id=data.get('user_id', 1)  # Em produção, usar autenticação
        )
        
        db.session.add(task)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'task': task.to_dict(),
            'message': 'Tarefa criada com sucesso'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@tasks_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Atualizar uma tarefa"""
    try:
        task = Task.query.get_or_404(task_id)
        data = request.get_json()
        
        # Atualizar campos se fornecidos
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'importance_level' in data:
            task.importance_level = data['importance_level']
        if 'urgency_level' in data:
            task.urgency_level = data['urgency_level']
        if 'presence_axis' in data:
            task.presence_axis = data['presence_axis']
        if 'contacts' in data:
            task.contacts = json.dumps(data['contacts'])
        if 'scheduled_for' in data:
            task.scheduled_for = datetime.fromisoformat(data['scheduled_for']) if data['scheduled_for'] else None
        if 'status' in data:
            task.status = data['status']
            if data['status'] == 'completed':
                task.completed_at = datetime.utcnow()
        
        task.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'task': task.to_dict(),
            'message': 'Tarefa atualizada com sucesso'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@tasks_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Deletar uma tarefa"""
    try:
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tarefa deletada com sucesso'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@tasks_bp.route('/tasks/matrix', methods=['GET'])
def get_tasks_by_matrix():
    """Obter tarefas organizadas pela matriz adaptada"""
    try:
        user_id = request.args.get('user_id', 1, type=int)
        
        tasks = Task.query.filter_by(user_id=user_id, status='pending').all()
        
        matrix = {
            'urgent_important': [],
            'important_not_urgent': [],
            'urgent_not_important': [],
            'not_urgent_not_important': [],
            'presence': []
        }
        
        for task in tasks:
            quadrant = task.get_quadrant()
            matrix[quadrant].append(task.to_dict())
        
        return jsonify({
            'success': True,
            'matrix': matrix
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@tasks_bp.route('/tasks/ai-optimize', methods=['POST'])
def ai_optimize_tasks():
    """Endpoint para otimização de tarefas pela IA"""
    try:
        user_id = request.args.get('user_id', 1, type=int)
        data = request.get_json()
        
        # Simulação de otimização por IA
        # Em produção, isso chamaria o motor de IA
        tasks = Task.query.filter_by(user_id=user_id, status='pending').all()
        
        optimized_tasks = []
        for task in tasks:
            # Simulação de score de prioridade baseado em IA
            if task.importance_level == 'high' and task.urgency_level == 'high':
                task.ai_priority_score = 0.9
            elif task.importance_level == 'high':
                task.ai_priority_score = 0.7
            elif task.urgency_level == 'high':
                task.ai_priority_score = 0.6
            else:
                task.ai_priority_score = 0.3
            
            # Sugestão de energia necessária
            if task.ai_priority_score > 0.8:
                task.ai_energy_requirement = 'high'
            elif task.ai_priority_score > 0.5:
                task.ai_energy_requirement = 'medium'
            else:
                task.ai_energy_requirement = 'low'
            
            optimized_tasks.append(task.to_dict())
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'optimized_tasks': sorted(optimized_tasks, key=lambda x: x['ai_priority_score'], reverse=True),
            'message': 'Tarefas otimizadas pela IA'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

