from django.shortcuts import render
from django.views import generic

from sweden.forms import *

class IndexView(generic.View):

    def dispatch(self, request, *args, **kwargs):
        handler_class = None

        if request.user.is_authenticated():
            handler_class = HomeView(request=request)
        else:
            handler_class = WelcomeView(request=request)

        if request.method.lower() in handler_class.http_method_names:
            handler = getattr(handler_class, request.method.lower(),
                              handler_class.http_method_not_allowed)
        else:
            handler = handler_class.http_method_not_allowed
        return handler(request, *args, **kwargs)


class WelcomeView(generic.TemplateView):
    template_name = "sweden/welcome.html"


class LoginView(generic.TemplateView):
    template_name = "sweden/login.html"

    def get_context_data(self, **kwargs):
        context = {
            'loginform': LoginForm()
        }
        return context


class HomeView(generic.TemplateView):
    template_name = "facebook/home.html"

    def get_context_data(self, **kwargs):
        posts = Post.objects.order_by('datetime').reverse()

        context = {
            'postform': PostForm(),
            'posts': posts,
        }
        return context
