from django.conf.urls import patterns, url, include
from blog import views

urlpatterns = patterns(
    '',
    url(r'^$', views.Home.as_view(), {}, name='home'),
    url(r'^contact/$', views.Contact.as_view(), {}, name='contact'),
    url(r'^about/$', views.About.as_view(), {}, name='about'),
    url(r'^login/$', views.login, {}, name='login'),
    url(r'^signin/$', views.signin, {}, name='signin'),
)
