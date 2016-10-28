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


# TODO permission require(add)
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


# TODO permission require(del)
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


# TODO permission require(edit)
@require_http_methods(['GET', 'POST'])
@login_required
def lib_edit(request, lib_name):
    lib = get_object_or_404(Library, visible=True, name=lib_name)
    form = LibraryForm(initial={
        'name': lib.name,
        'description': lib.description
    })
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
    form = LibraryRequestForm(initial={
        'library': lib.id
    })
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
            # TODO send msg to manager, and pass request confirm(backlog +1)
            messages.success(request, 'Your message has been submit, the result'
                                      'will message to you after pass.')
            return redirect('lesspy:func_list', lib_name=library.name)
    return render(request, 'lesspy/lib_request.html', {'form': form})


@require_safe
def func_list(request, lib_name):
    functions = Function.objects.filter(library__name=lib_name).order_by('name')
    return render(request, 'lesspy/func_list.html', {'functions': functions})


# TODO permission require(add)
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


# TODO permission require(del)
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


# TODO permission require(edit)
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
                f.save()
                messages.success(request, 'Update succeed')
                return redirect('lesspy:func', lib_name=lib_name,
                                func_name=f.name)
    return render(request, 'lesspy/func_edit', {'form': form})


@require_http_methods(['GET', 'POST'])
@login_required
def func_request(request, lib_name, func_name):
    lib = get_object_or_404(Library, name=lib_name)
    f = get_object_or_404(Function, name=func_name)
    form = FunctionRequestForm(initial={
        'library': lib.id,
        'function': f.id
    })
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
                # TODO send msg to manager, and pass request confirm(backlog +1)
                messages.success(request,
                                 'Your message has been submit, the result'
                                 'will message to you after pass.')
                return redirect('lesspy:func', lib_name=function.library.name,
                                func_name=function.name)
    return render(request, 'lesspy/func_request.html', {'form': form})


@require_safe
def topic_list(request):
    topics = Topic.objects.filter(visible=True).order_by('name')
    return render(request, 'lesspy/topic_list.html', {'topics': topics})


# TODO permission require(add)
@require_http_methods(['GET', 'POST'])
@login_required
def topic_add(request):
    form = TopicForm()
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            creator = request.user.userprofile
            if Topic.objects.filter(title=title).exists():
                messages.error(request, 'This topic has been exists')
            else:
                topic = Topic.objects.create(
                    title=title,
                    description=description,
                    creator=creator
                )
                messages.success(request, 'Create topic succeed')
                return redirect('lesspy:skill_list', topic_name=topic.title)
    return render(request, 'lesspy/topic_add.html', {'form': form})


# TODO permission require(del)
@require_http_methods(['GET', 'POST'])
@login_required
def topic_del(request, topic_name):
    messages.warning(request, 'You want to delete {0}'.format(topic_name))
    if request.method == 'POST':
        topic = get_object_or_404(Topic, title=topic_name)
        topic.hide()
        messages.success(request, 'Delete succeed')
        return redirect('lesspy:topic_list')
    return redirect('lesspy:topic_del.html', topic_name=topic_name)


# TODO permission require(edit)
@require_http_methods(['GET', 'POST'])
@login_required
def topic_edit(request, topic_name):
    topic = get_object_or_404(Topic, title=topic_name)
    form = TopicForm(initial={
        'title': topic.name,
        'description': topic.description
    })
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            if Topic.objects.exclude(title=topic_name).filter(title=title).exists():
                messages.error(request, 'This topic has been exists')
            else:
                topic.title = title
                topic.description = description
                topic.save()
                messages.success(request, 'Update succeed')
                return redirect('lesspy:skill_list', topic_name=topic_name)
    return render(request, 'lesspy/topic_edit.html', {'form': form})


@require_http_methods(['GET', 'POST'])
@login_required
def topic_request(request, topic_name):
    topic = get_object_or_404(Topic, topic_name)
    form = TopicRequestForm(initial={
        'topic': topic.id
    })
    if request.method == 'POST':
        form = TopicRequestForm(request.POST)
        if form.is_valid():
            topic_id = form.cleaned_data['topic']
            topic = get_object_or_404(Topic, id=topic_id)
            request_type = form.cleaned_data['request_type']
            subject = form.cleaned_data['subject']
            solution = form.cleaned_data['solution']
            note = form.cleaned_data['note']
            creator = request.user.userprofile
            TopicRequest.objects.create(
                topic=topic,
                request_type=request_type,
                subject=subject,
                solution=solution,
                note=note,
                creator=creator
            )
            # TODO send msg to manager, and pass request confirm(backlog +1)
            messages.success(request, 'Your message has been submit, the result'
                                      'will message to you after pass.')
            return redirect('lesspy:skill_list', topic_name=topic.title)
    return render(request, 'lesspy/topic_request.html', {'form': form})


@require_safe
def skill_list(request, topic_name):
    topic = get_object_or_404(Topic, title=topic_name)
    return render(request, 'lesspy/skill_list.html', {'topic': topic})


# TODO permission require(add)
def skill_add(request, topic_name):
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            background = form.cleaned_data['background']
            solution = form.cleaned_data['solution']
            tag_id = form.cleaned_data['tag']
            tag = get_object_or_404(TagList, id=tag_id)
            creator = request.user.userprofile
            if Skill.objects.filter(title=title).exists():
                messages.error(request, 'This skill has been exists')
            else:
                s = Skill.objects.create(
                    title=title,
                    background=background,
                    solution=solution,
                    tag=tag,
                    creator=creator
                )
                messages.success(request, 'Create skill succeed')
                return redirect('lesspy:skill', topic_name=topic_name,
                                skill_name=s.title)
    return render(request, 'lesspy/skill_add.html', {'form': form})


@require_safe
def skill(request, topic_name, skill_name):
    s = get_object_or_404(Skill, title=skill_name)
    return render(request, 'lesspy/skill.html', {'skill': s})


# TODO permission require(del)
@require_http_methods(['GET', 'POST'])
@login_required
def skill_del(request, topic_name, skill_name):
    messages.warning(request, 'You want to delete {0}'.format(skill_name))
    if request.method == 'POST':
        s = get_object_or_404(Skill, title=skill_name)
        s.hide()
        messages.success(request, 'Delete succeed')
        return redirect('lesspy:skill_list', topic_name=topic_name)
    return redirect('lesspy:skill', topic_name=topic_name, skill_name=skill_name)


# TODO permission require(edit)
@require_http_methods(['GET', 'POST'])
@login_required
def skill_edit(request, topic_name, skill_name):
    s = get_object_or_404(Skill, title=skill_name)
    form = SkillForm(initial={
        'title': s.title,
        'background': s.background,
        'solution': s.solution,
        'tag': s.tag.id
    })
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            background = form.cleaned_data['background']
            solution = form.cleaned_data['solution']
            tag_id = form.cleaned_data['tag']
            tag = get_object_or_404(TagList, id=tag_id)
            if Skill.objects.exclude(title=skill_name).filter(title=title).exists():
                messages.error(request, 'This skill has been exists')
            else:
                s.title = title
                s.background = background
                s.solution = solution
                s.tag = tag
                messages.success(request, 'Update succeed')
                return redirect('lesspy:skill', topic_name=topic_name,
                                skill_name=s.title)
    return render(request, 'lesspy/skill_edit.html', {'form': form})


@require_http_methods(['GET', 'POST'])
@login_required
def skill_request(request, topic_name, skill_name):
    topic = get_object_or_404(Topic, title=topic_name)
    s = get_object_or_404(Skill, title=skill_name)
    form = SkillRequestForm(initial={
        'topic': topic.id,
        'skill': s.id
    })
    if request.method == 'POST':
        form = SkillRequestForm(request.POST)
        if form.is_valid():
            topic_id = form.cleaned_data['topic']
            topic = get_object_or_404(Topic, id=topic_id)
            s_id = form.cleaned_data['skill']
            s = get_object_or_404(Skill, id=s_id)
            request_tpye = form.cleaned_data['request_type']
            subject = form.cleaned_data['subject']
            solution = form.cleaned_data['solution']
            note = form.cleaned_data['note']
            creator = request.user.userprofile
            if s.topic.id != topic.id:
                messages.error(request, 'This skill is not belong to {0}'
                               .format(topic.title))
            else:
                SkillRequest.objects.create(
                    topic=topic,
                    skill=s,
                    request_tpye=request_tpye,
                    subject=subject,
                    solution=solution,
                    note=note,
                    creator=creator
                )
                # TODO send msg to manager, and pass request confirm(backlog +1)
                messages.success(request,
                                 'Your message has been submit, the result'
                                 'will message to you after pass.')
                return redirect('lesspy:skill', topic_name=topic.title,
                                skill_name=s.title)
    return render(request, 'lesspy/skill_request.html', {'form': form})
