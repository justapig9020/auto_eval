import requests
import random
import json
import matplotlib.pyplot as plt
from PIL import Image
from bs4 import BeautifulSoup

browser = requests.session()
cookie = browser.cookies
web = browser.get('https://ecare.nfu.edu.tw/', cookies=cookie)
parse = BeautifulSoup(web.text, 'lxml')

with open('test.jpg', 'wb') as file:
    web = browser.get('https://ecare.nfu.edu.tw/ext/authimg?rnd=' + str(random.random()), cookies=cookie)
    file.write(web.content)

img = Image.open('test.jpg')
plt.imshow(img)
plt.show()
# stu_id = input('student ID: ')
# stu_pass = input('student pass:')
stu_id = input('ID: ')
stu_pass = input('PW: ')
verify_code = input('Verify Code: ')

data = {
    'login_acc': stu_id,
    'login_pwd': stu_pass,
    'login_chksum': verify_code,
}

login = browser.post('https://ecare.nfu.edu.tw/login/auth', data=data, cookies=cookie)

web = browser.get('https://ecare.nfu.edu.tw/aaiqry/poll', cookies=cookie)
info = BeautifulSoup(web.text, 'lxml')

table = info.find('table', class_='tbcls')
rows = table.find_all('tr')
for row in range(len(rows) - 1):
    if row > 0:
        link = rows[row].find('a')

        data = {}
        if link is not None:
            for i in range(1, 11):
                data['ans' + str(i)] = '3'
            for i in range(11, 20):
                data['ans' + str(i)] = '4'

            for i in range(65, 71):
                data['ans' + str(chr(i))] = '2'
            data['ansG'] = '無'
            data['ansH'] = ''
            data['ansI'] = '無'

            for arg in link['href'].split('?')[1].split('&'):
                key = arg.split('=')[0]
                val = arg.split('=')[1]
                if key == 'seq_id':
                    data['seq_id'] = val
                elif key == 'year':
                    data['year'] = val
                elif key == 'seme':
                    data['seme'] = val

            data['acc'] = stu_id

        web = browser.post('https://ecare.nfu.edu.tw/aaiqry/poll?kind=5&tcc_kind=', data, cookies=cookie)
    cells = rows[row].find_all('td')
    for i in range(1, len(cells)):
        if i == 2:
            print('|' + '%-20s' % cells[i].text, end='')
        elif i == len(cells) - 1:
            print('|done.\t|')
        else:
            print('|' + '%-5s' % cells[i].text, end='')
