"""
Модуль вытягивает из API институты и направления обучения в них
"""

import re
from django.core.management.base import BaseCommand
import requests
import out.settings as db
from apps.specialities.serializers import SpecialitySerializer
from apps.specialities.models import Speciality
import json

pictures = [
    (
        "https://job.istu.edu/out/img/IMG_2384.png",
        "Институт авиамашиностроения и транспорта",
    ),
    (
        "https://job.istu.edu/out/img/kombinirovannoe_logo_png.webp",
        "Институт архитектуры, строительства и дизайна",
    ),
    ("https://job.istu.edu/out/img/logo_ivt.png", "Институт высоких технологий"),
    (
        "https://job.istu.edu/out/img/Logo_itiad_2.png",
        "Институт информационных технологий и анализа данных",
    ),
    ("https://job.istu.edu/out/img/Logotip_IN_b.png", "Институт недропользования"),
    (
        "https://job.istu.edu/out/img/logo-iuep.jpg",
        "Институт экономики, управления и права",
    ),
    ("https://job.istu.edu/out/img/IMG_0263.PNG", "Институт энергетики"),
    ("https://www.istu.edu/upload/iblock/d86/logo.jpg", "Байкальский институт БРИКС"),
    (
        "https://www.istu.edu/upload/iblock/f55/logo_1.png",
        "Институт лингвистики и межкультурной коммуникации",
    ),
]

trans = {
    "46": 5,
    "36": 7,
    "45": 2,
    "69725": 16,
    "38": 8,
    "50": 14,
    "33": 1,
    "34": 6,
    "43": 3,
}
trans_el = [1, 2, 3, 4, 5]


class Command(BaseCommand):
    """
    Комманда, которая реализует вытягивание из API направлений обучения
    и добавляение этих значений в БД
    """

    help = "Обновление данных в бд"

    def handle(self, *args, **_):
        r = requests.get(db.API_URL, timeout=10)
        if r.status_code == 200:
            mykeys = [*r.json()["RecordSet"]]
            groups = list(
                self.get_uniq_value(
                    mykeys,
                    ["abbr", "facid", "cadmkind", "spec_name", "direct_name"],
                    reg=r"[.]",
                )
            )
            groups = [
                (
                    x[0].strip(),
                    trans[str(x[1])],
                    x[2],
                    x[3].strip() if x[3] is not None else x[4].strip(),
                )
                for x in groups
                if str(x[1]) in trans and x[2] in trans_el
            ]
            not_in = list()
            specs = Speciality.objects.all()
            to_upd_codes = {}
            ids = []
            codes = [x[0] for x in groups]
            for spec in specs:
                if (
                    spec.code in codes
                    and (
                        spec.code,
                        spec.faculty_id,
                        spec.education_level,
                        spec.name,
                    )
                    not in groups
                ):
                    to_upd_codes[spec.code] = spec.id
                    ids.append(spec.id)
                elif spec.code not in codes:
                    spec.delete()
            for x in groups:
                name = x[0]
                faculty_id = x[1]
                education_level = x[2]
                full_name = x[3]
                if name in to_upd_codes:
                    not_in.append(
                        {
                            "id": to_upd_codes[name],
                            "code": name,
                            "faculty": faculty_id,
                            "education_level": education_level,
                            "name": full_name,
                        }
                    )

                elif not Speciality.objects.filter(
                    code=name,
                    faculty=faculty_id,
                    education_level=education_level,
                    name=full_name,
                ):
                    not_in.append(
                        {
                            "code": name,
                            "faculty": faculty_id,
                            "education_level": education_level,
                            "name": full_name,
                        }
                    )
            deser_upd = SpecialitySerializer(
                Speciality.objects.filter(id__in=ids), data=not_in, many=True
            )
            # deser = SpecialitySerializer(data=not_in, many=True)
            # if deser.is_valid(raise_exception=True):
            #     deser.save()
            if deser_upd.is_valid(raise_exception=True):
                deser_upd.save()

    def get_uniq_value(self, dict_list, names, restrict=lambda x: True, reg=""):
        """
        @param dict_list: Лист из словарей с набором значений
        @param names: Набор параметров, который мы вытаскиваем из словарей
        @param restrict: Ограничение в виде анонимной функции
        @return: Уникальные значения для кортежей из параметров names
        из списка словарей dict_list с ограничением restrict
        """
        return set(
            [
                tuple(
                    re.sub(reg, "", x[i]) if isinstance(x[i], str) else x[i]
                    for i in names
                )
                for x in dict_list
                if restrict(x)
            ]
        )
