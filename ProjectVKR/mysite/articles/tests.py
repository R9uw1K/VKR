from django.test import TestCase
from .models import Article
from .views import export_article_to_rdf, export_article_to_json, export_article_to_xml, export_article_to_yaml, normalize_article_to_jats, normalize_article_to_dublin_core, normalize_article_to_eudml
from xml.etree.ElementTree import Element, tostring
from locust import HttpUser, TaskSet, task,  between

class ArticleExport(TestCase):
    def setUp(self):
        self.article = Article.objects.create(
            article_name="Test",
            article_author="author",
            article_collection='collection',
            article_release='release',
            article_pages = 'pages',
            article_language = 'language',
            article_path = 'path',
            article_keywords = {"0": []},
            article_annotation = 'annotation',
            article_issn = 'ISSN',
            article_science = 'science'
        )

    def test_export_rdf(self):
        rdf_data = export_article_to_rdf(self.article)
        self.assertIn(b'<rdf:RDF', rdf_data)
        self.assertIn(b'<dcterms:title xml:lang="ru">Test</dcterms:title>', rdf_data)

    def test_export_jats_1_0(self):
        jats_data = normalize_article_to_jats(self.article, '1.0')
        self.assertIn('<article version="1.0">', jats_data)
        self.assertIn('<article_name>Test</article_name>', jats_data)

    def test_export_jats_1_1(self):
        jats_data = normalize_article_to_jats(self.article, '1.1')
        self.assertIn('<article version="1.1">', jats_data)
        self.assertIn('<article_collection>collection</article_collection>', jats_data)

    def test_export_eudml(self):
        eudml_data = normalize_article_to_eudml(self.article)
        self.assertIn('<eudml>', eudml_data)
        self.assertIn('<title>Test</title>', eudml_data)

    def test_export_dublin_core(self):
        dc_data = normalize_article_to_dublin_core(self.article)
        self.assertIn(b'<dcterms:title>Test</dcterms:title>', dc_data)
        self.assertIn(b'<dcterms:date>release</dcterms:date>', dc_data)

