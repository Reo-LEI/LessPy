from django.conf.urls import url, include

from . import views


app_name = 'lesspy'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<url>pythonlib)/$', include([
        url(r'^$', views.display, name='lib'),
        url(r'^add/(?:(?P<id>\d*)/)?$', views.add, name='lib_add'),
        url(r'^edit/(?:(?P<id>\d*)/)?$', views.edit, name='lib_edit'),
        url(r'^issue/(?:(?P<id>\d*)/)?$', views.issue, name='lib_issue')
    ])),
    url(r'pythonlib/(?P<url>function)/', include([
        url(r'^$', views.display, name='func'),
        url(r'^add/(?:(?P<id>\d*)/)?$', views.add, name='func_add'),
        url(r'^edit/(?:(?P<id>\d*)/)?$', views.edit, name='func_edit'),
        url(r'^issue/(?:(?P<id>\d*)/)?$', views.issue, name='func_issue')
    ])),
    url(r'^(?P<url>lesscode)/$', include([
        url(r'^s', views.display, name='lesscode'),
        url(r'^add/(?:(?P<id>\d*)/)?$', views.add, name='lesscode_add'),
        url(r'^edit/(?:(?P<id>\d*)/)?$', views.edit, name='lesscode_edit'),
        url(r'^issue/(?:(?P<id>\d*)/)?$', views.issue, name='lesscode_issue')
    ])),
    url(r'^lesscode/(?P<url>skill)/$'), include([
        url(r'^$', views.display, name='skill'),
        url(r'^add/(?:(?P<id>\d*)/)?$', views.add, name='skill_add'),
        url(r'^edit/(?:(?P<id>\d*)/)?$', views.edit, name='skill_edit'),
        url(r'^issue/(?:(?P<id>\d*)/)?$', views.issue, name='skill_issue')
    ])
]
