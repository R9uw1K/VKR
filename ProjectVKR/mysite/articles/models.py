import json

from django.db import models

# Create your models here.
# Create your models here.
class Article(models.Model):
    article_name = models.TextField('Название статьи')
    article_author = models.TextField('Авторы')
    article_collection = models.TextField('Коллекция')
    article_release = models.TextField('Выпуск')
    article_pages = models.TextField('Страницы')
    article_language = models.TextField('Язык')
    article_path = models.TextField('Путь к файлу', default="")
    article_keywords = models.JSONField('Ключевые слова', default=json.dumps({'0': []}))
    article_annotation = models.TextField('Аннотация', default=None)
    article_issn = models.TextField('ISSN', default=None)
    article_science = models.TextField('Научное направление', default=None)

    def __str__(self):
        return f"{self.id} -- {self.article_name}"

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
