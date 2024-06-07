from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import force_bytes
from .models import Article
import rdflib
import json
import yaml
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom


def home(request):
    collections = Article.objects.values_list('article_collection', flat=True).distinct()
    return render(request, 'articles/home.html', {'collections': collections})

@csrf_exempt
def articles(request):
        all_articles = Article.objects.filter(article_collection=json.loads(request.body)['collection'])
        return render(request, 'articles/articles.html', {'articles': all_articles})



def article(request, article_id):
    article = Article.objects.filter(id=article_id)[0]
    print(article.article_release)
    return render(request, 'articles/article.html', {'article': article})


# Функция нормализации одной статьи в Dublin Core
def normalize_article_to_dublin_core(article):
    graph = rdflib.Graph()
    article_uri = rdflib.URIRef(f"http://127.0.0.1:8000/{article.id}")
    graph.add((article_uri, rdflib.RDF.type, rdflib.FOAF.Document))
    graph.add((article_uri, rdflib.DCTERMS.title, rdflib.Literal(article.article_name)))
    graph.add((article_uri, rdflib.DCTERMS.creator, rdflib.Literal(article.article_author)))
    graph.add((article_uri, rdflib.DCTERMS.source, rdflib.Literal(article.article_collection)))
    graph.add((article_uri, rdflib.DCTERMS.date, rdflib.Literal(article.article_release)))
    graph.add((article_uri, rdflib.DCTERMS.coverage, rdflib.Literal(article.article_pages)))
    graph.add((article_uri, rdflib.DCTERMS.language, rdflib.Literal(article.article_language)))
    return graph.serialize(format='xml', encoding='utf-8')


# Функция нормализации одной статьи в JATS формате
def normalize_article_to_jats(article, version):
    article_elem = Element("article")
    SubElement(article_elem, "article_name").text = article.article_name
    SubElement(article_elem, "article_author").text = article.article_author
    SubElement(article_elem, "article_collection").text = article.article_collection
    SubElement(article_elem, "article_release").text = article.article_release
    SubElement(article_elem, "article_pages").text = article.article_pages
    SubElement(article_elem, "article_language").text = article.article_language
    SubElement(article_elem, "kwd-group").text = str(article.article_keywords["0"])
    article_elem.set('version', version)
    xml_str = tostring(article_elem, 'utf-8')
    parsed_str = minidom.parseString(xml_str)
    return parsed_str.toprettyxml(indent="  ")



# Функция экспорта одной статьи в RDF формате
def export_article_to_rdf(article):
    graph = rdflib.Graph()
    article_uri = rdflib.URIRef(f"http://127.0.0.1:8000/{article.id}")
    graph.add((article_uri, rdflib.RDF.type, rdflib.FOAF.Document))
    graph.add((article_uri, rdflib.URIRef("http://purl.org/dc/terms/title"), rdflib.Literal(article.article_name, lang='ru')))
    graph.add((article_uri, rdflib.URIRef("http://purl.org/dc/terms/creator"), rdflib.Literal(article.article_author)))
    graph.add((article_uri, rdflib.URIRef("http://purl.org/dc/terms/source"), rdflib.Literal(article.article_collection)))
    graph.add((article_uri, rdflib.URIRef("http://purl.org/dc/terms/date"), rdflib.Literal(article.article_release, lang='ru')))
    graph.add((article_uri, rdflib.URIRef("http://purl.org/dc/terms/coverage"), rdflib.Literal(article.article_pages, lang='ru')))
    graph.add((article_uri, rdflib.URIRef("http://purl.org/dc/terms/language"), rdflib.Literal(article.article_language, lang='ru')))
    graph.add((article_uri, rdflib.URIRef("http://purl.org/dc/terms/description"), rdflib.Literal(article.article_keywords, lang='ru')))
    return graph.serialize(format='xml', encoding='utf-8')




# Функция нормализации одной статьи в EuDML формате
def normalize_article_to_eudml(article):
    root = Element('eudml')
    title = SubElement(root, 'title')
    title.text = article.article_name
    creator = SubElement(root, 'creator')
    creator.text = article.article_author
    collection = SubElement(root, 'collection')
    collection.text = article.article_collection
    url = SubElement(root, 'url')
    url.text = f"http://127.0.0.1:8000/{article.id}/"
    description = SubElement(root, 'abstract')
    description.text = article.article_annotation
    pages = SubElement(root, 'description')
    pages.text = article.article_pages
    volume = SubElement(root, 'volume')
    volume.text = article.article_release
    fileFormat = SubElement(root, 'fileFormat')
    fileFormat.text = 'pdf'
    xml_str = tostring(root, 'utf-8')
    parsed_str = minidom.parseString(xml_str)
    return parsed_str.toprettyxml(indent="  ")


# Функция экспорта одной статьи в XML формате
def export_article_to_xml(article):
    article_elem = Element("article")
    SubElement(article_elem, "article_name").text = article.article_name
    SubElement(article_elem, "article_author").text = article.article_author
    SubElement(article_elem, "article_collection").text = article.article_collection
    SubElement(article_elem, "article_release").text = article.article_release
    SubElement(article_elem, "article_pages").text = article.article_pages
    SubElement(article_elem, "article_language").text = article.article_language
    SubElement(article_elem, "article_keywords").text = str(article.article_keywords["0"])
    return minidom.parseString(tostring(article_elem)).toprettyxml()


# Функция экспорта одной статьи в JSON формате
def export_article_to_json(article):
    volume = vars(article)
    volume['_state'] = str(volume['_state'])
    return json.loads(json.dumps(volume))


# Функция экспорта одной статьи в YAML формате
def export_article_to_yaml(article):
    volume = vars(article)
    volume['_state'] = str(volume['_state'])
    return yaml.dump(volume)


# Django endpoint для экспорта статьи по её идентификатору в RDF
@csrf_exempt
def rdf_export_by_id(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404("Статья не найдена")
    rdf_data = export_article_to_rdf(article)
    return HttpResponse(rdf_data, content_type="application/rdf+xml; charset=utf-8")


# Django endpoint для экспорта статьи по её идентификатору в XML
@csrf_exempt
def xml_export_by_id(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404("Статья не найдена")
    xml_data = export_article_to_xml(article)
    return HttpResponse(xml_data, content_type="application/xml")


# Django endpoint для экспорта статьи по её идентификатору в YAML
@csrf_exempt
def yaml_export_by_id(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404("Статья не найдена")
    yaml_data = export_article_to_yaml(article)
    return HttpResponse(yaml_data, content_type="text/yaml")


# Django endpoint для экспорта статьи по её идентификатору в JSON
@csrf_exempt
def json_export_by_id(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404("Статья не найдена")
    json_data = export_article_to_json(article)
    return JsonResponse(json_data, safe=False)


@csrf_exempt
def eudml_export_by_id(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404("Статья не найдена")
    error = []
    if article.article_name == '':
        error.append('Название статьи')
    if article.article_author == '':
        error.append('Авторы')
    if article.article_collection == '':
        error.append('Библиография')
    if not error:
        eudml_data = normalize_article_to_eudml(article)
        return HttpResponse(eudml_data, content_type="application/xml")
    else:
        return render(request, 'articles/error.html', {'main_text': 'Недостаточно обязательных метаданных для нормализации EuDML, воспользуйтесь редактором метаданных, чтобы добавить:', 'errors': error})


@csrf_exempt
def dublincore_export_by_id(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404("Статья не найдена")
    error = []
    if article.article_name == '':
        error.append('Название статьи')
    if article.article_author == '':
        error.append('Автор')
    if article.article_collection == '':
        error.append('Библиография')
    if article.article_release == '':
        error.append('Выпуск и год')
    if article.article_pages == '':
        error.append('Страницы')
    if article.article_language == '':
        error.append('Язык')
    if not error:
        dublincore_data = normalize_article_to_dublin_core(article)
        return HttpResponse(dublincore_data, content_type="application/rdf+xml; charset=utf-8")
    else:
        error_main_text = 'Недостаточно данных, воспользуйтесь редактором метаданных!'
        # return HttpResponse("<script>location.href='/'; alert('Недостаточно данных, воспользуйтесь редактором метадынных!');</script>")
        return render(request, 'articles/error.html', {'main_text': error_main_text, 'errors': error})


@csrf_exempt
def jats_export_by_id(request, version, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404("Статья не найдена")
    error = []
    if article.article_name == '':
        error.append('Название статьи')
    if article.article_author == '':
        error.append('Автор')
    if article.article_collection == '':
        error.append('Библиография')
    if article.article_release == '':
        error.append('Выпуск и год')
    if article.article_pages == '':
        error.append('Страницы')
    if article.article_language == '':
        error.append('Язык')
    if article.article_keywords["0"] == []:
        error.append('Ключи')
    if not error:
        jats_data = normalize_article_to_jats(article, version)
        return HttpResponse(jats_data, content_type="application/xml")
    else:
        error_main_text = 'Некорректная запись метаданных, воспользуйтесь редактором метаданных!'
        # return HttpResponse("<script>location.href='/'; alert('Недостаточно данных, воспользуйтесь редактором метадынных!');</script>")
        return render(request, 'articles/error.html', {'main_text': error_main_text, 'errors': error})

