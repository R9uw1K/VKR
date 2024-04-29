from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.articles),
    path('<int:article_id>/', views.article, name='article'),

    path('export/rdf/<int:article_id>/', views.rdf_export_by_id, name='rdf_export_by_id'),
    path('export/xml/<int:article_id>/', views.xml_export_by_id, name='xml_export_by_id'),
    path('export/json/<int:article_id>/', views.json_export_by_id, name='json_export_by_id'),
    path('export/yaml/<int:article_id>/', views.yaml_export_by_id, name='yaml_export_by_id'),

    path('normalize/dublincore/<int:article_id>/', views.dublincore_export_by_id, name='dublincore_export_by_id'),
    path('normalize/jats/<int:article_id>/', views.jats_export_by_id, name='jats_export_by_id')
]
