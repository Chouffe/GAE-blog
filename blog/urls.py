from django.conf.urls import patterns, url
from blog import views

urlpatterns = patterns(
    '',
    url(r'^$', views.home, {}, name='home'),
    url(r'^login/$', views.login, {}, name='login'),
    url(r'^logout/$', views.logout, {}, name='logout'),
    url(r'^signin/$', views.signin, {}, name='signin'),
    # API
    url(r'^article/create/$',
        views.create_article, {},
        name="article_create"),
    url(r'^article/delete/(?P<id>\d+)/$',
        views.delete_article,
        name="article_delete"),
    url(r'^article/update/(?P<id>\d+)/$',
        views.update_article,
        name="article_update"),
)
