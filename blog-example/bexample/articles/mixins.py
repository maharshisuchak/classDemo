from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from .models import Article

class NameFilterMixin(object):
	queryset = Article.objects.filter(title="m")

class AuthRequireMixin(object):
	""" 
	Require that a user is authenticated. If user is not authenticated 
	than send them to login page
	"""
	# login_url = settings.LOGIN_URL
	def dispatch(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return redirect_to_login(request.get_full_path(), settings.LOGIN_URL)
		return super(AuthRequireMixin, self).dispatch(request, *args, **kwargs)

class UserAuthorMixin(AuthRequireMixin):
	""" Check if the user is the author of the article. If no than return 403 """
	def dispatch(self,request,*args,**kwargs):
		if request.user.is_authenticated and request.user.id is not self.get_object().author.id:
			raise PermissionDenied
		return super(UserAuthorMixin, self).dispatch(request, *args, **kwargs)