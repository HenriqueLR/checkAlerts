#encoding: utf-8
'''
Created on 30/04/2014

@author: Henrique Luz Rodrigues
'''

from con.fraudes import Alerts, TempAlerts, Authani


class Query(object):


    def __init__(self, session1, session2):
        self.__session = session1
        self.__session2 = session2

    def alerts(self, config):
        row = self.__session.query(TempAlerts)\
                .from_statement("SELECT temp_alerts.id_temp_alerts, number, created, description "
                                "FROM temp_alerts "
                                "WHERE number =:dict1 "
                                "AND created =:dict2 "
                                "AND description =:dict3")\
                                .params(dict1=config['number'], dict2=config['created'], dict3=config['description'])

        if row.all() == []:
            obj = TempAlerts(number=config['number'],qtd=config['qtd'],created=config['created'],description=config['description'],cod=config['cod'])
            self.__session.add(obj)
            self.__session.commit()
            return config
        else:
            for param in row:
                if param.qtd < config['qtd']:
                    self.__session.query(TempAlerts).filter_by(id_temp_alerts=param.id_temp_alerts).update({"qtd":config['qtd'], "cod":config['cod']})
                    self.__session.commit()
                    return config

                if param.qtd > config['qtd']:
                    self.__session.query(TempAlerts).filter_by(id_temp_alerts=param.id_temp_alerts).update({"qtd":config['qtd'], "cod":config['cod']})
                    self.__session.commit()
                    return None

                if param.qtd == config['qtd']:
                    self.__session.query(TempAlerts).filter_by(id_temp_alerts=param.id_temp_alerts).update({"qtd":config['qtd'], "cod":config['cod']})
                    self.__session.commit()
                    return None

    def history(self, config):
        obj = Alerts(number=config['number'], qtd=config['qtd'], created=config['created'], description=config['description'], status=False)
        self.__session.add(obj)
        self.__session.commit()

    def generator(self, params):
        trans = str(params)
        exist = self.__session.query(TempAlerts)\
                    .from_statement("SELECT temp_alerts.id_temp_alerts, cod "
                                    "FROM temp_alerts "
                                    "WHERE cod =:cod")\
                                    .params(cod=trans)
        if exist.all() == []:
            self.__session.close()
            return True
        else:
            self.__session.close()
            return False

    def clean(self, param1, param2):
        trans = str(param1)
        exist = self.__session.query(TempAlerts)\
                    .from_statement("SELECT temp_alerts.id_temp_alerts, cod "
                                    "FROM temp_alerts "
                                    "WHERE cod !=:cod "
                                    "AND description =:description")\
                                    .params(cod=trans, description=param2)
        if exist.all() != []:
            for remove in exist:
                self.__session.delete(remove)
                self.__session.commit()

    def confirm_alert(self, config):
        self.__session.query(Alerts)\
            .filter_by(number=config['number'], created=config['created'],
                       qtd=config['qtd'], description=config['description'])\
            .update({"status":True})
        self.__session.commit()

    def block_number(self, param):
        n = int(param['number'])
        aplic = self.__session2.query(Authani)\
                .from_statement("SELECT authani.ani "
                                "FROM authani "
                                "WHERE ani=:ani")\
                                .params(ani=n)
        if aplic:
            for slash in aplic:
                self.__session2.query(Authani)\
                    .filter_by(ani=slash.ani)\
                    .update({"block":1})
                self.__session2.commit()

    def factor_clean(self, sigla):
        verify = self.__session.query(TempAlerts).from_statement("SELECT * FROM temp_alerts WHERE description=:g").params(g=sigla)

        for rm in verify:
            self.__session.delete(rm)
            self.__session.commit()
        self.__session.close()
