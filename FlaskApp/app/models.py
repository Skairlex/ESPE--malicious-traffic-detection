from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Results(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    firstname = Column(String(100), nullable=False)

    def __str__(self):
        return self.firstname

class Escaner(Base):
    __tablename__ = 'escaner'
    id = Column(Integer, primary_key=True)
    tipo = Column(Integer, nullable=False)
    nombre = Column(String(100), nullable=False)
    cantidad = Column(Integer, nullable=False)

    def __str__(self):
        return self.nombre

class Bitacora(Base):
    __tablename__ = 'bitacora'
    id = Column(Integer, primary_key=True)
    terminal = Column(String(100), nullable=False)
    fecha = Column(String(100), nullable=False)
    beningn = Column(String(100), nullable=False)
    attack_brute_force = Column(String(100), nullable=False)
    attack_XSS = Column(String(100), nullable=False)
    attack_SQL_injection = Column(String(100), nullable=False)

    def __str__(self):
        return self.terminal


class Analisis(Base):
    __tablename__ = 'analisis'
    id = Column(Integer, primary_key=True)
    fechaInicio = Column(String(100), nullable=False)
    fechaFin = Column(String(100), nullable=True)
    resultado = Column(String(100), nullable=False)
    estado=Column(String(100), nullable=False)
    task_id= Column(String(150), nullable=True)

    def __str__(self):
        return self.resultado


class Resultado(Base):
    __tablename__ = 'resultados'
    id = Column(Integer, primary_key=True)
    tipo = Column(String(100), nullable=False)
    ip = Column(String(100), nullable=False)
    puerto = Column(String(100), nullable=False)
    hora = Column(String(100), nullable=False)
    analisis_id=Column(Integer,ForeignKey('analisis.id'))
    analisis=relationship(Analisis,backref ='resultados')

    def __str__(self):
        return self.tipo

