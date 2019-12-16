import requests
import random
import json
import matplotlib.pyplot as plt
from PIL import Image
from bs4 import BeautifulSoup

def wrt(row, scr):
    link = row.find('a')

    data = {}
    if link is not None:
        for i in range(1, 11):
            data['ans' + str(i)] = str(scr + random.randint(-1,1))
        for i in range(11, 20):
            data['ans' + str(i)] = str(scr + random.randint(-1,1))

        for i in range(65, 71):
            data['ans' + str(chr(i))] = str(1 + random.randint(0,1))
        data['ansG'] = ''
        data['ansH'] = ''
        data['ansI'] = ''

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
        print (data)
        web = browser.post('https://ecare.nfu.edu.tw/aaiqry/poll?kind=5&tcc_kind=', data, cookies=cookie)
        cells = row.find_all('td')
        for i in range(1, len(cells)):
            if i == 2:
                print('|' + '%-20s' % cells[i].text, end='')
            elif i == len(cells) - 1:
                print('|done.\t|')
            else:
                print('|' + '%-5s' % cells[i].text, end='')

def show_cls(rows):
    for row in range(1,len(rows) - 1):
        cells = rows[row].find_all('td')
        print(str(row) + ' ' +  cells[2].text)

def auto(rows):
    for row in range(len(rows) - 1):
        if row > 0:
            wrt(rows[row], 3)
            
def manual(rows):
    cls = len(rows)-2
    print (cls+1)
    temp = [ 0 for i in range(cls+1) ]
    while True:
        for row in range(1,len(rows) - 1):
            cells = rows[row].find_all('td')
            print(str(row) + ': ' +  cells[2].text)
        print ('0: exit')
        slct = input('- ')
        
        if slct.isnumeric() == False:
            continue
        slct = int(slct)
        if slct == 0:
            break
        elif slct <= cls and temp[slct] == 0:
            print("select: " + rows[slct].find_all('td')[2].text)
            tchlv = input("Teacher: (g)ood (n)ormal (s)uck (e)xit\n- ")
            if tchlv in "good":
                wrt(rows[slct], 4)
            elif tchlv in "normal":
                wrt(rows[slct], 3)
            elif tchlv in "suck":
                wrt(rows[slct], 2)
            else:
                continue

            temp[slct] = 1
              
        print()
    slct = input("Auto write left: (y)es (n)o:")
    if slct in "yes":
        for row in range(1, len(rows) - 1):
            print (str(row) + ": ")
            if row > 0 and temp[row] == 0:
                wrt(rows[row], 3)
                



browser = requests.session()
cookie = browser.cookies
web = browser.get('https://ecare.nfu.edu.tw/', cookies=cookie)
parse = BeautifulSoup(web.text, 'lxml')

with open('test.jpg', 'wb') as file:
    web = browser.get('https://ecare.nfu.edu.tw/ext/authimg?rnd=' + str(random.random()), cookies=cookie)
    file.write(web.content)

img = Image.open('test.jpg')

# stu_id = input('student ID: ')
# stu_pass = input('student pass:')

stu_id = input('ID: ')
stu_pass = input('PW: ')


plt.imshow(img)
plt.show()
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

print ("Class of this semester:")
show_cls(rows)

while True:
    slct = input ("Auto write? (y)es (n)o (e)ixt: ")
    if slct in "yes":
        # print("yes")
        auto(rows)
        break
    elif slct in "no":
        # print("no")
        manual(rows)
        break

