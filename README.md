#django-arbitrage
Project to exploit the inefficiencies in online prediction markets.
###Branching
Branching model is partly adapted from [nvie](http://nvie.com/posts/a-successful-git-branching-model/)
##Install
1. _Optional, but recommended:_ Install [`virtualenvwrapper`](http://www.doughellmann.com/docs/virtualenvwrapper/) and create a virtualenv for `django-arbitrage`.
2. Clone repo
3. `pip install -r requirements.txt`
4. _Optional:_ Run tests: `./manage.py test`
5. Collect admin files: `./manage.py collectstatic`
6. Sync database (sqlite for development): `./manage.py sycndb`
7. Apply South migrations: `./manage.py migrate`
8. _Optional:_ Run local server: `./manage.py runserver`