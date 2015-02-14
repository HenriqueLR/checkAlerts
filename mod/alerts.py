#encoding: utf-8
'''
Created on 30/04/2014

@author: Henrique Luz Rodrigues
'''

from datetime import date
from con.core import Connection
from mod.seek import Query
from random import randint
import commands
from con.fraudes import TempAlerts, Alerts



class Alerts(object):

    def __init__(self, cq = Connection()):
        self.__host = commands.getoutput("hostname")
        self.__block = cq.block()
        self.__alerts = cq.alerts()
        self.__spw = Query(self.__alerts, self.__block)

    def check_alert(self, sql, sigla, code, integration):
        try:
            self.__alerts.close_all()
            self.__block.close_all()
            created = date.today()
            if sql:
                for alerts in sql:
                    context = {}
                    context['number'] = str(alerts).split("'")[1]
                    context['qtd'] = int(str(alerts).split(", ")[1].split("L)")[0])
                    context['created'] = str(created)
                    context['description'] = sigla
                    context['cod'] = code
                    self.__spw.history(context)
                    self.check_none(self.__spw.alerts(context), context, integration)

            self.__spw.clean(code, sigla)
            self.__alerts.close_all()
            self.__block.close_all()
        except Exception, e:
            print ("ERROR: %s" % e)

    def check_none(self, resp, config, integration):

        if resp:
            list_send = []
            list_send.append(resp['number'])
            list_send.append(resp['qtd'])
            list_send.append(resp['created'])
            list_send.append(resp['description'].upper())
            integration.enviarEmail("INCIDENTE %s:" % resp['description']+"-ALTO VOLUME DE CHAMADAS -"+''+self.__host, list_send)
            integration.LogComIncidente(resp['description'], list_send)
            self.__spw.confirm_alert(resp)

            if resp['description'] == 'cqcsi':
                self.__spw.block_number(resp)

        if resp is None:
            integration.LogSemIncidente(config['description'].upper())

    def generator_code(self):
        code = randint(1,1000)
        exist_code = self.__spw.generator(code)
        if exist_code is True:
            return code
        if exist_code is False:
           return self.generator_code()

    def temp_clean(self, sigla):
        trans = str(sigla)
        self.__spw.factor_clean(trans)