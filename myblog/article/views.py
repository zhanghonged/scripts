#coding:utf-8
from django.shortcuts import render
from models import Article,Tag
# 导入分页用的3个模块
from django.core.paginator import Paginator ,EmptyPage ,PageNotAnInteger
from django.db.models import Count
from collections import Counter
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
    # 实例化分页对象,每页6条数据,页面显示范围为5
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

def categories(request):
    if request.GET.get('c'):
        c = request.GET.get('c')
        title = '分类|'+ str(c)
        article_obj = Article.objects.filter(category=c)
        header = '%s 分类'%str(c)
        return render(request,'archives.html',{'article_obj':article_obj,'title':title,'header':header})
    else:
        title = '文章分类'
        # postsAll = Article.objects.annotate(num_comment=Count('id'))
        postsAll = Article.objects.all()
        categ = [str(p.category) for p in postsAll if str(p.category) != '']
        categ_dict = Counter(categ)
        return render(request,'categories.html',{'categ_dict':categ_dict,'title':title})

def archives(request):
    title = '归档'
    article_obj = Article.objects.all().order_by('time').reverse()
    header = '很好! 目前共计 %s 篇日志。 继续努力。'%len(article_obj)
    try:
        current_page = int(request.GET.get('page'))
    except:
        current_page = 1
    # 实例化分页对象,每页15条数据,页面显示范围为5
    paginator = CustomPaginator(current_page,5,article_obj,15)
    try:
        # 取对象的当前页分页对象
        posts = paginator.page(current_page)
    # current_page非数字时取第一页
    except PageNotAnInteger:
        posts = paginator.page(1)
    # current_page空时取最后一页
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request,'archives.html',{'posts':posts,'title':title,'header':header})

def tags(request):
    """
    实现标签功能
    根据指定标签获取标签下的全部文章
    :param request:
    :return:
    """
    if request.GET.get('tag'):
        tag = request.GET.get('tag').encode('utf8')
        title = '标签|'+ tag
        header = '%s 标签' %tag
        article_obj = Article.objects.filter(tags__name=tag)
        return render(request,'archives.html',{'header':header,'title':title,'article_obj':article_obj})
    else:
        title = '标签'
        tags_list = Tag.objects.all()
        return render(request,'tags.html',{'title':title,'tags_list':tags_list})