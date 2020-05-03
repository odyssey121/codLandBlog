# Внимание для запуска приложения
### Выполните ниже перечисленые шаги сверху вниз
### порядок имеет значение!



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