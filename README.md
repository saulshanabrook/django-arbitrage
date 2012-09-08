#django-arbitrage
Project to exploit the inefficiencies in online prediction markets.
###Branching
Branching model is partly adapted from [nvie](http://nvie.com/posts/a-successful-git-branching-model/)
##Install in Dev Environment
1. _Optional, but recommended:_ Install [`virtualenvwrapper`](http://www.doughellmann.com/docs/virtualenvwrapper/) and create a virtualenv for `django-arbitrage`.
2. Clone repo
3. `pip install -r requirements/dev.txt`
4. _Optional:_ Run tests: `./manage.py test`
5. Collect admin files: `./manage.py collectstatic`
6. Sync database (sqlite for development): `./manage.py sycndb`
7. Apply South migrations: `./manage.py migrate`
8. _Optional:_ Run local server: `./manage.py runserver`
##Install on Heroku
    heroku addons:add newrelic:standard
    heroku addons:add memcachier:dev
    heroku addons:add heroku-postgresql:dev
    heroku config:add DJANGO_SETTINGS_MODULE=arbitrage.settings.prod SECRET_KEY=$SECRET_KEY
    heroku pg:promote *db_name*
    heroku run './manage.py syncdb --noinput ; ./manage.py migrate'
