# Generated by Django 5.0.4 on 2024-04-21 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_name', models.IntegerField(verbose_name='Название статьи')),
                ('article_author', models.TextField(verbose_name='Авторы')),
                ('article_collection', models.TextField(verbose_name='Коллекция')),
                ('article_release', models.TextField(verbose_name='Выпуск')),
                ('article_pages', models.TextField(verbose_name='Страницы')),
                ('article_language', models.TextField(verbose_name='Язык')),
                ('article_path', models.TextField(default='', verbose_name='Путь к файлу')),
            ],
            options={
                'verbose_name': 'Статья',
                'verbose_name_plural': 'Статьи',
            },
        ),
    ]
