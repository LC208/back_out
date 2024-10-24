import re
import requests

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
result = []
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
    agreements_array = re.findall('Договор[^<]+<',companies[i])
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
    result.append({'name':names[i],'img':images[i],'agreements':agreements[i],'urls':urls[i]})
    print(result[i])
