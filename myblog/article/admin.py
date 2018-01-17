from django.contrib import admin
from models import Article
# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','author','time')
    search_fields = ('title','author')
    list_filter = ('time','author')


admin.site.register(Article,ArticleAdmin)
