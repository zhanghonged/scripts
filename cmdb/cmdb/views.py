#coding:utf-8
from django.shortcuts import render_to_response,render
from django.db import connection


def base(request):
    return render(request,'base.html',locals())

def login(request):
    return render(request, 'login.html')

def getpage(sql, page, num = 3, maxpage_num = 7):
    '''
    查询数据库数据
    :param sql: 每次查询的语句
    :param page: 当前的页码
    :param num: 每页数据的条数
    :param maxpage_num: 分页区域显示的页码数量
    :return:查询出来的数据和分页信息
    '''
    page = int(page)
    num = int(num)
    start_page = (page-1) * num
    page_data_sql = sql + ' limit %s,%s'%(start_page,num)
    print page_data_sql
    cursor = connection.cursor() #实例化游标
    cursor.execute(page_data_sql)
    page_data = cursor.fetchall()

    desc = cursor.description #取出表的字段值
    # 把表地段和数据拼接为字典个数，存放到list里
    data_list = [
        dict(zip([d[0] for d in desc],row))
        for row in page_data
    ]
    #查询总条数
    page_total_sql = 'select count(f.id) from (%s) as f'%sql
    cursor.execute(page_total_sql)
    nums = cursor.fetchone()[0]
    #页码最大值
    if nums%num == 0:
        page_total = nums/num
    else:
        page_total = nums/num + 1

    #最多页码显示范围
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