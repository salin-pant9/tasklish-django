"""
Serializers-related tests for Taskspace
"""
import pytest
from taskspace.serializers import (
        TaskspaceSerializer,
        TaskSerializer
        )

pytestmark = pytest.mark.django_db


def test_taskspace_valid_data():
    """
    {
        "name": "blah",
        "description": "blah blah"
    }

    should be a valid data for taskspace
    """
    test_data = {"name": "test taskspace",
                 "description": "this is a test taskspace"}
    serializer = TaskspaceSerializer(data=test_data)

    assert serializer.is_valid(raise_exception=True), "Should return True"
    assert serializer.errors == {}, "Should not return any errors"


def test_task_valid_data():
    """
    {
        "title": "blah",
        "description": "blah blah"
    }

    should be a valid data for task
    """
    test_data = {"title": "test task",
                 "description": "this is a test task"}
    serializer = TaskSerializer(data=test_data)

    assert serializer.is_valid(raise_exception=True), "Should return True"
