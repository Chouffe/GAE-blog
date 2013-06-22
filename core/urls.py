from django.conf.urls.defaults import *
from django.conf import settings
from core import views

urlpatterns = patterns(
    '',
    url(r'^$', views.HelloWorld.as_view(), {}, name='hello-world'),
    url(r'^__exception_test__/$', views.exception_test, {}),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^500/$', 'django.views.generic.simple.direct_to_template', {'template': '500.html'}),
        url(r'^404/$', 'django.views.generic.simple.direct_to_template', {'template': '404.html'}),
        )
