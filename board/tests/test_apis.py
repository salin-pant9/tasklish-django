import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from rest_framework.authtoken.models import Token
from mixer.backend.django import mixer

from ..apis import create_board, get_boards, get_shared_board
from ..models import Board


pytestmark = pytest.mark.django_db


def test_get_boards():
    """ Test get_boards API endpoint """
    factory = APIRequestFactory()
    user = mixer.blend(get_user_model())
    token = Token.objects.create(user=user)
    board = mixer.blend(Board, created_by=user)
    request = factory.get('/boards', HTTP_AUTHORIZATION=f'Token {token}')
    response = get_boards(request)
    assert response.status_code == 200
    assert response.data[0]['name'] == board.name # type: ignore


def test_get_shared_board():
    """ Test get_shared_board API endpoint """
    factory = APIRequestFactory()
    user = mixer.blend(get_user_model())
    token = Token.objects.create(user=user)
    board = mixer.blend(Board)
    board.shared_with.add(user) # type: ignore
    board.save() # type: ignore

    request = factory.get('/boards/shared', HTTP_AUTHORIZATION=f'Token {token}')
    response = get_shared_board(request)
    assert response.status_code == 200
    assert len(response.data) == 1 # type: ignore


def test_create_board():
    """ Test create_board API endpoint """
    factory = APIRequestFactory()
    user = mixer.blend(get_user_model())
    token = Token.objects.create(user=user)

    data = {
        'name': 'test',
        'description': 'test'
    }
    request = factory.post('/boards', data, HTTP_AUTHORIZATION=f'Token {token}')

    response = create_board(request)
    assert response.status_code == 200
    assert response.data['name'] == 'test' # type: ignore
