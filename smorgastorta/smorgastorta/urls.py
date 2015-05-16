from django.conf.urls import patterns, include, url
from django.contrib import admin


from sweden import views 


admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'smorgastorta.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^login/', views.LoginView.as_view(), name='login'),
    url(r'^signup/', views.SignUpView.as_view(), name='signup'),
    url(r'^verifyLogin$', views.VerifyLogin.as_view(), name='verifyLogin'),
    url(r'^verifySignUp$', views.VerifySignUp.as_view(), name='verifySignUp'),
    url(r'^logout$', views.LogoutUser.as_view(), name='logout'),
    url(r'^profile$', views.ProfileView.as_view(), name='profile'),
    url(r'^quiz$', views.QuizView.as_view(), name='quiz'),
)
