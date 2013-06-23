from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render
from blog.models import Article, User
from blog.forms import SignInUserForm, LogInUserForm, ArticleForm
import time
import hashlib


def home(request):
    """Home Page: displaying the last articles"""
    articles = Article.all().order('-created_on').fetch(10)
    return render(request, 'home.html', locals())


def login(request):
    """Login View enabling login into the blog"""

    if request.method == 'POST':
        form = LogInUserForm(request.POST)

        if form.is_valid():
            user = User.gql("WHERE username = :username",
                            username=form.cleaned_data['username']).fetch(1)
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
            user = User(username=form.cleaned_data['username'],
                        password=m.hexdigest())
            user.put()
            messages.add_message(request, messages.INFO,
                                 u'You are signed in. Please Log in now.')
            return redirect('home')

    else:
        form = SignInUserForm()

    return render(request, 'signin.html', locals())


def create_article(request):
    """Enables Article creation"""

    if request.method == 'POST':
        form = ArticleForm(request.POST)

        if form.is_valid():
            article = Article(title=form.cleaned_data['title'],
                              content=form.cleaned_data['content'],
                              author=request.session['user'].username)
            article.put()
            messages.add_message(request,
                                 messages.INFO,
                                 u'Article %s created' %
                                 form.cleaned_data['title'])
            time.sleep(1)

            return redirect('home')

    else:
        form = ArticleForm()

    return render(request, 'article/create.html', locals())


def delete_article(request, id):
    """Enables Article deletion"""

    article = Article.get_by_id(int(id))
    if article:
        messages.add_message(request,
                             messages.INFO,
                             u'Article %s deleted' % article.title)
        article.delete()
        time.sleep(1)
    else:
        messages.add_message(request, messages.ERROR, u'Article not found')
    return redirect('home')


def update_article(request, id):
    """Enables Article update"""

    article = Article.get_by_id(int(id))

    if article:
        if request.method == 'POST':
            form = ArticleForm(request.POST)

            if form.is_valid():
                article.title = form.cleaned_data['title']
                article.content = form.cleaned_data['content']
                article.put()
                messages.add_message(request,
                                     messages.INFO,
                                     u'Article %s created'
                                     % form.cleaned_data['title'])

                time.sleep(1)

                return redirect('home')

        else:

            form = ArticleForm({'title': article.title,
                                'content': article.content})

        return render(request, 'article/create.html', locals())
    else:
        messages.add_message(request,
                             messages.ERROR,
                             u'Article not found')
        return redirect('home')
