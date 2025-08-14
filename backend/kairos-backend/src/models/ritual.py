from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Ritual(db.Model):
    __tablename__ = 'rituals'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    
    # Tipo de ritual
    ritual_type = db.Column(db.String(50), nullable=False)  # 'morning', 'evening', 'break', 'custom'
    
    # Configurações do ritual
    duration_minutes = db.Column(db.Integer, default=5)
    instructions = db.Column(db.Text)
    
    # Configurações de repetição
    is_active = db.Column(db.Boolean, default=True)
    frequency = db.Column(db.String(20), default='daily')  # 'daily', 'weekly', 'custom'
    scheduled_time = db.Column(db.Time)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamento com usuário
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'ritual_type': self.ritual_type,
            'duration_minutes': self.duration_minutes,
            'instructions': self.instructions,
            'is_active': self.is_active,
            'frequency': self.frequency,
            'scheduled_time': self.scheduled_time.strftime('%H:%M') if self.scheduled_time else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'user_id': self.user_id
        }

class RitualExecution(db.Model):
    __tablename__ = 'ritual_executions'
    
    id = db.Column(db.Integer, primary_key=True)
    ritual_id = db.Column(db.Integer, db.ForeignKey('rituals.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Dados da execução
    executed_at = db.Column(db.DateTime, default=datetime.utcnow)
    duration_actual = db.Column(db.Integer)  # duração real em minutos
    completion_rating = db.Column(db.Integer)  # 1-5 rating de como foi o ritual
    notes = db.Column(db.Text)
    
    # Relacionamentos
    ritual = db.relationship('Ritual', backref='executions')
    
    def to_dict(self):
        return {
            'id': self.id,
            'ritual_id': self.ritual_id,
            'user_id': self.user_id,
            'executed_at': self.executed_at.isoformat() if self.executed_at else None,
            'duration_actual': self.duration_actual,
            'completion_rating': self.completion_rating,
            'notes': self.notes
        }

