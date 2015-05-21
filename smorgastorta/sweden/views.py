import json
import datetime

from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from sweden.forms import SignUpForm
from sweden.models import HWQuestion, SleepQuestion, Assessment, User_HWQ_Assessment
from sweden.utilities import Thesis_Models

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


class ProfileView(generic.DetailView):
    model = User_HWQ_Assessment
    template_name = "sweden/profile.html"

    def get_object(self, **kwargs):
        return get_object_or_404(User, username=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        user_ass = User_HWQ_Assessment.objects.filter(user=self.object)
        context = {
            'user_ass': user_ass
        }
        return context


class QuizView(generic.TemplateView):
    template_name = "sweden/quiz.html"

    def get_context_data(self, **kwargs):
        message = User_HWQ_Assessment.objects.filter(user=self.request.user, date=datetime.datetime.today().date())
        
        context = {
            "message": message
        }

        return context

class AssessView(generic.View):
    def post(self, request):
        try:
            hwq = HWQuestion.objects.create(
                srh=float(request.POST.get('srh')),
                sleep=float(request.POST.get('sleep')),
                concentration=float(request.POST.get('concentration')),
                stress=float(request.POST.get('stress')),
                energy=float(request.POST.get('energy')),
                control=float(request.POST.get('control')),
                social=float(request.POST.get('social')),
                efficiency=float(request.POST.get('efficiency')),
                satisfaction=float(request.POST.get('work_joy')),
                work_load=float(request.POST.get('work_load')),
                atmosphere=float(request.POST.get('work_atm'))
            )
            
            sleepq = SleepQuestion.objects.create(
                sleep_1=int(request.POST.get('sleep1')),
                sleep_2=int(request.POST.get('sleep2')),
                sleep_3=int(request.POST.get('sleep3')),
                sleep_4=int(request.POST.get('sleep4')),
                sleep_5=int(request.POST.get('sleep5'))
            )

            hwq.save()  
            sleepq.save()

            hw11 = [
                float(request.POST.get('srh')),
                float(request.POST.get('sleep')),
                float(request.POST.get('concentration')),
                float(request.POST.get('stress')),
                float(request.POST.get('energy')),
                float(request.POST.get('control')),
                float(request.POST.get('social')),
                float(request.POST.get('efficiency')),
                float(request.POST.get('work_joy')),
                float(request.POST.get('work_load')),
                float(request.POST.get('work_atm'))
            ]

            sleep = [
                int(request.POST.get('sleep1')),
                int(request.POST.get('sleep2')),
                int(request.POST.get('sleep3')),
                int(request.POST.get('sleep4')),
                int(request.POST.get('sleep5'))
            ]

            models = Thesis_Models()

            marc = models.assess_sickness_absence(hw11)
            tamps = models.diagnose_sleep_problem(hw11, sleep)
            ber = models.predict_srh(hw11)

            assessments = Assessment.objects.create(
                sick_leave=marc,
                sleep=tamps,
                srh=ber
            )

            assessments.save()

            final = User_HWQ_Assessment.objects.create(
                user=request.user,
                hwQ=hwq,
                sleepQ=sleepq,
                ass=assessments
            )

            final.save()

            return HttpResponseRedirect('results')

        except:
            return HttpResponseBadRequest("INVALID INPUT")


class ResultsView(generic.TemplateView):
    template_name = 'sweden/results.html'

    def get_context_data(self, **kwargs):
        results = User_HWQ_Assessment.objects.get(user=self.request.user, date=datetime.datetime.today().date())
        context = {
            'marc': results.ass.sick_leave,
            'tamps': results.ass.sleep,
            'ber': results.ass.srh
        }

        return context





