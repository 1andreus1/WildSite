#!/usr/bin/env python3
from requests import post,get
from math import ceil
import cgi
import html
import sys
import codecs
from matplotlib.pyplot import subplots,xticks,savefig
from matplotlib.ticker import MultipleLocator
from time import strftime,time,localtime
from os import remove
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

position='start'

form = cgi.FieldStorage()  # Получаем форму
action = form.getfirst("action", "")  # Получаем поле action из формы
all=''
vyr=0
prod=0

if action == "search":  # Получаем логин и пароль
    search = form.getfirst("search", "")
    search = html.escape(search)
    d2 = strftime("%Y-%m-%d", localtime(time()))
    d1 = strftime("%Y-%m-%d", localtime(time() - 2592000))
    response = post(
        'https://mpstats.io/api/wb/get/seller?d1=' + d1 + '&d2=' + d2 + '&path=' + search,
        headers={'X-Mpstats-TOKEN': '610a8de100ebf6.4662661992188d67d94d5b474ed6433a36ea4888'},
        data={
            'startRow': '1',
            'endRow': '2',
            'filterModel': {},
            'sortModel': []}
    )
    res = response.json()
    try:
        aa=res['code']
    except:
        total = res['total']
        n = ceil(total / 5000)

        all = ''
        k = 1
        for j in range(n):
            response = post(
                'https://mpstats.io/api/wb/get/seller?d1=' + d1 + '&d2=' + d2 + '&path=' + search,
                headers={'X-Mpstats-TOKEN': '610a8de100ebf6.4662661992188d67d94d5b474ed6433a36ea4888'},
                data={
                    'startRow': str(1 + j * 5000),
                    'endRow': str(5000 + j * 5000),
                    'filterModel': {},
                    'sortModel': []}
            )
            res = response.json()
            r = res['data']
            for i in range(len(r)):
                vyr+=int(r[i]['revenue'])
                prod+=int(r[i]['sales'])
                stroka = '<tr><th scope="row">' + str(k) + '</th><td scope="col">' + '<form action="/cgi-bin/index.py" method="post"><input type="hidden" name="action" value="' + str(r[i]['id']) + '"><input class="btn btn-link-dark" type="submit" value="'+ str(r[i]['id']) +'"></form>' + '</th><td scope="col"><img src="' + str(
                    r[i]['thumb']) + '" class="img-thumbnail"></th><td scope="col">' + str(
                    r[i]['brand']) + '</th><td scope="col">' + str(r[i]['revenue']) + '</th><td scope="col">' + str(
                    r[i]['lost_profit']) + '</th><td scope="col">' + str(
                    r[i]['final_price']) + '</th><td scope="col">' + str(r[i]['sales']) + '</th></tr>'
                all += stroka
                k += 1
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

    fig, ax=subplots(figsize=(18, 11.7))
    ax.bar(mm,sales,color='#212529')
    ax.yaxis.set_major_locator(MultipleLocator(base=1))
    xticks(mm,m)
    remove('graph.png')
    savefig('graph.png')
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
    <img src="http://127.0.0.1:8000/graph.png">
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
