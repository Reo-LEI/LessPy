from django.conf.urls import url, include

from . import views


app_name = 'lesspy'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^pythonlib/$', include([
        url(r'^$', views.lib_list, name='lib_list'),
        url(r'^add/$', views.lib_add, name='lib_add'),
        url(r'^(?P<lib_name>\w*)/del/$', views.lib_del, name='lib_del'),
        url(r'^(?P<lib_name>\w*)/edit/$', views.lib_edit, name='lib_edit'),
        url(r'^(?P<lib_name>\w*)/request/$', views.lib_request, name='lib_request'),
        url(r'^(?P<lib_name>\w*)/$', include([
            url(r'^$', views.func_list, name='func_list'),
            url(r'^add/$', views.func_add, name='func_add'),
            url(r'^(?P<func_name>\w*)/$', views.func, name='func'),
            url(r'^(?P<func_name>\w*)/del/$', views.func_del, name='func_del'),
            url(r'^(?P<func_name>\w*)/edit/$', views.func_edit, name='func_edit'),
            url(r'^(?P<func_name>\w*)/request/$', views.func_request, name='func_request')
        ])),
    ])),
    url(r'^lesscode/$', include([

    ])),
    url(r'^', include('django.contrib.auth.urls'))
]
