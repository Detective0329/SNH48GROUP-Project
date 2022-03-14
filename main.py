import re
import requests
import xlwt
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
data = []
savepath = 'SNH48GROUP.xls'

sname_pattern = re.compile('"sname":"(.*?)"')
nickname_pattern = re.compile('"nickname":"(.*?)"')
height_pattern = re.compile('"height":"(.*?)"')
blood_type_pattern = re.compile('"blood_type":"(.*?)"')
birth_day_pattern = re.compile('"birth_day":"(.*?)"')
star_sign_12_pattern = re.compile('"star_sign_12":"(.*?)"')
birth_place_pattern = re.compile('"birth_place":"(.*?)"')
speciality_pattern = re.compile('"speciality":"(.*?)"')
hobby_pattern = re.compile('"hobby":"(.*?)"')
join_day_pattern = re.compile('"join_day":"(.*?)"')
pname_pattern = re.compile('"pname":"(.*?)"')
catch_phrase_pattern = re.compile('"catch_phrase":"(.*?)"')

def get_data(url):
    wb_data = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(wb_data.content, 'lxml')

    sname_list = re.findall(sname_pattern, soup.text)
    nickname_list = re.findall(nickname_pattern, soup.text)
    height_list = re.findall(height_pattern, soup.text)
    blood_type_list = re.findall(blood_type_pattern, soup.text)
    birth_day_list = re.findall(birth_day_pattern, soup.text)
    star_sign_12_list = re.findall(star_sign_12_pattern, soup.text)
    birth_place_list = re.findall(birth_place_pattern, soup.text)
    speciality_list = re.findall(speciality_pattern, soup.text)
    hobby_list = re.findall(hobby_pattern, soup.text)
    join_day_list = re.findall(join_day_pattern, soup.text)
    pname_list = re.findall(pname_pattern, soup.text)
    catch_phrase_list = re.findall(catch_phrase_pattern, soup.text)

    for sname, nickname, height, blood_type, birth_day, star_sign_12, birth_place, speciality, hobby, join_day, pname, catch_phrase in zip(sname_list, nickname_list, height_list, blood_type_list, birth_day_list, star_sign_12_list, birth_place_list, speciality_list, hobby_list, join_day_list, pname_list, catch_phrase_list):
        datum = {}
        datum[0] = sname.encode('utf-8').decode('unicode-escape')
        datum[1] = nickname.encode('utf-8').decode('unicode-escape')
        datum[2] = height
        datum[3] = blood_type
        datum[4] = birth_day
        datum[5] = star_sign_12.encode('utf-8').decode('unicode-escape')
        datum[6] = birth_place.encode('utf-8').decode('unicode-escape')
        datum[7] = speciality.encode('utf-8').decode('unicode-escape')
        datum[8] = hobby.encode('utf-8').decode('unicode-escape')
        datum[9] = join_day
        datum[10] = pname.encode('utf-8').decode('unicode-escape')
        datum[11] = catch_phrase.encode('utf-8').decode('unicode-escape')
        data.append(datum)

def save_data(data, savepath):
    print('正在保存中，请稍候………………')
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('SNH48GROUP', cell_overwrite_ok=True)
    cols = ('姓名', '昵称', '身高', '血型', '生日', '星座', '出生地', '个人特长', '兴趣爱好', '加入时间', '加入所属', '自我介绍')
    sheet.write_merge(0, 0, 0, 11, 'SNH48GROUP 全成员个人资料一览（截止至2022/03/14）')
    for col in range(0, 12):
        sheet.write(1, col, cols[col])
    for row in range(len(data)):
        datum = data[row]
        for col in range(0, 12):
            sheet.write(row+2, col, datum[col])
    book.save(savepath)
    print('保存完毕！')

if __name__ == '__main__':
    urls = ['https://h5.48.cn/resource/jsonp/allmembers.php?gid={}0&callback=get_members_success'.format(page) for page in range(1, 8)]
    for url in urls:
        get_data(url)
    save_data(data, savepath)
    print('爬虫程序运行完毕！')
