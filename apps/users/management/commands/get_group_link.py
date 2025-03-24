import re

import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from apps.faculties.models import Faculty
from apps.specialities.models import Speciality


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        url = "https://www.istu.edu/abiturientu/bakalavriat_spetsialitet/napravleniya"
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        items = soup.find_all("dir", class_="directioncard-item")
        output_b = []  # бакалавры и специалитет
        for item in items:
            edu_level = item.find(class_="directioncard-item-level").find("b").text
            links = item.find_all("a")
            for link in links:
                clear_name = (
                    re.sub(r"^\d+(\.\d+)*\s+", "", link.text).split("/")[0].rstrip()
                )
                button_link = "https://www.istu.edu" + link.get("href")
                response = requests.get(button_link)
                html_link = response.text
                soup_link = BeautifulSoup(html_link, "html.parser")
                inst_blank = soup_link.find_all(
                    "div", class_="eduprofile-item-subdname eduprofile-form-element"
                )
                for blank in inst_blank:
                    current_inst = blank.find(
                        class_="eduprofile-form-element-value"
                    ).text
                    if "заочно-вечернего" not in current_inst:
                        break
                inst = Faculty.objects.filter(name=current_inst)
                if len(inst) == 0:
                    continue
                if "бакалавриат" in edu_level:
                    output_b.append(
                        {
                            "faculty": inst[0].id,
                            "url": button_link,
                            "full_name": clear_name,
                            "education_level": 2,
                        }
                    )
                elif "специалитет" in edu_level:
                    output_b.append(
                        {
                            "faculty": inst[0].id,
                            "url": button_link,
                            "full_name": clear_name,
                            "education_level": 1,
                        }
                    )

        url = "https://www.istu.edu/abiturientu/magistratura/napravleniya"
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        items = soup.find_all("div", class_="eduprofile-item")
        output_m = []  # магистранты
        for item in items:
            dir = item.find(class_="eduprofile-item-dirlevel").text.replace("\n", "")
            clear_name = (
                item.find(class_="eduprofile-item-header")
                .text.replace("\n", "")
                .split("/")[0]
                .rstrip()
            )
            link = item.find(class_="eduprofile-item-link").find("a").get("href")
            link = "https://www.istu.edu" + link if "http" not in link else link
            if "abiturientu" in link:
                response = requests.get(link)
                html_link = response.text
                soup_link = BeautifulSoup(html_link, "html.parser")
                inst_blank = soup_link.find_all(
                    "div", class_="eduprofile-item-subdname eduprofile-form-element"
                )
                for blank in inst_blank:
                    current_inst = blank.find(
                        class_="eduprofile-form-element-value"
                    ).text
                    if "заочно-вечернего" not in current_inst:
                        break
                inst = Faculty.objects.filter(name=current_inst)
                if len(inst) == 0:
                    continue
                output_m.append(
                    {
                        "faculty": inst[0].id,
                        "url": link,
                        "full_name": clear_name,
                        "education_level": 3,
                    }
                )
        output_m.extend(output_b)
        for spec in output_m:
            specialities = Speciality.objects.filter(
                faculty=Faculty.objects.get(id=spec["faculty"]),
                full_name=spec["full_name"],
                education_level=spec["education_level"],
            )
            if specialities.exists():  # Если записи найдены, обновляем их
                specialities.update(url=spec["url"])
