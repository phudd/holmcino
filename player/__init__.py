from django.shortcuts import redirect
from django.core.urlresolvers import reverse

def require_player_login(redirurl=None):
	def decoratorWrapper(func):
		def decorator(request, *args, **kwargs):
			if request.session.get('player') == None:
				if redirurl == None:
					redirurl = reverse('player_login')
				return redirect(redirurl)
			else:
				return func(request, *args, **kwargs)
		return decorator
	return decoratorWrapper
