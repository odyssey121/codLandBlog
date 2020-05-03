from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import URLValidator
from django.conf import settings


class AuthUser(AbstractUser):
    """
    Форма информации Пользователя блога
    """
    nid = models.AutoField(primary_key=True)
    avatar = models.FileField(upload_to="media/avatars/", default="/media/avatars/default.svg")
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Article(models.Model):
    """
    Статьи блога
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=80)
    desc = models.CharField(max_length=255)
    prev_image = models.CharField(max_length=80, null=True, default="not_found.png")
    create_time = models.DateTimeField(auto_now_add=True)
    comment_count = models.IntegerField(verbose_name="количество комментариев", default=0)
    up_count = models.IntegerField(verbose_name="понравилось", default=0)
    down_count = models.IntegerField(verbose_name="не понравилось", default=0)
    category = models.ForeignKey(to="Category", to_field="nid", null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(to="AuthUser", to_field="nid", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class ArticleDetail(models.Model):
    """
    Детализация статьи блога
    """
    nid = models.AutoField(primary_key=True)
    content = models.TextField()
    article = models.OneToOneField(to="Article", to_field="nid", on_delete=models.CASCADE)
    image = models.CharField(max_length=80, null=True, default='not_found.png')


class ArticleUpDown(models.Model):
    """
    Список лайков
    """
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to="AuthUser", null=True, on_delete=models.SET_NULL)
    article = models.ForeignKey(to="Article", null=True, on_delete=models.SET_NULL)
    is_up = models.BooleanField(default=True)

    class Meta:
        unique_together = (("article", "user"),)


class Comment(models.Model):
    """
    Коментарии статьи
    """
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(to="Article", to_field="nid", on_delete=models.CASCADE)
    user = models.ForeignKey(to="AuthUser", to_field="nid", on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


class Category(models.Model):
    """
    Категория статьи
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)

    def __str__(self):
        return self.title
