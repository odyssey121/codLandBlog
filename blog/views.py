from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Count
from .models import Article, ArticleDetail, AuthUser
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .forms import CreateArticleForm, RegisterForm, LoginForm
from django.conf import settings
from uuid_upload_path import uuid
import mimetypes
from os import path

# Create your views here.
from blog import models


def logout(request):
    auth.logout(request)
    return redirect('blog:login')


def login(request):
    if request.method == "POST":
        form_obj = LoginForm(request.POST)
        if form_obj.is_valid():
            username = form_obj.cleaned_data.get("username")
            password = form_obj.cleaned_data.get("password")
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return redirect("blog:home")
        else:
            return render(request, "login.html", {"title": "Авторизация", "form_obj": form_obj})

    form_obj = LoginForm
    return render(request, "login.html", {"title": "Авторизация", "form_obj": form_obj})


def register(request):
    if request.method == "POST":
        form_obj = RegisterForm(request.POST)
        if form_obj.is_valid():
            username = form_obj.cleaned_data.get("username")
            password = form_obj.cleaned_data.pop('re_password')
            user_obj = AuthUser.objects.create_user(username=username, password=password)
            auth.login(request, user_obj)
            return redirect("blog:home")
        else:
            return render(request, 'register.html', {'form_obj': form_obj, "title": "Добавить статью"})

    form_obj = RegisterForm()
    return render(request, 'register.html', {"form_obj": form_obj, "title": "Регистрация"})


def home(request):
    articles = models.Article.objects.order_by('-create_time').all()
    article_recent = articles[0] if len(articles) > 1 else None
    article_list = articles[1:] if len(articles) > 2 else articles
    category_list = models.Category.objects.all()
    return render(request, 'home.html', {
        "article_recent": article_recent,
        "article_list": article_list,
        "category_list": category_list,
        "title": "Главная"
    })


@login_required
def add_article(request):
    if request.method == 'POST':
        form_obj = CreateArticleForm(request.POST, request.FILES)
        if form_obj.is_valid():
            saved_data = dict()
            saved_data['title'] = form_obj.cleaned_data.get('title')
            raw_desc = form_obj.cleaned_data.get("desc")
            saved_data['user'] = request.user
            file_obj = form_obj.cleaned_data.get("image")
            if file_obj:
                file_uuid_name = uuid()
                file_ext = mimetypes.guess_extension(file_obj.content_type)
                file_name = "{}{}".format(file_uuid_name, file_ext)
                saved_data['prev_image'] = file_name
                filepath = path.join(settings.MEDIA_ROOT, 'image', file_name)
                with open(filepath, "wb") as f:
                    for chunk in file_obj.chunks():
                        f.write(chunk)

            from bs4 import BeautifulSoup
            bs = BeautifulSoup(raw_desc, "html.parser")
            saved_data['desc'] = bs.text[0:225] + "..." if len(bs.text) > 225 else bs.text
            # фильтруем опасные теги
            for tag in bs.find_all():
                if tag.name in ['script', 'link']:
                    tag.decompose()
            article_obj = Article.objects.create(**saved_data)
            ArticleDetail.objects.create(content=str(bs), article=article_obj,
                                         image=saved_data.get("prev_image", 'not_found.png'))
            return redirect("blog:home")

        else:
            return render(request, 'add_article.html', {'form_obj': form_obj, "title": "Добавить статью"})

    form_obj = CreateArticleForm()
    return render(request, 'add_article.html', {'form_obj': form_obj, "title": "Добавить статью"})
