#encoding: utf-8
'''
Created on 30/04/2014

@author: Henrique Luz Rodrigues
'''

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean

Base = declarative_base()


class Alerts(Base):
    __tablename__ = 'alerts'

    id_alerts = Column(Integer,primary_key=True)
    number = Column(String)
    qtd = Column(Integer)
    created = Column(String)
    description = Column(String)
    status = Column(Boolean)

    def __init__(self, number, qtd, created, description, status):
        self.number = number
        self.qtd = qtd
        self.created = created
        self.description = description
        self.status = status
    def __repr__(self):
        return u'%s, %s, %s, %s, %s, %s' % (self.id_alerts, self.number, self.qtd, self.created, self.description, self.status)
    
class TempAlerts(Base):    
    __tablename__ = 'temp_alerts'
    id_temp_alerts = Column(Integer, primary_key=True)
    number = Column(String)
    qtd = Column(Integer)
    created = Column(String)
    description = Column(String)
    cod = Column(String)
    
    def __init__(self, number, qtd, created, description, cod):
        self.number = number
        self.qtd = qtd
        self.created = created
        self.description = description
        self.cod = cod
    
    def __repr__(self):
        return u'%s, %s, %s, %s, %s, %s' % (self.id_temp_alerts, self.number, self.qtd, self.created, self.description, self.cod)


class Authani(Base):
    __tablename__ = 'authani'
    ani = Column(Integer, primary_key=True)
    acccode = Column(Integer)
    block = Column(Integer)
    tipo_linha = Column(Integer)
    id_cliente = Column(Integer)
    id_plano = Column(Integer)
    block_outros_csp = Column(Integer)
    block_cel_lc = Column(Integer)
    block_cel_ld = Column(Integer)
    block_fixo_ldn = Column(Integer)
    block_acobrar = Column(Integer)
    block_internacional = Column(Integer)
    
    def __init__(self, block):
        self.block = block

    def __repr__(self):
        return u'%s, %s' % (self.ani, self.block)
