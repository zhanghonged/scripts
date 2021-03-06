from django.contrib import admin
from models import *
# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','author','time')
    # search_fields = ('title','author')
    # list_filter = ('time','author')

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name','age','gender')

class TagAdmin(admin.ModelAdmin):
    list_display = ('name','create_time')
admin.site.register(Article,ArticleAdmin)
admin.site.register(Author,AuthorAdmin)
admin.site.register(Tag,TagAdmin)