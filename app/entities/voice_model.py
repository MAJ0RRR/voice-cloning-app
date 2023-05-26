from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class VoiceModel(Base):
    __tablename__ = 'models'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    path_model = Column(String(200))
    path_config = Column(String(200))
    gender = Column(String(10))
    language = Column(String(2))

    def __init__(self, name, path_model, path_config, gender, language):
        self.name = name
        self.path_model = path_model
        self.path_config = path_config
        self.gender = gender
        self.language = language

    def __repr__(self):
        return "<VoiceModel(name='%s')>" % (self.name)
