from google.appengine.ext import db


class User(db.Model):

    username = db.StringProperty()
    password = db.StringProperty()

    def __unicode__(self):
        return self.username


class Article(db.Model):

    title = db.StringProperty()
    content = db.TextProperty()
    created_on = db.DateTimeProperty(auto_now_add=1)
    author = db.StringProperty(User)

    def __str__(self):
        return '%s' % self.title

    def __unicode__(self):
        return self.title
