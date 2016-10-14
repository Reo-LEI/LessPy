from django.conf.urls import url, include

from . import views


app_name = 'lesspy'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^python/$', include([
        url(r'^s', views.python, name='python')
    ]))
]
