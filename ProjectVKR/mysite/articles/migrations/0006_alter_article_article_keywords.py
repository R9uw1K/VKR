# Generated by Django 4.2.11 on 2024-04-23 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_alter_article_article_keywords'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='article_keywords',
            field=models.JSONField(default={'0': []}, verbose_name='Ключевые слова'),
        ),
    ]
