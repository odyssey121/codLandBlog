from django.contrib import admin
from blog import models
# Register your models here.

admin.site.register(models.AuthUser)
admin.site.register(models.Article)
admin.site.register(models.Category)
admin.site.register(models.Comment)
admin.site.register(models.ArticleUpDown)
admin.site.register(models.ArticleDetail)