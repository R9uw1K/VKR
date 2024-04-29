from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from .models import Article
import rdflib
import json
import yaml
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom


def articles(request):
    all_articles = Article.objects.filter()
    return render(request, 'articles/articles.html', {'articles': all_articles})


def article(request, article_id):
    article = Article.objects.filter(id=article_id)[0]
    print(article.article_release)
    return render(request, 'articles/article.html', {'article': article})


# Функция экспорта одной статьи в Dublin Core формате


def export_article_to_dublin_core(article):
    graph = rdflib.Graph()
    article_uri = rdflib.URIRef(f"http://127.0.0.1:8000/{article.id}")
    graph.add((article_uri, rdflib.RDF.type, rdflib.FOAF.Document))
    graph.add((article_uri, rdflib.DCTERMS.title, rdflib.Literal(article.article_name)))
    graph.add((article_uri, rdflib.DCTERMS.creator, rdflib.Literal(article.article_author)))
    graph.add((article_uri, rdflib.DCTERMS.source, rdflib.Literal(article.article_collection)))
    graph.add((article_uri, rdflib.DCTERMS.date, rdflib.Literal(article.article_release)))
    graph.add((article_uri, rdflib.DCTERMS.coverage, rdflib.Literal(article.article_pages)))
    graph.add((article_uri, rdflib.DCTERMS.language, rdflib.Literal(article.article_language)))
    return graph.serialize(format='xml')


# Функция экспорта одной статьи в JATS формате
def export_article_to_jats(article):
    article_elem = Element("article")
    SubElement(article_elem, "article_name").text = article.article_name
    SubElement(article_elem, "article_author").text = article.article_author
    SubElement(article_elem, "article_collection").text = article.article_collection
    SubElement(article_elem, "article_release").text = article.article_release
    SubElement(article_elem, "article_pages").text = article.article_pages
    SubElement(article_elem, "article_language").text = article.article_language
    SubElement(article_elem, "kwd-group").text = str(article.article_keywords["0"])
    return minidom.parseString(tostring(article_elem)).toprettyxml()


# Функция экспорта одной статьи в RDF формате
def export_article_to_rdf(article):
    graph = rdflib.Graph()
    article_uri = rdflib.URIRef(f"http://127.0.0.1:8000/{article.id}")
    graph.add((article_uri, rdflib.RDF.type, rdflib.FOAF.Document))
    graph.add((article_uri, rdflib.DCTERMS.title, rdflib.Literal(article.article_name)))
    graph.add((article_uri, rdflib.DCTERMS.creator, rdflib.Literal(article.article_author)))
    graph.add((article_uri, rdflib.DCTERMS.source, rdflib.Literal(article.article_collection)))
    graph.add((article_uri, rdflib.DCTERMS.date, rdflib.Literal(article.article_release)))
    graph.add((article_uri, rdflib.DCTERMS.coverage, rdflib.Literal(article.article_pages)))
    graph.add((article_uri, rdflib.DCTERMS.language, rdflib.Literal(article.article_language)))
    graph.add((article_uri, rdflib.DCTERMS.description, rdflib.Literal(article.article_keywords)))
    return graph.serialize(format='xml')


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
    return HttpResponse(rdf_data, content_type="rdf+xml")


# Django endpoint для экспорта статьи по её идентификатору в XML
@csrf_exempt
def xml_export_by_id(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404("Статья не найдена")
    xml_data = export_article_to_xml(article)
    return HttpResponse(xml_data, content_type="application/xml")


# Django endpoint для экспорта статьи по её идентификатору в JSON
@csrf_exempt
def json_export_by_id(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404("Статья не найдена")
    json_data = export_article_to_json(article)
    return JsonResponse(json_data, safe=False)


# Django endpoint для экспорта статьи по её идентификатору в YAML
@csrf_exempt
def yaml_export_by_id(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404("Статья не найдена")
    yaml_data = export_article_to_yaml(article)
    return HttpResponse(yaml_data, content_type="text/yaml")


@csrf_exempt
def dublincore_export_by_id(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404("Статья не найдена")
    if article.article_keywords["0"] != []:
        dublincore_data = export_article_to_dublin_core(article)
        return HttpResponse(dublincore_data, content_type="rdf+xml")
    else:
        return HttpResponse("<script>location.href='/'; alert('Недостаточно данных, воспользуйтесь редактором метадынных!');</script>")
#

@csrf_exempt
def jats_export_by_id(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404("Статья не найдена")
    if article.article_keywords["0"] != []:
        jats_data = export_article_to_jats(article)
        return HttpResponse(jats_data, content_type="application/xml")
    else:
        return HttpResponse("<script>location.href='/'; alert('Недостаточно данных, воспользуйтесь редактором метадынных!');</script>")
