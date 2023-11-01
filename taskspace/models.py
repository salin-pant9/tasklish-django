"""
Models for Taskspace
"""
from django.db import models
from django.contrib.auth import get_user_model


class Taskspace(models.Model):
    """
    Taskspace holds your tasks and todos. Taskspace can be shared with
    friends.
    """
    name = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                              related_name='taskspaces')
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    def __str__(self):
        """ Return taskspace name """
        return self.name


class TaskGroup(models.Model):
    """
    TaskGroup helps organise tasks into various categories.
    Unlike traditional categories, TaskGroup allows single
    tasks to be in multiple group.
    """
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    taskspace = models.ForeignKey(Taskspace, on_delete=models.CASCADE,
                                  related_name='groups')

    def __str__(self):
        """ Return group name """
        return self.name


class Task(models.Model):
    """
    Task represents your day-to-day todos and events.
    """
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    taskspace = models.ForeignKey(Taskspace, on_delete=models.CASCADE,
                                  related_name='tasks')
    group = models.ManyToManyField(TaskGroup)

    def __str__(self):
        """ Return title """
        return self.title
