from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Matriz Adaptada de Presença
    importance_level = db.Column(db.String(20), nullable=False)  # 'high', 'low'
    urgency_level = db.Column(db.String(20), nullable=False)     # 'high', 'low'
    presence_axis = db.Column(db.Boolean, default=False)         # Eixo da Presença
    
    # Integração Humana
    contacts = db.Column(db.Text)  # JSON string com contatos relacionados
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    scheduled_for = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    
    # Status
    status = db.Column(db.String(20), default='pending')  # 'pending', 'in_progress', 'completed'
    
    # IA Insights
    ai_priority_score = db.Column(db.Float, default=0.0)
    ai_energy_requirement = db.Column(db.String(20))  # 'low', 'medium', 'high'
    ai_suggested_time = db.Column(db.DateTime)
    
    # Relacionamento com usuário
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'importance_level': self.importance_level,
            'urgency_level': self.urgency_level,
            'presence_axis': self.presence_axis,
            'contacts': self.contacts,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'scheduled_for': self.scheduled_for.isoformat() if self.scheduled_for else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'status': self.status,
            'ai_priority_score': self.ai_priority_score,
            'ai_energy_requirement': self.ai_energy_requirement,
            'ai_suggested_time': self.ai_suggested_time.isoformat() if self.ai_suggested_time else None,
            'user_id': self.user_id
        }
    
    def get_quadrant(self):
        """Retorna o quadrante da matriz baseado na importância e urgência"""
        if self.presence_axis:
            return 'presence'
        elif self.importance_level == 'high' and self.urgency_level == 'high':
            return 'urgent_important'
        elif self.importance_level == 'high' and self.urgency_level == 'low':
            return 'important_not_urgent'
        elif self.importance_level == 'low' and self.urgency_level == 'high':
            return 'urgent_not_important'
        else:
            return 'not_urgent_not_important'

