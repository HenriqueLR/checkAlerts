#encoding: utf-8
'''
Created on 30/04/2014

@author: Henrique Luz Rodrigues
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from con.file import FileConfig



class Connection(object):

    def __init__(self, config=FileConfig()):
        self.__config = config.dbConfig()
        self.__block = config.dbBlock()
        self.__session = sessionmaker()       

    def alerts(self):
        _engine_ = create_engine(self.__config['engine']+self.__config['user']+
                                       self.__config['pass']+self.__config['host']+
                                       self.__config['port']+self.__config['db'])
        self.__session.configure(bind=_engine_)
        return self.__session()

    def block(self):
        _engine_ = create_engine(self.__block['engine']+self.__block['user']+
                                 self.__block['pass']+self.__block['host']+
                                 self.__block['port']+self.__block['db'])
        self.__session.configure(bind=_engine_)
        return self.__session()