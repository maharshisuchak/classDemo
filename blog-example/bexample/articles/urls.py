from django.conf.urls import url
from django.views.generic.dates import (
    ArchiveIndexView,
    MonthArchiveView
    )
from .models import Article
from .views import BlogHomeListView, ArticleDetailView, ArticleCreateView, \
                   ArticleDeleteView, ArticleUpdateView, MyView, \
                   TemplateViewDemo, RedirectViewDemo, ArticleYearArchiveView, \
                   ArticleMonthArchiveView
urlpatterns = [
    url(r'^$', BlogHomeListView.as_view(), name="blog-home"),
    url(r'^(?P<pk>\d+)/$', ArticleDetailView.as_view(), name="article-detail"),
    url(r'^myview/$',MyView.as_view(), name='my-view'),
    
    # TemplateView
    url(r'^showtemplate/$', TemplateViewDemo.as_view(), name='TemplateViewDemo'),
    
    url(r'^create/$', ArticleCreateView.as_view(), name="article-create"),
    url(r'^delete/(?P<pk>\d+)/$', ArticleDeleteView.as_view(), name="article-delete"),
    url(r'^update/(?P<pk>\d+)/$', ArticleUpdateView.as_view(), name="article-update"),
    url(r'^redirect/$', RedirectViewDemo.as_view(url='http://www.smartsensesolutions.com'), 
    	name='redirect'),
    # url(r'^redirect/(?P<path>.*)$', RedirectViewDemo.as_view(url='/new_path/%(path)s')),
    url(r'^archive/$', ArchiveIndexView.as_view(model=Article, date_field="created",
        allow_future=True), 
        name="article_archive"),
    url(r'^yearly/(?P<year>[0-9]{4})/$', ArticleYearArchiveView.as_view(), name="article_year_archive"),
    # Example: /2012/aug/
    url(r'^(?P<year>[0-9]{4})/(?P<month>[-\w]+)/$', ArticleMonthArchiveView.as_view(), 
        name="archive_month"),

    # Example: /2012/08/
    # url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]+)/$', ArticleMonthArchiveView.as_view(month_format='%m'), 
        # name="archive_month_numeric"),
]
