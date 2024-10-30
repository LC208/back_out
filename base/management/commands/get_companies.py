import re
import requests
import random
import string
from django.core.management.base import BaseCommand
from base.serializers import Company_Serializer


class Command(BaseCommand):
    def translit(self,text):
        translit_dict = {
            'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'Yo',
            'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M',
            'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
            'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Sch', 'Ъ': '',
            'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya',
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
            'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
            'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
            'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '',
            'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
            ' ': ' '
        }
        return ''.join(translit_dict.get(char, char) for char in text)

    def generate_random_string(self,n):
        characters = string.ascii_letters + string.digits  # Включает буквы и цифры
        return ''.join(random.choice(characters) for _ in range(n))

    def handle(self,*args,**_):
        st_accept = "text/html"
        st_useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
        headers = {
           "Accept": st_accept,
           "User-Agent": st_useragent,
        }
        req = requests.get("https://open.istu.edu/course/view.php?id=146https://open.istu.edu/course/view.php?id=146%D1%8D%D1%82%D0%BE", headers)
        src = req.text
        companies = []
        names = []
        images = []
        agreements = []
        urls = []
        user = []
        sections = re.split('li id="section-([1-9][0-9]?|0)',src)#i-ая секция хранит всю информацию о i-ой компании
        for i in range(4,len(sections),2):
            companies.append(sections[i])
        companies[38] = (companies[38].split('<section data-region="blocks-column" class="hidden-print"'))[0]
        for i in range(len(companies)):
            #name
            class_section_name = re.search('class="sectionname"><span><a href="\S{,57}">[^<>]+', companies[i])[0]
            section_plus_name = re.search('section-[1-9][0-9]?.+',class_section_name)[0]
            names.append(section_plus_name.split('>')[1] if len((section_plus_name.split('>')[1]).split(' - '))==0 else (section_plus_name.split('>')[1]).split(' - ')[0])
            #img
            img_src = re.findall('<img src="\S+"',companies[i])[0]
            images.append((re.findall('http\S+"',img_src)[0])[:-1]) if not("icon" in img_src) else images.append(None)
            #agreements
            agreements_array = re.findall('Договор с ИрНИТУ.+[0-9][0-9]\.[0-9][0-9]\.[0-9][0-9]',companies[i])
            for elem in range(len(agreements_array)):#для удаления тегов внутри
                agreements_array[elem] = re.sub(r'<.*?>', '', agreements_array[elem])
            if len(agreements_array)>0:
                agreements_array = agreements_array[0].replace('\xa0',' ',1)
                agreements.append(agreements_array[:-1])
            else:
                agreements.append(None)
            #sites
            sub_sites = re.findall('<a class="aalink" onclick="" href="\S{46,48}"><img src="\S{65,67}" class="iconlarge activityicon" alt="" role="presentation" aria-hidden="true" /><span class="instancename">Веб-сайт',companies[i])
            try:
                link = (re.findall('href="\S{46,48}', sub_sites[0])[0])[6:-2]
            except Exception as e:#если нету у компании сайта
                urls.append(None)
            else:
                sub_req = requests.get(link, headers)
                sub_src = sub_req.text
                raw_site = re.findall('Нажмите на ссылку <a href="\S+" >\S+</a>', sub_src)
                urls.append((requests.get(link, allow_redirects=True)).url) if len(raw_site)==0 else urls.append((re.findall('http.+"', raw_site[0])[0])[:-1])
            # users
            login_user = names[i]
            login_user = self.translit(login_user) if len(re.findall('\".+\"',names[i]))==0 else self.translit(re.findall('\".+\"',names[i])[0])
            login_user = login_user.replace('  ', '_').replace(' ', '_').replace('-', '_').replace('.', '').replace('"', '').replace(',', '')
            login_user = login_user[1:] if login_user[0]=='_' else login_user
            pass_user = self.generate_random_string(8)
            user.append({'username':login_user,'password':pass_user,'is_staff':0})
            #sending data
            pract = [{"name":names[i],"faculty":5,"links":[{"type":"Веб-сайт","url":urls[i]}]}]
            if urls[i] is None:
                pract = [{"name":names[i],"faculty":5}]
            data_set={
            "name": names[i],
            "image":images[i],
            "agreements":agreements[i],
            "users":user[i],
            "practices":pract,}
            ser = Company_Serializer(data=data_set)
            if ser.is_valid():
                ser.save()
            else:
                self.stdout.write(self.style.ERROR(f"Ошибка: {ser.errors}"))

        with open('example.txt', 'w') as file:
            # Записываем строку в файл
            file.write(str([{"username":x["username"],"password":x["password"]} for x in user ]))