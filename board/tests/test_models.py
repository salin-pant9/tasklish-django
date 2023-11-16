import pytest
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db


def test_board_str():
    board = mixer.blend('board.Board', name='Test Board')
    assert str(board) == 'Test Board'


def test_card_str():
    card = mixer.blend('board.Card', title='Test Card')
    assert str(card) == 'Test Card'
