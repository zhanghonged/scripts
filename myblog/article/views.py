#coding:utf-8
from django.shortcuts import render
from models import Article
# 导入分页用的3个模块
from django.core.paginator import Paginator ,EmptyPage ,PageNotAnInteger
# Create your views here.


def Article_list(request):
    cus_list = Article.objects.all()


    # 实例化结果集，定义每页显示4条数据
    paginator = Paginator(cus_list,4)
    # 接收网页中的page值
    page = request.GET.get('page')
    # 获取当前页对象的元素列表
    if page:
        article_list = paginator.page(page).object_list
    else:
        article_list = paginator.page(1).object_list
    # 获取page页的分页对象
    try:
        customer = paginator.page(page)
    # 页码不会一个整数异常，赋值为第一页
    except PageNotAnInteger:
        customer = paginator.page(1)
    # 空页码异常，赋值为最后一页
    except EmptyPage:
        customer = paginator.page(paginator.num_pages)
    return render(request, 'article_list.html', {'cus_list':customer,'article_list':article_list})


def Article_content(request,article_id):
    current_id = int(article_id)
    article = Article.objects.get(id = current_id)
    # 获取id不为空的所有文件列表
    articleAll = Article.objects.filter(id__isnull=False)
    article_list = list(articleAll)

    # 由于id可能出现不连续，所以通过切片取值方法来获取上一页和下一页
    if article == article_list[-1]:
        before_page = article_list[-2]
        after_page = None
    elif article == article_list[0]:
        before_page = None
        after_page = article_list[1]
    else:
        situ = article_list.index(article)
        before_page = article_list[situ-1]
        after_page = article_list[situ+1]

    return render(request,'article.html',{'article':article,'before_page':before_page,'after_page':after_page})
