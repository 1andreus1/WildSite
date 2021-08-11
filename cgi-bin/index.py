#!/usr/bin/env python3
from requests import post,get
from math import ceil
import cgi
import html
import sys
import codecs
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from time import strftime,time,localtime
import sqlite3
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
sumstr = 10
d2 = strftime("%Y-%m-%d", localtime(time()))
d1 = strftime("%Y-%m-%d", localtime(time() - 2592000))
def tadd(total):
    conn = sqlite3.connect("mydb.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE sum SET sum = "+str(total)+" WHERE idx = 0")
    conn.commit()
def tget():
    conn = sqlite3.connect("mydb.db")
    cursor = conn.cursor()
    cursor.execute("SELECT sum FROM sum WHERE idx = 0")
    return int(cursor.fetchone()[0])
def result(total,p):
    end=ceil(total/sumstr)
    a=[]
    if p==0:
        pass
    else:
        print(1 + (p-1) * sumstr,sumstr + (p-1) * sumstr+1)
        response = post(
            'https://mpstats.io/api/wb/get/seller?d1=' + d1 + '&d2=' + d2 + '&path=' + search,
            headers={'X-Mpstats-TOKEN': '610a8de100ebf6.4662661992188d67d94d5b474ed6433a36ea4888'},
            data={
                'startRow': str(1 + (p-1) * sumstr),
                'endRow': str(sumstr + (p-1) * sumstr+1),
                'filterModel': {},
                'sortModel': []})

        res = response.json()
        r = res['data']
        for i in range(len(r)):
            a.append([str(1 + (p-1) * sumstr + i), str(r[i]['id']), str(r[i]['thumb']), str(r[i]['brand']), str(r[i]['revenue']), str(r[i]['lost_profit']), str(r[i]['final_price']),str(r[i]['sales'])])
    res=''
    for i in a:
        stroka = '<tr><th scope="row">' + str(i[0]) + '</th><td scope="col">' + '<form action="/cgi-bin/index.py" method="post"><input type="hidden" name="action" value="' + str(
            i[1]) + '"><input class="btn btn-link-dark" type="submit" value="' + str(
            i[1]) + '"></form>' + '</th><td scope="col"><img src="' + str(
            i[2]) + '" class="img-thumbnail"></th><td scope="col">' + str(
            i[3]) + '</th><td scope="col">' + str(i[4]) + '</th><td scope="col">' + str(
            i[5]) + '</th><td scope="col">' + str(
            i[6]) + '</th><td scope="col">' + str(i[7]) + '</th></tr>'
        res += stroka
    return res
def buttons(total,p):
    end = ceil(total / sumstr)
    if p==0 or end==0:
        a=[]
    elif end<=11 and 0<end:
        a=list(range(1,p))+[str(p)]+list(range(p+1,end+1))
    else:
        if end-p<5:
            a=list(range(end-10, p)) + [str(p)] + list(range(p + 1, end+1))
        elif p-1<5:
            a=list(range(1, p)) + [str(p)] + list(range(p + 1, 12))
        else:
            a=list(range(p-5,p))+[str(p)]+list(range(p+1,p+6))
    res=''
    for i in a:
        if str(type(i))[-5:-2]=='str':
            res+='<form action="/cgi-bin/index.py" method="post"><input type="hidden" name="action" value="' + 'a'+str(i) + '"><input class="btn" type="submit" value="'+ str(i) +'"></form>'
        else:
            res +='<form action="/cgi-bin/index.py" method="post"><input type="hidden" name="action" value="' + 'a' + str(i) + '"><input class="btn btn-dark" type="submit" value="' + str(i) + '"></form>'
    return res
position='start'
p=0
end=0

form = cgi.FieldStorage()  # Получаем форму
action = form.getfirst("action", "")  # Получаем поле action из формы
all=''
vyr=0
prod=0
butts=''

if action == "search":  # Получаем логин и пароль
    p=1
    search = form.getfirst("search", "")
    search = html.escape(search)
    response = post('https://mpstats.io/api/wb/get/seller?d1=' + d1 + '&d2=' + d2 + '&path=' + search,
                    headers={'X-Mpstats-TOKEN': '610a8de100ebf6.4662661992188d67d94d5b474ed6433a36ea4888'}, data={
            'startRow': '1',
            'endRow': '2',
            'filterModel': {},
            'sortModel': []})
    res = response.json()

    if 'code' in res:
        pass
    else:
        total = res['total']
        tadd(total)
        end = ceil(total / sumstr)
        print(total, end)
        all = result(total, p)
        butts = buttons(total, p)


elif  action.isdigit():
    position='item'
    d2 = strftime("%Y-%m-%d", localtime(time()))
    d1 = strftime("%Y-%m-%d", localtime(time() - 2592000))
    item=str(action)

    response = get(
        'https://mpstats.io/api/wb/get/item/'+item,
        headers={'X-Mpstats-TOKEN': '610a8de100ebf6.4662661992188d67d94d5b474ed6433a36ea4888'}
    )
    res = response.json()
    brand=res['item']['brand']
    seller=res['item']['seller']
    first_date=res['item']['first_date']
    #print(brand,seller,first_date)

    response = get(
        'https://mpstats.io/api/wb/get/item/'+item+'/sales?d1='+d1+'&d2='+d2,
        headers={'X-Mpstats-TOKEN': '610a8de100ebf6.4662661992188d67d94d5b474ed6433a36ea4888'}
    )

    res = response.json()
    sales=[]
    all=''
    for i in range(len(res)):
        data=res[i]['data']
        balance=res[i]['balance']
        final_price=res[i]['final_price']
        sale=res[i]['sales']
        sales.append(sale)
        comments=res[i]['comments']
        #print(data,balance,final_price,sale,comments)
        stroka = '<tr><th scope="row">' + str(i+1) + '</th><td scope="col">' + str(data) + '</th><td scope="col">' + str(balance) + '</th><td scope="col">' + str(final_price) + '</th><td scope="col">' + str(sale) + '</th><td scope="col">' + str(comments) + '</th></tr>'
        all += stroka
    #print(all)
    sale=sales.reverse()
    mm=list(range(1,31))
    m=[]
    t=time()-86400
    for i in range(30):
        m.append(str(localtime(t).tm_mday))
        t-=86400
    m=list(reversed(m))
    fig, ax = plt.subplots(figsize=(18, 11.7))
    ax.bar(mm, sales, color='#212529')
    ax.yaxis.set_major_locator(MultipleLocator(base=1))
    plt.xticks(mm, m)
    plt.tight_layout()
    plt.show()
    plt.savefig('/home/ubuntu/www/media/images/fig.png')
elif action!='' and action[0]=='a':
    total=tget()
    p=int(action[1:])
    all = result(total, p)
    butts = buttons(total, p)


pattern = '''
<!DOCTYPE HTML>
<html>
<head>
<meta charset="utf-8">
<title>Поиск</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-wEmeIV1mKuiNpC+IOBjI7aAzPcEZeedi5yW5f2yOq55WWLwNGmvvx4Um1vskeMj0" crossorigin="anonymous">
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <div class="container">
    <a class="navbar-brand" href="#">InfoPage</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="#">Home</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">Features</a>
        </li>
      </ul>
    </div>
  </div>
</nav>
<div class="container">
<br><br>
{form}

</div>
</body>
</html>
'''

if position=='start':
    pub = '''


        <div class="row">
        <div class="col-3" style="background-color: #e5e5e5;">
        <h5 style="margin-top: 10px;margin-bottom: 15px;">Введите запрос</h5>
        <form action="/cgi-bin/index.py" method="post">


            <div class="mb-3">
            <label for="Название организации" class="form-label">Название организации</label>
            <input type="text" class="form-control" name="search" id="exampleInputEmail1" aria-describedby="dateHelp" required>
            </div>




            <input type="hidden" name="action" value="search">

            <div>
            <div class="d-grid gap-2">
            <button type="submit" class="btn mb-3 btn btn-dark">Найти</button>
            </div>
            </div>
        </form>
        </div>
        <div class="col-9">
        
        <div class="row">
        <table class="table">
      <thead>
        <tr class="table-active">
          <th scope="col">№</th>
          <th scope="col">SKU</th>
          <th scope="col">Фото</th>
          <th scope="col">Бренд</th>
          <th scope="col">Выручка</th>
          <th scope="col">Упущенная выручка</th>
          <th scope="col">Цена</th>
          <th scope="col">Кол-во Продаж</th>
        </tr>
            <tr>
          <th scope="col"></th>
          <th scope="col"></th>
          <th scope="col"></th>
          <th scope="col"></th>
          <th scope="col">''' + str(vyr) + '''</th>
          <th scope="col"></th>
          <th scope="col"></th>
          <th scope="col">''' + str(prod) + '''</th>
        </tr>
      </thead>
      <tbody>
      ''' + all + '''
      </tbody>
    </table>
    
    </div>
    
    <div class="row">
    <div class="btn-toolbar justify-content-center" role="toolbar" aria-label="Toolbar with button groups">

  <div class="btn-group me-2" role="group" aria-label="Second group">
'''+butts+'''
    </div>
  </div>
  
    </div>
    </div>
    
    
        </div>
        </div>
        '''
elif position=='item':
    pub = '''


    <div class="row">
    <div class="col-3" style="background-color: #e5e5e5;">
    <h5 style="margin-top: 10px;margin-bottom: 15px;">Результат</h5>
    <p style="font-weight:550;">Бренд:</p>
    <p>'''+str(brand)+'''</p>
    <p style="font-weight:550;">Продавец:</p>
    <p>'''+str(seller)+'''</p>
    <p style="font-weight:550;">Впервые обнаружен:</p>
    <p>'''+str(first_date)+'''</p>
    </div>
    <div class="col-9">
    <div class="row">
    <img src="http://87.247.157.127/images/fig.png">
    </div>
    
    <div class="row">
    <table class="table">
  <thead>
    <tr class="table-active">
      <th scope="col">№</th>
      <th scope="col">Дата</th>
      <th scope="col">Остаток</th>
      <th scope="col">Со скидкой</th>
      <th scope="col">Сумма продаж</th>
      <th scope="col">Комментариев</th>
    </tr>
  </thead>
  <tbody>''' + all + '''
  </tbody>
</table>
    </div>
    </div>
    </div>
    '''



print(pattern.format(form=pub))
