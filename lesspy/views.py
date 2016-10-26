from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.views.decorators.http import require_GET, require_POST,\
    require_safe, require_http_methods
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

from .models import UserProfile, Text, TagList, Library, LibraryRequest, \
    Function, FunctionRequest, Topic, TopicRequest, Skill, SkillRequest
from .form import UserProfileForm,  TagListForm, LibraryForm,\
    LibraryRequestForm, FunctionForm, FunctionRequestForm, TopicForm, \
    TopicRequestForm, SkillForm, SkillRequestForm
from .. import envconfig as env
from ..tools import get_page


@require_safe
def index(request):
    usage = Text.objects.get(name='usage')
    topics = Topic.objects.all()
    return render(request, 'lesspy/index.html', {
        'topics': topics, 'usage': usage})


@require_safe
def lib_list(request):
    library = Library.objects.filter(visible=True).order_by('name')
    paginator = Paginator(library, env.pagination['lib'])
    page = request.GET.get('page')
    items = get_page(paginator, page)
    return render(request, 'lesspy/lib_list.html', {'items': items})


# TODO permission require
@require_http_methods(['GET', 'POST'])
@login_required
def lib_add(request):
    form = LibraryForm()
    if request.method == 'POST':
        form = LibraryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            if Library.objects.filter(name=name).exists():
                messages.error(request, 'This library has been exists')
            else:
                lib = Library.objects.create(name=name, description=description,
                                             creator=request.user.userprofile)
                messages.success(request, 'Create library successfully')
                return redirect('lesspy:func_list', lib_name=lib.name)
    return render(request, 'lesspy/lib_add.html', context={'form': form})


# TODO permission require
@require_http_methods(['GET', 'POST'])
@login_required
def lib_del(request, lib_name):
    lib = get_object_or_404(Library, name=lib_name)
    messages.warning(request, 'You want to delete {0}'.format(lib_name))
    if request.method == 'POST':
        lib.hide()
        messages.success(request, 'Delete succeed')
        return redirect('lesspy:lib_list')
    return redirect('lesspy:func_list')


# TODO permission require
@require_http_methods(['GET', 'POST'])
@login_required
def lib_edit(request, lib_name):
    lib = get_object_or_404(Library, visible=True, name=lib_name)
    form = LibraryForm(initial={
        'name': lib.name, 'description': lib.description})
    if request.method == 'POST':
        form = LibraryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            if Library.objects.exclude(name=lib_name).filter(name=name).exists():
                messages.error(request, 'This library has been exists')
            else:
                lib.name = name
                lib.description = description
                lib.save()
                messages.success(request,'Update succeed')
                return redirect('lesspy:func_list', lib_name=name)
    return render(request, 'lesspy/lib_edit.html', {'form': form})


@require_http_methods(['GET', 'POST'])
@login_required
def lib_request(request, lib_name):
    lib = get_object_or_404(Library, name=lib_name)
    form = LibraryRequestForm(initial={'library': lib.id})
    if request.method == 'POST':
        form = LibraryRequestForm(request.POST)
        if form.is_valid():
            lib_id = form.cleaned_data['library']
            library = get_object_or_404(Library, id=lib_id)
            request_type = form.cleaned_data['request_type']
            subject = form.cleaned_data['subject']
            solution = form.cleaned_data['solution']
            note = form.cleaned_data['note']
            creator = request.user.userprofile
            Library.objects.create(
                library=library,
                request_type=request_type,
                subject=subject,
                solution=solution,
                note=note,
                creator=creator
            )
            # TODO send msg to manager, and pass request confirm
            messages.success(request, 'Your message has been submit, the result'
                                      'will message to you after pass.')
            return redirect('lesspy:func_list', lib_name=library.name)
    return render(request, 'lesspy/lib_request.html', {'form': form})

