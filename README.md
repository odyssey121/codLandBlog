## Ссылка на тестовую развёртку на heroku => https://codeland-landing.herokuapp.com/
# Внимание для запуска приложения 
### Выполните ниже перечисленые шаги сверху вниз
### порядок имеет значение!
###(в настройках вбита тестовая база так что можно пропустить,
###шаги 2-4 если не будете подключать свою)



## CMD

```bash
1 install dependencies
$ pip install -r requirements.txt

2 create auth migration  
$ python manage.py migrate auth

3 create blog migration  
$ python manage.py migrate blog

4 create other migration
$ python manage.py migrate

5 run dev server  
$ python manage.py runserver
```

##чтобы добавлять статьи зарегестрируйтесь.