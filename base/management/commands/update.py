import json
import MySQLdb
from django.core.management.base import BaseCommand
import requests
import out.settings as db

faculty_deans = {'5' : 'Говорков Алексей Сергеевич'}


class Command(BaseCommand):
    help = 'Обновление данных в бд'

    def handle(self, *args, **kwargs):
        r = requests.get(db.API_URL)
        if r.status_code == 200:
            mykeys = [*r.json()['RecordSet']]
            for key, value in faculty_deans.items():
                groups = self.get_uniq_value(mykeys, 'abbr', lambda x: x['dean'] == value)
                con = MySQLdb.connect(host='127.0.0.1',
                                      port=4000,
                                      user=db.DATABASES['default']['USER'],
                                      password=db.DATABASES['default']['PASSWORD'],
                                      database=db.DATABASES['default']['NAME'])
                query = "INSERT INTO base_speciality (name, faculty_id) VALUES (%s, %s)"
                with con:
                    cur = con.cursor()
                    cur.execute("SELECT name FROM base_speciality WHERE  faculty_id=%s", key)
                    res = [x[0] for x in cur.fetchall()]
                    cur.executemany(query, [(x, key) for x in groups if x not in res])
                    con.commit()

    def get_uniq_value(self, dict_list, name, restrict):
        return set([x[name] for x in dict_list if restrict(x)])
