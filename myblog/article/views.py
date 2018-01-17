#coding:utf-8
from django.shortcuts import render
from models import Article
# Create your views here.


def Article_list(request):
    article_list = Article.objects.all()
    return render(request,'article_list.html',locals())

def Article_content(request,article_id):
    current_id = int(article_id)
    article = Article.objects.get(id = current_id)
    return render(request,'article.html',locals())

def test(request):
    return render(request,'test.html',locals())