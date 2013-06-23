from django.core.urlresolvers import reverse
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from google.appengine.api import users
from django.views.generic import TemplateView
from blog.models import Article, User
from blog.forms import SignInUserForm, LogInUserForm, ArticleForm
from django.views.generic import CreateView
import hashlib


def home(request):
    articles = Article.all()
    return render(request, 'home.html', locals())


def about(request):
    return render(request, 'about.html', locals())


def contact(request):
    return render(request, 'contact.html', locals())


def login(request):
    """Login View enabling login into the blog"""

    if request.method == 'POST':
        form = LogInUserForm(request.POST)

        if form.is_valid():
            user = User.gql("WHERE username = :username", username=form.cleaned_data['username']).fetch(1)
            request.session['user'] = user[0]
            messages.add_message(request, messages.INFO, u'You are signed in')
            return redirect('home')
    else:
        form = LogInUserForm()

    return render(request, 'login.html', locals())


def logout(request):
    """Logout View enabling logout"""

    del(request.session['user'])
    messages.add_message(request, messages.INFO, u'Session destroyed - Logout')
    return redirect('home')


def signin(request):
    """Signin Page enabling signin and new users to create an account"""

    if request.method == 'POST':
        form = SignInUserForm(request.POST)

        if form.is_valid():
            # Hash the Password using md5
            m = hashlib.md5()
            m.update(form.cleaned_data['password'])
            # Create the user
            user = User(username=form.cleaned_data['username'], password=m.hexdigest())
            user.put()
            messages.add_message(request, messages.INFO, u'You are signed in. Please Log in now.')
            return redirect('home')

    else:
        form = SignInUserForm()

    return render(request, 'signin.html', locals())


def create_article(request):

    if request.method == 'POST':
        form = ArticleForm(request.POST)

        if form.is_valid():
            article = Article(title=form.cleaned_data['title'],
                              content=form.cleaned_data['content'],
                              author=request.session['user'].username)
            article.put()
            messages.add_message(request, messages.INFO, u'Article %s created' % form.cleaned_data['title'])

            return redirect('home')

    else:
        form = ArticleForm()

    return render(request, 'article/create.html', locals())


def delete_article(request, id):
    article = Article.get_by_id(int(id))
    if article:
        messages.add_message(request, messages.INFO, u'Article %s deleted' % article.title)
        article.delete()
    else:
        messages.add_message(request, messages.ERROR, u'Article not found')
    return redirect('home')


def update_article(request, id):

    article = Article.get_by_id(int(id))

    if article:
        if request.method == 'POST':
            form = ArticleForm(request.POST)

            if form.is_valid():
                article.title = form.cleaned_data['title']
                article.content = form.cleaned_data['content']
                article.put()
                messages.add_message(request, messages.INFO, u'Article %s created' % form.cleaned_data['title'])

                return redirect('home')

        else:

            form = ArticleForm({ 'title': article.title, 'content': article.content })

        return render(request, 'article/create.html', locals())
    else:
        messages.add_message(request, messages.ERROR, u'Article not found')
        return redirect('home')
