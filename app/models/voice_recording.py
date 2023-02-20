from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class VoiceRecording:
    __tablename__ = 'voice_models'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    path = Column(String(200))

    def __init__(self, name, path):
        self.name = name
        self.path = path

    def __repr__(self):
        return "<VoiceModel(name='%s')>" % (self.name)