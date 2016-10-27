from django.shortcuts import render, redirect, get_object_or_404
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
                lib = Library.objects.create(
                    name=name,
                    description=description,
                    creator=request.user.userprofile
                )
                messages.success(request, 'Create library successfully')
                return redirect('lesspy:func_list', lib_name=lib.name)
    return render(request, 'lesspy/lib_add.html', context={'form': form})


# TODO permission require
@require_http_methods(['GET', 'POST'])
@login_required
def lib_del(request, lib_name):
    messages.warning(request, 'You want to delete {0}'.format(lib_name))
    if request.method == 'POST':
        lib = get_object_or_404(Library, name=lib_name)
        lib.hide()
        messages.success(request, 'Delete succeed')
        # TODO send msg to supervisor to note
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
                messages.success(request, 'Update succeed')
                return redirect('lesspy:func_list', lib_name=lib.name)
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
            LibraryRequest.objects.create(
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


@require_safe
def func_list(request, lib_name):
    function = Function.objects.filter(library__name=lib_name).order_by('name')
    paginator = Paginator(function, env.pagination['func'])
    page = request.GET.get('page')
    items = get_page(paginator, page)
    return render(request, 'lesspy/func_list.html', {'items': items})


# TODO permission require
@require_http_methods(['GET', 'POST'])
@login_required
def func_add(request, lib_name):
    form = FunctionForm()
    if request.method == 'POST':
        form = FunctionForm(request.POST)
        if form.is_valid():
            lib = get_object_or_404(Library, name=lib_name)
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            example = form.cleaned_data['example']
            instance = form.cleaned_data['instance']
            tag_id = form.cleaned_data['tag']
            tag = get_object_or_404(TagList, id=tag_id)
            creator = request.user.userprofile
            if Function.objects.filter(name=name).exists():
                messages.ERROR(request, 'This function has been exists')
            else:
                f = Function.objects.create(
                    library=lib,
                    name=name,
                    description=description,
                    example=example,
                    instance=instance,
                    tag=tag,
                    creator=creator
                )
                messages.success(request, 'Create function succeed')
                return redirect('lesspy:func', func_name=f.name)
    return render(request, 'lesspy/func_add.html', {'form': form})


@require_safe
def func(request, lib_name, func_name):
    f = get_object_or_404(Function, name=func_name)
    return render(request, 'lesspy/func.html', {'func': f})


# TODO permission require
@require_http_methods(['GET', 'POST'])
@login_required
def func_del(request, lib_name, func_name):
    messages.warning(request, 'You want to delete {0}'.format(func_name))
    if request.method == 'POST':
        f = get_object_or_404(Function, name=func_name)
        f.hide()
        messages.success(request, 'Delete succeed')
        # TODO send msg to supervisor to note
        return redirect('lesspy:func_list', lib_name=lib_name)
    return redirect('lesspy:func', lib_name=lib_name, func_name=func_name)


# TODO permission require
@require_http_methods(['GET', 'POST'])
@login_required
def func_edit(request, lib_name, func_name):
    f = get_object_or_404(Function, name=func_name)
    form = FunctionForm(initial={
        'name': f.name,
        'description': f.description,
        'example': f.example,
        'instance': f.instance,
        'tag': f.tag.id
    })
    if request.method == 'POST':
        form = FunctionForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            example = form.cleaned_data['example']
            instance = form.cleaned_data['instance']
            tag_id = form.cleaned_data['tag']
            tag = get_object_or_404(TagList, id=tag_id)
            if Function.objects.exclude(name=func_name).filter(name=name).exists():
                messages.error(request, 'This function has been exists')
            else:
                f.name = name
                f.description = description
                f.example = example
                f.instance = instance
                f.tag = tag
                messages.success(request, 'Update succeed')
                return redirect('lesspy:func', lib_name=lib_name,
                                func_name=f.name)
    return render(request, 'lesspy/func_edit', {'form': form})


@require_http_methods(['GET', 'POST'])
@login_required
def func_request(request, lib_name, func_name):
    lib = get_object_or_404(Library, name=lib_name)
    f = get_object_or_404(Function, name=func_name)
    form = FunctionRequestForm(initial={'library': lib.id, 'function': f.id})
    if request.method == 'POST':
        form = FunctionRequestForm(request.POST)
        if form.is_valid():
            library_id = form.cleaned_data['library']
            library = get_object_or_404(Library, id=library_id)
            function_id = form.cleaned_data['function']
            function = get_object_or_404(Function, id=function_id)
            request_type = form.cleaned_data['request_type']
            subject = form.cleaned_data['subject']
            solution = form.cleaned_data['solution']
            note = form.cleaned_data['note']
            creator = request.user.userprofile
            if function.library.id != library_id:
                messages.error(request, 'This function is not belong to {0}'
                               .format(library.name))
            else:
                FunctionRequest.objects.create(
                    function=function,
                    request_type=request_type,
                    subject=subject,
                    solution=solution,
                    note=note,
                    creator=creator
                )
                # TODO send msg to manager, and pass request confirm
                messages.success(request,
                                 'Your message has been submit, the result'
                                 'will message to you after pass.')
                return redirect('lesspy:func', lib_name=function.library.name,
                                func_name=function.name)
    return render(request, 'lesspy/func_request.html', {'form': form})
