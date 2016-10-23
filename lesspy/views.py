from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.views.decorators.http import require_GET, require_POST,\
    require_safe ,require_http_methods
from django.core.paginator import Paginator

from .models import UserProfile, Text, TagList, Library, LibraryRequest, \
    Function, FunctionRequest, Topic, TopicRequest, Skill, SkillRequest
from .form import UserProfileForm,  TagListForm, LibraryForm,\
    LibraryRequestForm, FunctionForm, FunctionRequestForm, TopicForm, \
    TopicRequestForm, SkillForm, SkillRequestForm

from .. import envconfig
from ..tools import get_page


@require_safe
def index(request):
    usage = Text.objects.get(name='usage')
    topics = Topic.objects.all()
    return render(request, 'lesspy/index.html', {'topics': topics,
                                                 'usage': usage})


@require_safe
def display(request, url):
    """ display the data from database """
    # dispatch model by 'url' mark captured by url
    models = {
        'pythonlib': Library,
        'function': Function,
        'lesscode': Topic,
        'skill': Skill
    }
    model = models[url]
    data = model.objects.all()
    paginator = Paginator(data, envconfig.pagination[url])
    page = request.GET.get('page')
    items = get_page(paginator, page)
    return render(request, 'lesspy/display', {'url': url, 'items': items})
