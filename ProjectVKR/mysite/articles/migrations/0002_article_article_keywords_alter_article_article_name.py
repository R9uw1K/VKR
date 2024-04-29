# Generated by Django 4.2.11 on 2024-04-23 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='article_keywords',
            field=models.JSONField(default={}, verbose_name='Ключевые слова'),
        ),
        migrations.AlterField(
            model_name='article',
            name='article_name',
            field=models.TextField(verbose_name='Название статьи'),
        ),
    ]
