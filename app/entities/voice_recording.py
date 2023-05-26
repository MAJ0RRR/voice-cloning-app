from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class VoiceRecording:
    __tablename__ = 'voice_recordings'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    path = Column(String(200))
    model_id = Column(Integer, ForeignKey("models.id"))

    def __init__(self, name, path, model_id):
        self.name = name
        self.path = path
        self.model_id = model_id

    def __repr__(self):
        return "<VoiceModel(name='%s')>" % (self.name)
