from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """  store non-auth related information about user."""
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True)


class Library(models.Model):
    """for python's build-in type, module and library"""
    name = models.CharField(unique=True)
    description = models.TextField(max_length=500)
    timestamp = models.DateTimeField('update time')
    contributor = models.ManyToManyField(UserProfile,
                                         through='LibraryContributionLog')


class LibraryContributionLog(models.Model):
    """change log for Library"""
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    contributor = models.ForeignKey(
        UserProfile, blank=True, null=True, on_delete=models.SET_NULL)
    approver = models.ForeignKey(
        UserProfile, blank=True, null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField('update time')
    change = models.TextField()


class Function(models.Model):
    """for python's methods"""
    name = models.CharField(unique=True)
    description = models.TextField(max_length=500)
    instance = models.TextField(max_length=500)
    timestamp = models.DateTimeField('update time')
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    contributor = models.ManyToManyField(UserProfile,
                                         through='FunctionContributionLog')


class FunctionContributionLog(models.Model):
    """change log for Function"""
    function = models.ForeignKey(Function, on_delete=models.CASCADE)
    contributor = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL)
    approver = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField('update time')
    change = models.TextField()


class Topic(models.Model):
    """the topic for less code"""
    title = models.CharField(unique=True)
    description = models.TextField(max_length=500)
    timestamp = models.DateTimeField('update time')
    contributor = models.ManyToManyField(UserProfile,
                                         through='TopicContributionLog')


class TopicContributionLog(models.Model):
    """change log for Topic"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    contributor = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL)
    approver = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField('update time')
    change = models.TextField()


class Skill(models.Model):
    """the coding skills for each less code topic"""
    title = models.CharField(unique=True)
    background = models.TextField(max_length=500)
    solution = models.TextField()
    timestamp = models.DateTimeField('update time')

