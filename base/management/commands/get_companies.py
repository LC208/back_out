import re
import requests
from django.core.management.base import BaseCommand
from base.serializers import CompanySerializer,PracticeAddSerializer,DockLinkSerializer


class Command(BaseCommand):
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

        for i in range(len(companies)):
            company_data = [{'name':names[i],'image':images[i],'agreements':agreements[i]}]
            companies = []
            for company in company_data:
                company_serializer = CompanySerializer(data=company)
                if company_serializer.is_valid():
                    company_instance = company_serializer.save()
                    companies.append(company_instance)  # Сохраняем экземпляры авторов
                else:
                    self.stdout.write(self.style.ERROR(f"Ошибка: {company_serializer.errors}"))
            for j in range(len(companies)):
                practice_data = [{'name':names[j],'faculty':5,'company':companies[j].id}]
                practices = []
                for practice in practice_data:
                    practice_serializer = PracticeAddSerializer(data=practice)
                    if practice_serializer.is_valid():
                        practice_instance = practice_serializer.save()
                        practices.append(practice_instance)  # Сохраняем экземпляры книг
                    else:
                        self.stdout.write(self.style.ERROR(f"Ошибка: {practice_serializer.errors}"))
            for j in range(len(practices)):
                dock_data = [{'type': 'Веб-сайт', 'url': urls[i],'practice':practices[j].id}]
                for dock in dock_data:
                    dock_serializer = DockLinkSerializer(data=dock)
                    if dock_serializer.is_valid():
                        dock_serializer.save()
                    else:
                        self.stdout.write(self.style.ERROR(f"Ошибка: {dock_serializer.errors}"))
