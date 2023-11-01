"""
API-related tests for Taskspace
"""
import pytest
from mixer.backend.django import mixer
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


pytestmark = pytest.mark.django_db


def get_authenticated_client():
    """ Create user and authenticate the client with it """
    client = APIClient()
    user = mixer.blend(get_user_model())
    client.force_authenticate(user=user)
    return client, user


def test_taskspace_list():
    """
    Taskspace list should return list of taskspaces and 200 status code
    """
    client, user = get_authenticated_client()
    # Two taskspaces owned by the user
    _ = mixer.blend('taskspace.Taskspace', owner=user)
    _ = mixer.blend('taskspace.Taskspace', owner=user)
    res = client.get('/taskspace/list')
    assert res.status_code == 200, "Should return 200"
    assert len(res.data) == 2, "Should return 1 taskspace"


def test_taskspace_list_without_takspace():
    """
    Taskspace list should return message and 200 status code
    """
    client, _ = get_authenticated_client()
    res = client.get('/taskspace/list')
    assert res.status_code == 200, "Should return 200"
    assert "message" in res.data, "Should return message"


def test_taskspace_create():
    """
    Taskspace create should return the created taskspace with the status_code 200 
    """
    client, user = get_authenticated_client()
    new_taskspace_info = {"name": "test taskspace",
                          "description": "This is a test taskspace"}
    res = client.post('/taskspace/create', new_taskspace_info, format='json')
    assert res.status_code == 200, "Should return 200"
    assert res.data["name"] == new_taskspace_info["name"], "Should return taskspace"
    assert res.data["owner"] == user.username, "Should be owned by current user"


def test_taskspace_udpate():
    """
    Taskspace update should return the updated taskspace info with the status 200
    """
    client, user = get_authenticated_client()
    # Create taskspace to update
    taskspace = mixer.blend('taskspace.Taskspace', owner=user)
    res = client.put(f"/taskspace/update/{taskspace.id}", {"name": "updated test"},
                     format='json')
    assert res.status_code == 200, "Should return 200"
    assert res.data["name"] == "updated test", "Should update taskspace"


def test_taskspace_udpate_nonexistent_taskspace():
    """
    Taskspace update should return the message with status code 200
    """
    client, _ = get_authenticated_client()
    res = client.put("/taskspace/update/1234", {"name": "updated test"},
                     format='json')
    assert res.status_code == 200, "Should return 200"
    assert "message" in res.data, "Should update taskspace"


def test_taskspace_udpate_permission_denied():
    """
    Taskspace update should return the message with status code 200
    """
    client, _ = get_authenticated_client()
    user = mixer.blend(get_user_model())
    taskspace = mixer.blend('taskspace.Taskspace', owner=user)
    res = client.put(f"/taskspace/update/{taskspace.id}", {"name": "updated test"},
                     format='json')
    assert res.status_code == 200, "Should return 200"
    assert "message" in res.data, "Should update taskspace"


def test_taskspace_delete():
    """
    Taskspace delete should return the message with the status 200
    """
    client, user = get_authenticated_client()
    # Create taskspace to update
    taskspace = mixer.blend('taskspace.Taskspace', owner=user)
    res = client.delete(f"/taskspace/delete/{taskspace.id}")
    assert res.status_code == 200, "Should return 200"
    assert "message" in res.data, "Should return message"


def test_taskspace_delete_nonexistent_taskspace():
    """
    Taskspace delete should return the message with status code 200
    """
    client, _ = get_authenticated_client()
    res = client.delete("/taskspace/delete/1234")
    assert res.status_code == 200, "Should return 200"
    assert "message" in res.data, "Should update taskspace"


def test_taskspace_delete_permission_denied():
    """
    Taskspace delete should return the message with status code 200
    """
    client, _ = get_authenticated_client()
    user = mixer.blend(get_user_model())
    taskspace = mixer.blend('taskspace.Taskspace', owner=user)
    res = client.delete(f"/taskspace/delete/{taskspace.id}")
    assert res.status_code == 200, "Should return 200"
    assert "message" in res.data, "Should return message"
