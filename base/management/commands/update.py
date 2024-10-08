'''
Модуль вытягивает из API институты и направления обучения в них
'''
import MySQLdb
from django.core.management.base import BaseCommand
import requests
import out.settings as db

picture = [
    ('https://job.istu.edu/out/img/IMG_2384.png',
     'Институт авиамашиностроения и транспорта'),
    ('https://job.istu.edu/out/img/kombinirovannoe_logo_png.webp',
     'Институт архитектуры, строительства и дизайна'),
    ('https://job.istu.edu/out/img/logo_ivt.png',
    'Институт высоких технологий'),
    ('https://job.istu.edu/out/img/Logo_itiad_2.png',
     'Институт информационных технологий и анализа данных'),
    ('https://job.istu.edu/out/img/Logotip_IN_b.png',
     'Институт недропользования'),
    ('https://job.istu.edu/out/img/logo-iuep.jpg',
     'Институт экономики, управления и права'),
    ('https://job.istu.edu/out/img/IMG_0263.PNG',
     'Институт энергетики'),
    ('https://www.istu.edu/upload/iblock/d86/logo.jpg',
     'Байкальский институт БРИКС'),
    ('https://www.istu.edu/upload/iblock/f55/logo_1.png',
     'Институт лингвистики и межкультурной коммуникации')
    ]


class Command(BaseCommand):
    '''
    Комманда, которая реализует вытягивание из API институтов и направлений обучения в них 
    и добавляение этих значений в БД
    '''
    help = 'Обновление данных в бд'

    def handle(self, *args, **_):
        r = requests.get(db.API_URL, timeout=10)
        if r.status_code == 200:
            mykeys = [*r.json()['RecordSet']]
            facs = self.get_uniq_value(mykeys, ['fac', 'facid'])
            con = MySQLdb.connect(host=db.DATABASES['default']['HOST'],
                        port=int(db.DATABASES['default']['PORT']),
                        user=db.DATABASES['default']['USER'],
                        password=db.DATABASES['default']['PASSWORD'],
                        database=db.DATABASES['default']['NAME'])
            with con:
                cur = con.cursor()
                sel_tuple = (tuple([x[1] for x in facs]),)
                cur.execute("SELECT name, id FROM faculty WHERE id in %s", sel_tuple)
                f_res = cur.fetchall()
                f_to_add = [x for x in facs if x[0] not in [x[0] for x in f_res]]
                #f_to_del = [x for x in f_res if x[0] not in [x[0] for x in facs]]
                cur.executemany("INSERT INTO faculty (name, id, picture) VALUES (%s, %d, '')",
                                    f_to_add)
                #cur.executemany("DELETE faculty WHERE name=%s AND faculty_id=%d",
                #                    f_to_del)
                cur.executemany("UPDATE faculty SET picture=%s WHERE name=%s",
                                    picture)
                for _ , key in facs:
                    groups = list(self.get_uniq_value(mykeys,
                                                      ['abbr'],
                                                      lambda x, key=key: x['facid'] == key))
                    cur.execute("SELECT name FROM base_speciality WHERE faculty_id=%s", [key])
                    g_res = [x[0] for x in cur.fetchall()]
                    g_to_add = [(x[0], key) for x in groups if x[0] not in g_res]
                    #g_to_del = [(x, key) for x in g_res if x not in [x[0] for x in groups]]
                    cur.executemany('''INSERT INTO base_speciality (name, faculty_id)
                                    VALUES (%s, %s)''',
                                    g_to_add)
                    #cur.executemany("DELETE FROM  base_speciality WHERE name=%s AND faculty_id=%s",
                                    #g_to_del)

                con.commit()


    def get_uniq_value(self, dict_list, names, restrict=lambda x: True):
        '''
        @param dict_list: Лист из словарей с набором значений
        @param names: Набор параметров, который мы вытаскиваем из словарей
        @param restrict: Ограничение в виде анонимной функции
        @return: Уникальные значения для кортежей из параметров names 
        из списка словарей dict_list с ограничением restrict
        '''
        return set([tuple(x[i] for i in names) for x in dict_list if restrict(x)])
