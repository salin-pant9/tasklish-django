"""
Model-related tests for Taskspace
"""
import pytest
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db


def test_str_returns_taskspace_name():
    """ str(Taskspace) should return name of the task """
    taskspace = mixer.blend('taskspace.Taskspace')
    assert str(taskspace) == taskspace.name, "Should return name"


def test_str_returns_task_title():
    """ str(task) should return title of the task """
    taskspace = mixer.blend('taskspace.Taskspace')
    task = mixer.blend('taskspace.Task', taskspace=taskspace)
    assert str(task) == task.title, "Should return task title"

def test_str_returns_group_name():
    """ str(group) should return group name """
    group = mixer.blend('taskspace.TaskGroup')
    assert str(group) == group.name, "Should return group name"
