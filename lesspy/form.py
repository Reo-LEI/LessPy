from django import forms

from .models import RequestLog, TagList, Library, Function, Topic, Skill


class UserForm(forms.Form):
    username = forms.CharField(30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(lable='Confirm',
                                       widget=forms.PasswordInput)
    chinesename = forms.CharField(max_length=10, required=False)

    def pwd_validate(self, pwd1, pwd2):
        return pwd1 == pwd2


class TagListForm(forms.Form):
    classes = forms.ChoiceField(choices=TagList.CLASSES_LIST)
    tag = forms.CharField(max_length=20)


class LibraryForm(forms.Form):
    name = forms.CharField(max_length=20, lable='Library name',
                           help_text='build in function or module')
    description = forms.CharField(max_length=400,
                                  help_text='400 characters max',
                                  widget=forms.Textarea)


class LibraryRequestForm(forms.Form):
    library = forms.ChoiceField()
    request_type = forms.ChoiceField(choices=RequestLog.REQUEST_TYPE_LIST)
    subject = forms.CharField(max_length=20)
    solution = forms.CharField(widget=forms.Textarea)
    note = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(LibraryRequestForm, self).__init__(*args, **kwargs)
        self.library.choices = [
            (lib.id, lib.name) for lib in Library.objects.all()]


class FunctionForm(forms.Form):
    name = forms.CharField(max_length=20, lable='Function name',
                           help_text='function or methods of library')
    description = forms.CharField(maxlength=400,
                                  help_text='400 characters max',
                                  widget=forms.Textarea)
    example = forms.CharField(lable='Example',
                              help_text='the sample example for this function')
    instance = forms.CharField(lable='Instance',
                               help_text='the whole code for this function in '
                                         'real case')
    tag = forms.ChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        super(FunctionForm, self).__init__(*args, **kwargs)
        self.tag.choices = [
            (tag.id, tag.tag) for tag in TagList.objects.filter(classes='LB')]


class FunctionRequestForm(forms.Form):
    library = forms.ChoiceField()
    function = forms.ChoiceField()
    request_type = forms.ChoiceField(choices=RequestLog.REQUEST_TYPE_LIST)
    subject = forms.CharField(max_length=20)
    solution = forms.CharField(widget=forms.Textarea)
    note = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(FunctionRequestForm, self).__init__(*args, **kwargs)
        self.library.choices = [
            (lib.id, lib.name) for lib in Library.objects.all()]
        self.function.choices = [
            (func.id, func.name) for func in
            Function.objects.filter(library=self.library)]


class TopicForm(forms.Form):
    title = forms.CharField(max_length=40, label='Topic',
                            help_text='Generalize your skill to a topic')
    description = forms.CharField(max_length=400,
                                  help_text='400 characters max',
                                  widget=forms.Textarea)


class TopicRequestForm(forms.Form):
    topic = forms.ChoiceField()
    request_type = forms.ChoiceField(choices=RequestLog.REQUEST_TYPE_LIST)
    subject = forms.CharField(max_length=40)
    solution = forms.CharField(widget=forms.Textarea)
    note = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(TopicRequestForm, self).__init__(*args, **kwargs)
        self.topic.choices = [
            (topic.id, topic.name) for topic in Topic.objects.all()]


class SkillForm(forms.Form):
    title = forms.CharField(max_length=40)
    background = forms.CharField(widget=forms.Textarea,
                                 help_text='What problem you want to solve by '
                                           'this skill')
    solution = forms.CharField(widget=forms.Textarea)
    tag = forms.ChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)
        self.tag.choices = [
            (tag.id, tag.tag) for tag in TagList.objects.filter(classes='TP')]


class SkillRequestForm(forms.Form):
    topic = forms.ChoiceField()
    skill = forms.ChoiceField()
    request_type = forms.ChoiceField(choices=RequestLog.REQUEST_TYPE_LIST)
    subject = forms.CharField(max_length=40)
    solution = forms.CharField(widget=forms.Textarea)
    note = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(SkillRequestForm, self).__init__(*args, **kwargs)
        self.topic.choices = [
            (topic.id, topic.name) for topic in Topic.objects.all()]
        self.skill.choices = [
            (skill.id, skill.name) for skill in
            Skill.objects.filter(topic=self.topic)]
