#coding:utf-8
from django.shortcuts import render
from models import Article
# 导入分页用的3个模块
from django.core.paginator import Paginator ,EmptyPage ,PageNotAnInteger
# Create your views here.

# 扩展自定义表单分页
class CustomPaginator(Paginator):
    def __init__(self ,current_page, per_pager_num, *args, **kwargs):
        # 当前页
        self.current_page = int(current_page)
        # 页码最大显示范围
        self.per_pager_num = per_pager_num
        # 继承父类Paginator的其他属性方法
        Paginator.__init__(self, *args, **kwargs)
    def pager_num_range(self):
        if self.num_pages < self.per_pager_num:
            return range(1, self.num_pages + 1)
        part = int(self.per_pager_num / 2)
        if self.current_page <= part:
            return range(1, self.per_pager_num + 1)
        if (self.current_page + part) > self.num_pages:
            return range(self.num_pages - self.per_pager_num + 1, self.num_pages + 1)
        else:
            return range(self.current_page - part, self.current_page + part + 1)

def Article_list(request):
    cus_list = Article.objects.all()
    try:
        current_page = int(request.GET.get('page'))
    except:
        current_page = 1
    # 实例化分页对象,每页6条数据,页面显示范围为6
    paginator = CustomPaginator(current_page,5,cus_list,6)
    try:
        # 取对象的当前页分页对象
        posts = paginator.page(current_page)
    # current_page非数字时取第一页
    except PageNotAnInteger:
        posts = paginator.page(1)
    # current_page空时取最后一页
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request,'article_list.html',{'posts':posts})

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
