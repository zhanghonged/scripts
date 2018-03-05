#coding:utf-8
import random
from django.shortcuts import render
from Admin.views import loginValid
from django.http import HttpResponseRedirect
from django.db import connection

@loginValid
def index(request):
    return render(request,'index.html')

content = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyz'

def login(request):
    v_data = "".join(random.sample(content,28))
    response = render(request,'login.html',locals())
    response.set_cookie('key',v_data)
    return response

def logout(request):
    c_phone = request.COOKIES.get('phone')
    s_phone = request.session['phone']
    if c_phone and s_phone:
        del request.COOKIES['phone']
        # del request.session['phone']
        request.session.flush()
    return HttpResponseRedirect('/login')

def getpage(sql,page,num = 10,maxpage_num = 7):
    '''
    :param sql:每次查询的语句
    :param page: 当前的页码
    :param num: 每页数据的条数
    :param maxpage_num: 分页区域显示的页码数量
    :return: 查询出来的数据
    '''
    #查询当前页码的数据
    page = int(page)
    num = int(num)
    start_page = (page-1) * num
    page_data_sql = sql + ' limit %s,%s'%(start_page,num)
    cur = connection.cursor() #实例化游标
    cur.execute(page_data_sql)
    page_data = cur.fetchall()

    desc = cur.description #取表的字段
    #把表地段和数据拼接为字典个数，存放到list里
    data_list = [
        dict(zip([d[0] for d in desc],row))
        for row in page_data
    ]
    #查询总条数
    page_total_sql = 'select count(f.id) from (%s) as f'%sql
    cur.execute(page_total_sql)
    nums = cur.fetchone()[0]
    if nums%num == 0:
        page_total = nums/num
    else:
        page_total = nums/num +1

    #最多显示页码范围
    part = maxpage_num/2
    if page_total < maxpage_num:
        page_range = [i for i in range(1,page_total+1)]
    elif page <= part:
        page_range = [i for i in range(1,maxpage_num+1)]
    elif page + part > page_total:
        page_range = [i for i in range(page_total-maxpage_num,page_total+1)]
    else:
        page_range = [i for i in range(page-part,page+part+1)]

    result = {
        'page_data':data_list,
        'page_range':page_range,
        'current_page':page,
        'max_page':page_total
    }
    return result

# def getpage(request):
#     cur = connection.cursor() #实例化游标
#     cur.execute('select * from Equipment_equipment limit 0,3')
#     all_data = cur.fetchall()
#
#     desc = cur.description #取表的字段
#     #把表地段和数据拼接为字典个数，存放到list里
#     data_list = [
#         dict(zip([d[0] for d in desc],row))
#         for row in all_data
#     ]
#     return JsonResponse({'data':data_list})