# Generated by Django 3.0.5 on 2020-05-03 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20200503_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='prev_image',
            field=models.CharField(default='not_found.png', max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='articledetail',
            name='image',
            field=models.CharField(default='not_found.png', max_length=80, null=True),
        ),
    ]