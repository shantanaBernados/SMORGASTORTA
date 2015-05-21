from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.views import login, logout

from sweden import views 


admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'smorgastorta.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^login/', login, {'template_name': 'sweden/login.html'}, name='login'),
    url(r'^signup/', views.SignUpView.as_view(), name='signup'),
    url(r'^logout$', logout, {'next_page': 'index'}, name='logout'),
    url(r'^profile/(?P<slug>[-\w]+)/$', views.ProfileView.as_view(), name='profile'),
    url(r'^quiz$', views.QuizView.as_view(), name='quiz'),
    url(r'^assess$', views.AssessView.as_view(), name='assess'),
    url(r'^results$', views.ResultsView.as_view(), name='results')
)
