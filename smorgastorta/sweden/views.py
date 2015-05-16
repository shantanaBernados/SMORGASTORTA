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

import json
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


class SignUpView(generic.TemplateView):
    template_name = "sweden/signup.html"

    def get_context_data(self, **kwargs):
        context = {
            'signupform': SignUpForm()
        }
        return context


class HomeView(generic.TemplateView):
    template_name = "sweden/home.html"


class VerifyLogin(generic.View):

    def post(self, request, *args, **kwargs):
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )

        if user:
            login(request, user)
        else:
            return HttpResponse(
                json.dumps({"success": False, "error": "Username or password is incorrect."})
            )

        return HttpResponse(
            json.dumps({"success": True})
        )


class VerifySignUp(generic.View):

    def post(self, request, *args, **kwargs):
        user_form = SignUpForm(request.POST)
        if user_form.is_valid():
            username = user_form.clean_username()
            password = user_form.clean_password2()
            user_form.save()
            user = authenticate(username=username,
                                password=password)
            login(request, user)
            if request.is_ajax():
                return HttpResponse('{"success": true}')
        else:
            s = "Error:\n"

            for keys in user_form.error_messages:
                s += user_form.error_messages[keys] + "\n"

            if request.is_ajax():
                return HttpResponse(
                    json.dumps({"success": "false", "error": user_form.errors})
                )

        return HttpResponse('{"success": true}')


class LogoutUser(generic.View):

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class ProfileView(generic.TemplateView):
    template_name = "sweden/profile.html"


class QuizView(generic.TemplateView):
    template_name = "sweden/quiz.html"