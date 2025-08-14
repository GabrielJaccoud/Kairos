from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from src.models.user import db

class DailyReflection(db.Model):
    __tablename__ = 'daily_reflections'
    
    id = db.Column(db.Integer, primary_key=True)
    reflection_date = db.Column(db.Date, nullable=False, default=date.today)
    
    # Os 4 pilares da reflexão diária
    gratitude = db.Column(db.Text)      # Gratidão pelo que foi vivido
    forgiveness = db.Column(db.Text)    # Perdão para liberar o que incomoda
    learning = db.Column(db.Text)       # Aprendizado para crescer continuamente
    overcoming = db.Column(db.Text)     # Superação de desafios do dia
    
    # Avaliação geral do dia
    day_rating = db.Column(db.Integer)  # 1-10 rating do dia
    presence_level = db.Column(db.Integer)  # 1-10 nível de presença
    energy_level = db.Column(db.Integer)    # 1-10 nível de energia
    
    # IA Insights
    ai_insights = db.Column(db.Text)    # Insights gerados pela IA
    ai_suggestions = db.Column(db.Text) # Sugestões da IA para o próximo dia
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamento com usuário
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Constraint para garantir uma reflexão por dia por usuário
    __table_args__ = (db.UniqueConstraint('user_id', 'reflection_date', name='unique_daily_reflection'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'reflection_date': self.reflection_date.isoformat() if self.reflection_date else None,
            'gratitude': self.gratitude,
            'forgiveness': self.forgiveness,
            'learning': self.learning,
            'overcoming': self.overcoming,
            'day_rating': self.day_rating,
            'presence_level': self.presence_level,
            'energy_level': self.energy_level,
            'ai_insights': self.ai_insights,
            'ai_suggestions': self.ai_suggestions,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'user_id': self.user_id
        }

class PresenceLog(db.Model):
    __tablename__ = 'presence_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Dados do momento de presença
    logged_at = db.Column(db.DateTime, default=datetime.utcnow)
    activity = db.Column(db.String(200))
    presence_score = db.Column(db.Integer)  # 1-10 score de presença no momento
    mood = db.Column(db.String(50))         # humor no momento
    context = db.Column(db.String(100))     # contexto (trabalho, casa, lazer, etc.)
    
    # Notas opcionais
    notes = db.Column(db.Text)
    
    # Relacionamento com usuário
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'logged_at': self.logged_at.isoformat() if self.logged_at else None,
            'activity': self.activity,
            'presence_score': self.presence_score,
            'mood': self.mood,
            'context': self.context,
            'notes': self.notes,
            'user_id': self.user_id
        }

