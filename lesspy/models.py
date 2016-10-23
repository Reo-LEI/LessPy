from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """  store non-auth related information about user."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Text(models.Model):
    """ store all text(example: usage) for whole site"""
    name = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=20, unique=True)
    content = models.TextField()


class TagList(models.Model):
    """ store all tag for function and skill"""
    CLASSES_LIST = [
        ('LB', 'library'),
        ('TP', 'topic')
    ]
    classes = models.CharField(choices=CLASSES_LIST)
    tag = models.CharField(max_length=20)


class RequestLog(models.Model):
    """ base class for all issue and modify request log """
    REQUEST_TYPE_LIST = [
        ('add', 'Add'),
        ('issue', 'Issue')
    ]
    request_type = models.CharField(choices=REQUEST_TYPE_LIST)
    subject = models.TextField(max_length=40)
    solution = models.TextField()
    note = models.TextField()
    creator = models.ForeignKey(
        UserProfile, blank=True, null=True, on_delete=models.SET_NULL)
    approver = models.ForeignKey(
        UserProfile, blank=True, null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField('update time')

    class Meta:
        abstract = True


class Library(models.Model):
    """ for python's build-in type, module and library """
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField(max_length=400)
    creator = models.ForeignKey(UserProfile)
    timestamp = models.DateTimeField('update time')


class LibraryRequest(RequestLog):
    """ The issue of Library """
    library = models.ForeignKey(Library, on_delete=models.CASCADE)


class Function(models.Model):
    """ for python's methods """
    name = models.CharField(unique=True, max_length=20)
    description = models.TextField(max_length=400)
    instance = models.TextField(max_length=400)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    tag = models.ForeignKey(TagList, blank=True, null=True)
    creator = models.ForeignKey(UserProfile)
    timestamp = models.DateTimeField('update time')


class FunctionRequest(RequestLog):
    """ The issue of Function """
    function = models.ForeignKey(Function, on_delete=models.CASCADE)


class Topic(models.Model):
    """ The topic for less code """
    title = models.CharField(unique=True, max_length=40)
    description = models.TextField(max_length=400)
    creator = models.ForeignKey(UserProfile)
    timestamp = models.DateTimeField('update time')


class TopicRequest(RequestLog):
    """ The issue of Topic """
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)


class Skill(models.Model):
    """ The coding skills for each less code topic """
    title = models.CharField(unique=True, max_length=40)
    background = models.TextField(max_length=400)
    solution = models.TextField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    tag = models.ForeignKey(TagList, blank=True, null=True)
    creator = models.ForeignKey(UserProfile)
    timestamp = models.DateTimeField('update time')


class SkillRequest(RequestLog):
    """ The issue of Skill """
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
