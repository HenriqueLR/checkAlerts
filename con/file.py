#encoding: utf-8
'''
Created on 30/04/2014

@author: Henrique Luz Rodrigues
'''
from ConfigParser import ConfigParser, Error
import os

class FileConfig(object):

    def __init__(self):
        self.__fileName = "/.config.ini"
        self.__filePath = (os.path.dirname(__file__)+self.__fileName).split()
        self.__parser = ConfigParser()
        
        try:
            self.__parser.read(self.__filePath)
            self.__configSections = self.__parser.sections()
            try:
                self.__bd = self.__parser.items(self.__configSections[0])
                self.__bd2 = self.__parser.items(self.__configSections[1])
            except Error, e:
                print("Erro: " + e)
        except Error, e:
            print("Erro: " + e)
            
    def dbConfig(self):
        return dict(self.__bd)

    def dbBlock(self):
        return dict(self.__bd2)
