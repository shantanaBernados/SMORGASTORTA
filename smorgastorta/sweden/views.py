import json

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from sweden.forms import SignUpForm

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


class SignUpView(generic.edit.CreateView):
    template_name = "sweden/signup.html"
    form_class = SignUpForm
    success_url = '/login'


class HomeView(generic.TemplateView):
    template_name = "sweden/home.html"


class ProfileView(generic.TemplateView):
    template_name = "sweden/profile.html"


class QuizView(generic.TemplateView):
    template_name = "sweden/quiz.html"