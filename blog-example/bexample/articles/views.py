from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, Http404
from django.views.generic.dates import (
    YearArchiveView,
    MonthArchiveView
    )
from django.shortcuts import get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView,
    RedirectView,
    View,
    )
from .models import Article
from .forms import ArticleForm
from .mixins import (
    NameFilterMixin,
    UserAuthorMixin,
    AuthRequireMixin
    )
from django.views.generic.base import TemplateView
import logging

class MyView(View):
    def dispatch(self, request, *args, **kargs):
        if request.user.is_authenticated():
            return super(MyView, self).dispatch(request)
        else :
            raise Http404

    def get(self, request, *args, **kargs):
        return HttpResponse("Hello, World!")

# class BlogHomeListView(NameFilterMixin, ListView):
class BlogHomeListView(ListView):
    template_name = "articles/articles_home.html"
    # model = Article

    
    queryset = Article.objects.all() # == model = Article
    # queryset = Article.objects.filter(title="m")
    paginate_by = 10
    # paginate_orphans = 0 # Append defined number of objects on last page
    # page_kwarg = 'qqq'
    context_object_name = "p"
    # def get_context_data(self, **kwargs):
    #     context = super(BlogHomeListView, self).get_context_data(**kwargs)
    #     context['range'] = range(context['paginator'].num_pages)
    #     return context

    # def get_queryset(self):
    #     return Article.objects.filter(title='Raju')

class BlogHomeRedirectView(RedirectView):
    url = reverse_lazy('blog-home')

# class ArticleDetailView(NameFilterMixin, DetailView):
class ArticleDetailView(DetailView):
    template_name = "articles/article.html"
    model = Article
    # slug_field = 'title'

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['article_list'] = Article.objects.all()
        return context

class ArticleCreateView(AuthRequireMixin, CreateView):
    template_name = "articles/article_create.html"
    form_class = ArticleForm

    def form_valid(self, form):
        """
        Assign the author to the request.user
        """
        form.instance.author = self.request.user
        return super(ArticleCreateView, self).form_valid(form)


class ArticleDeleteView(UserAuthorMixin,DeleteView):
    model = Article
    success_url = reverse_lazy('blog-home')


class ArticleUpdateView(UserAuthorMixin, UpdateView):
    # http_method_names = ['post'] # Gives 405 error
    # http_method_names
    
    template_name = "articles/article_update.html"
    model = Article
    form_class = ArticleForm
    # fields=[]
    # http_method_names = ['get']

    # def get(self, request, *args, **kwargs):
    #     return HttpResponse("Hello, World!")

    # def http_method_not_allowed(self, request, *args, **kwargs):
    #     return HttpResponse("Method not found")

    #     # logger.warning('Method Not Allowed (%s) : %s', request.method, request.path,
    #     #     extra = {
    #     #         'status_code' : 405,
    #     #         'request' : request
    #     #     }
    #     # )
    #     return http.HttpResponseNotAllowed(self._allowed_methods())

    # def options(self, request, *args, **kwargs):
    #     response = http.HttpResponse()
    #     response['Allow'] = ','.join(self._allowed_methods())
    #     response['Content-Length'] = '0'
    #     return response

class TemplateViewDemo(TemplateView):
    template_name = 'articles/artical_template_demo.html'

    # def get(self, request, *args, **kwargs):
    #     kwargs['greeting'] = '1Bonjour' # add a keyword
    #                                    # and value to the context
    #     return super(TemplateViewDemo, self).get(request,  # call get
    #                                            *args,    # method of
    #                                            **kwargs) # TemplateView
    #                                                      # class

    def get_context_data(self, **kwargs): # Will Be called first
        kwargs['name'] = '2Pinank Lakhani'
        # get_context_data is the method of contextmixin. So here we have over ride 
        # that method and edit context.
        context = super(TemplateViewDemo, self).get_context_data(**kwargs)
        context['title'] = 'Pinank'
        return context

class RedirectViewDemo(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'article-detail'

    # def get_redirect_url(self, *args, **kwargs):
    #     article = get_object_or_404(Article)
    #     # article.update_counter()
    #     return super(RedirectViewDemo, self).get_redirect_url(*args, **kwargs)

class ArticleYearArchiveView(YearArchiveView):
    template_name = 'articles/article_archive_year.html'
    queryset = Article.objects.all()
    date_field = "created"
    make_object_list = True
    allow_future = True

class ArticleMonthArchiveView(MonthArchiveView):
    print("ArticleMonthArchiveView---->")
    template_name = 'articles/article_archive_month.html'
    queryset = Article.objects.all()
    date_field = "created"
    allow_future = True