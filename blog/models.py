from google.appengine.ext import db

class User(db.Model):

    username = db.StringProperty()
    password = db.StringProperty()


class Article(db.Model):

    title = db.StringProperty()
    created_on = db.DateTimeProperty(auto_now_add = 1)
    author = db.StringProperty()
    reference = db.ReferenceProperty(User)

    def __str__(self):
        return '%s' %self.title

    def get_absolute_url(self):
        return '/article/%s/' % self.key()

    def __unicode__(self):
        return title


