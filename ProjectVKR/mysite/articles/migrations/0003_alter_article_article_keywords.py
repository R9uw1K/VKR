# Generated by Django 4.2.11 on 2024-04-23 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_article_article_keywords_alter_article_article_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='article_keywords',
            field=models.JSONField(default=None, verbose_name='Ключевые слова'),
        ),
    ]