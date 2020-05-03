from django import forms
from django.contrib import auth
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MaxLengthValidator, MinLengthValidator
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from .models import AuthUser


def desc_validator(value):
    if (len(value.strip()) < 10):
        raise ValidationError('Поле описание должно быть не меньше 10 символов')
    # if (len(value.strip()) > 500):
    #     raise ValidationError('Поле описание максимальный размер 500 символов')


def file_size(value):
    limit = 9 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('Загружаемый файл слишком велик (макс 9 Мб)')


# ФОРМА СОЗДАНИЯ СТАТЬИ
class CreateArticleForm(forms.Form):
    title = forms.CharField(
        required=True,
        max_length=80,
        min_length=4,
        label='Заголовок',
        widget=forms.widgets.TextInput(attrs={"class": "validate", "name": "title", "id": "title","data-length":"80"}),
        error_messages={
            "max_length": "достигнута максимальная длинна",
            "required": "обязательное поле",
            "min_length": "заголовок слишком короткий"
        }
    )
    desc = forms.CharField(
        validators=[desc_validator],
        error_messages={"required": "Поле описание обязательно к заполнению"},
        widget=SummernoteWidget(),
    )

    image = forms.FileField(
        widget=forms.FileInput(attrs={'accept': 'image/*', 'name': 'file', 'class': 'hide', 'id': 'files', }),
        validators=[file_size],
        required=False)


# ФОРМА РЕГИСТРАЦИИ
class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=16,
        label="имя пользователя",
        widget=forms.widgets.TextInput(attrs={"class": "validate", "name": "username", "id": "username"}),
        error_messages={
            "max_length": "имя пользователя не должно привышать 16 символов",
            "required": "имя пользователя обязательное поле",
        }
    )
    password = forms.CharField(
        min_length=3,
        label="пароль",
        widget=forms.widgets.PasswordInput(
            attrs={"class": "validate", "name": "password", "id": "pass", "type": "password"}, render_value=True),
        error_messages={
            "min_length": "минимальный пароль 6 символов",
            "required": "пароль обязательное поле"
        }
    )
    re_password = forms.CharField(
        min_length=3,
        label="пароль еще раз",
        widget=forms.widgets.PasswordInput(
            attrs={"class": "validate", "name": "re_password", "id": "re_pass", "type": "password"}, render_value=True),
        error_messages={
            "min_length": "минимальный пароль 6 символов",
            "required": "пароль обязательное поле"
        }
    )

    # валидация username
    def clean_username(self):
        username = self.cleaned_data.get("username")
        is_exist = AuthUser.objects.filter(username=username)
        if is_exist:
            self.add_error("username", ValidationError("Имя пользователя уже существует！"))
        else:
            return username

    def clean(self):
        password = self.cleaned_data.get("password")
        re_password = self.cleaned_data.get("re_password")
        if re_password and re_password != password:
            self.add_error("re_password", ValidationError("Пароли не совпадают"))
        else:
            return self.cleaned_data


# ФОРМА ЛОГИНА
class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=16,
        label="имя пользователя",
        widget=forms.widgets.TextInput(attrs={"class": "validate", "name": "username", "id": "username"}),
        error_messages={
            "max_length": "имя пользователя не должно привышать 16 символов",
            "required": "имя пользователя обязательное поле",
        }
    )
    password = forms.CharField(
        label="пароль",
        widget=forms.widgets.PasswordInput(
            attrs={"class": "validate", "name": "password", "id": "password", "type": "password"}, render_value=True),

    )

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = auth.authenticate(username=username, password=password)
        if user:
            return self.cleaned_data
        else:
            self.add_error("password", ValidationError("Неверное имя пользователя или пароль"))
