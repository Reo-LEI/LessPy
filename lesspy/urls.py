from django.conf.urls import url, include

from . import views


app_name = 'lesspy'
urlpatterns = [
    url(r'^$', views.index, name='index'),

    # /pythonlib/
    url(r'^pythonlib/$', include([
        url(r'^$', views.lib_list, name='lib_list'),
        url(r'^add/$', views.lib_add, name='lib_add'),

        url(r'^(?P<lib_name>\w*)/$', include([

            # /pythonlib/<lib_name>/ -> lib level operation
            url(r'^del/$', views.lib_del, name='lib_del'),
            url(r'^edit/$', views.lib_edit, name='lib_edit'),
            url(r'^request/$', views.lib_request, name='lib_request'),

            # /pythonlib/<lib_name>/ -> func level
            url(r'^$', views.func_list, name='func_list'),  # library detail
            url(r'^add/$', views.func_add, name='func_add'),

            # /pythonlib/<lib_name>/<func_name>/ -> func level operation
            url(r'^(?P<func_name>\w*)/$', include([
                url(r'^$', views.func, name='func'),  # function detail
                url(r'^del/$', views.func_del, name='func_del'),
                url(r'^edit/$', views.func_edit, name='func_edit'),
                url(r'^request/$', views.func_request, name='func_request')
            ]))
        ]))
    ])),

    # /lesscode/
    url(r'^lesscode/$', include([
        url(r'^$', views.topic_list, name='topic_list'),
        url(r'^add/$', views.topic_add, name='topic_add'),

        url(r'^(?P<topic_name>\w*)/$', include([

            # /lesscode/<topic_name>/ -> topic level operation
            url(r'^del/$', views.topic_del, name='topic_del'),
            url(r'^edit/$', views.topic_edit, name='topic_edit'),
            url(r'^request/$', views.topic_request, name='topic_request'),

            # /lesscode/<topic_name>/ -> skill level
            url(r'^$', views.skill_list, name='skill_list'),  # topic detail
            url(r'^add/$', views.skill_add, name='skill_add'),

            # /lesscode/<topic_name>/<skill_name> -> skill level operation
            url(r'^(?P<skill_name>\w*)/$', include([
                url(r'^$', views.skill, name='skill'),  # skill detail
                url(r'^del/$', views.skill_del, name='skill_del'),
                url(r'^edit/$', views.skill_edit, name='skill_del'),
                url(r'^request/$', views.skill_request, name='skill_request')
            ]))
        ]))
    ])),

    # auth
    url(r'^', include('django.contrib.auth.urls'))
]
