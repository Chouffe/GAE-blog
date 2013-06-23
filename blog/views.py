from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.shortcuts import render
from google.appengine.api import users
from django.views.generic import TemplateView
from blog.models import Article, User
from blog.forms import UserForm
import hashlib


class Home(TemplateView):
    template_name = "home.html"


class About(TemplateView):
    template_name = "about.html"


class Contact(TemplateView):
    template_name = "contact.html"


def login(request):
    # me = User(username="chouffe", password="test")
    # me.put()
    users = User.all()
    return render(request, 'login.html', locals())


def signin(request):

    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            m = hashlib.md5()
            m.update(form.cleaned_data['password'])
            user = User(username=form.cleaned_data['username'], password=m.hexdigest())
            user.put()
            pass

    else:
        form = UserForm()

    return render(request, 'signin.html', locals())
