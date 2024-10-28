'''
Модуль вытягивает из API институты и направления обучения в них
'''
import re
from django.core.management.base import BaseCommand
import requests
import out.settings as db
from base.serializers import SpecialitySerializer
from base.models import Speciality

pictures = [
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

trans = {"46":5, "36":7,"45":2,"69725":16,"38":8,"50":14,"33":1,"34":6,"43":3}


class Command(BaseCommand):
    '''
    Комманда, которая реализует вытягивание из API направлений обучения
    и добавляение этих значений в БД
    '''
    help = 'Обновление данных в бд'

    def handle(self, *args, **_):
        r = requests.get(db.API_URL, timeout=10)
        if r.status_code == 200:
            mykeys = [*r.json()['RecordSet']]
            groups = list(self.get_uniq_value(mykeys,
                                                ['abbr', 'facid'],
                                                reg=r'[.]'))

            groups = [(x[0], trans[str(x[1])]) if str(x[1]) in trans else x for x in groups]
            not_in = list()
            specs = Speciality.objects.all()
            for spec in specs:
                if (spec.name, spec.faculty_id) not in groups:
                    spec.delete()
            for x in groups:
                name = x[0]
                faculty_id = x[1]
                if not Speciality.objects.filter(name=name, faculty=faculty_id):
                    not_in.append({'name':name, 'faculty':faculty_id})
                
            deser = SpecialitySerializer(data=not_in, many=True)
            if deser.is_valid():
                deser.save()

    def get_uniq_value(self, dict_list, names, restrict=lambda x: True, reg=''):
        '''
        @param dict_list: Лист из словарей с набором значений
        @param names: Набор параметров, который мы вытаскиваем из словарей
        @param restrict: Ограничение в виде анонимной функции
        @return: Уникальные значения для кортежей из параметров names 
        из списка словарей dict_list с ограничением restrict
        '''
        return set([tuple(re.sub(reg, '', x[i]) if isinstance(x[i], str) else x[i] for i in names) for x in dict_list if restrict(x)])
