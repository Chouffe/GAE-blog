# A streamlined Django 1.4 and App Engine integration.

## Requirements

Google Appengine Python SDK 1.7.5+

## Getting started

Run locally:

    git clone git@github.com:potatolondon/djappengine.git
    cd djappengine
    ./serve.sh

Visit <http://localhost:8080> to marvel at your work.

Now deploy to appspot, first set up an app on <http://appengine.google.com> and replace `application` in `app.yaml` with the name of your app (in your text editor or like this):

    sed -i '' 's/djappeng1ne/myappid/' app.yaml

You're ready to deploy:

    appcfg.py update .

The Django app in `core` is there to get you started. Have a look around.

## Local shell

With your local server stopped, open a python shell and play with your local data:

    ./shell

## Running tests

    python manage.py test core
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.000s

djappengine uses a custom test runner that doesn't try to use a database. This is because djappengine is designed primarily to be used with 
[App Engine's models](https://developers.google.com/appengine/docs/python/datastore/datamodeling), and not with Django's ORM. If you're using
CloudSQL, comment out the [TEST_RUNNER](https://github.com/potatolondon/djappengine/blob/master/settings.py#L29) line in `settings.py`.

[core/tests.py](https://github.com/potatolondon/djappengine/blob/master/core/tests.py) is an example test that sets App Engine's 
[testbed](https://developers.google.com/appengine/docs/python/tools/localunittesting).

## So what's going on?

### app.yaml

- Sets up static resources
- Points all other paths to the WSGI app

### main.py

- Sets the `DJANGO_SETTINGS_MODULE` environment var
- Routes logging for production
- Defines the WSGI app

### manage.py

- Uses path-fixing mechanisms in order for tests to run properly

### settings.py

- Usual Django defaults
- Sets the `SESSION_ENGINE` to a custom memcache/datastore session backend

### lib/environ.py

- Uses various internal SDK functions to set up the system environment in such a way that things will run in the context of Appengine's service stubs

### lib/memcache.py

- So App Engine's memcache is seen by django

### lib/testrunnernodb.py

- A custom test runner that lets you use Django's simple test runner to run tests with [App Engine's testbed](https://developers.google.com/appengine/docs/python/tools/localunittesting) and without a database.

### core

- A simple example app to get you started


## What's missing

Something missing? [please raise an issue](https://github.com/potatolondon/djappengine/issues?state=open).
