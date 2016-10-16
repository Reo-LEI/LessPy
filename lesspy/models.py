from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """  store non-auth related information about user."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class IssueLog(models.Model):
    """ base class for issue """
    issue = models.TextField()
    solution = models.TextField()
    note = models.TextField()
    contributor = models.ForeignKey(
        UserProfile, blank=True, null=True, on_delete=models.SET_NULL)
    approver = models.ForeignKey(
        UserProfile, blank=True, null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField('update time')

    class Meta:
        abstract = True


class TagList(models.Model):
    """ store all tag for function and skill"""
    CLASSES_LIST = [
        ('LB', 'library'),
        ('SK', 'skill')
    ]
    classes = models.CharField(choices=CLASSES_LIST)
    tag = models.CharField(max_length=20)


class Library(models.Model):
    """ for python's build-in type, module and library """
    name = models.CharField(unique=True)
    description = models.TextField(max_length=500)
    creator = models.ForeignKey(UserProfile)
    timestamp = models.DateTimeField('update time')


class LibraryIssue(IssueLog):
    """ The issue of Library """
    library = models.ForeignKey(Library, on_delete=models.CASCADE)


class Function(models.Model):
    """ for python's methods """
    name = models.CharField(unique=True)
    description = models.TextField(max_length=500)
    instance = models.TextField(max_length=500)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    tag = models.CharField(max_length=20, blank=True, null=True)
    creator = models.ForeignKey(UserProfile)
    timestamp = models.DateTimeField('update time')


class FunctionIssue(IssueLog):
    """ The issue of Function """
    function = models.ForeignKey(Function, on_delete=models.CASCADE)


class Topic(models.Model):
    """ The topic for less code """
    title = models.CharField(unique=True)
    description = models.TextField(max_length=500)
    creator = models.ForeignKey(UserProfile)
    timestamp = models.DateTimeField('update time')


class TopicIssue(IssueLog):
    """ The issue of Topic """
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)


class Skill(models.Model):
    """ The coding skills for each less code topic """
    title = models.CharField(unique=True)
    background = models.TextField(max_length=500)
    solution = models.TextField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    tag = models.CharField(max_length=20, blank=True, null=True)
    creator = models.ForeignKey(UserProfile)
    timestamp = models.DateTimeField('update time')


class SkillIssue(IssueLog):
    """ The issue of Skill """
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)



