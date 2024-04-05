from django.urls import path

from .apis import (
    get_boards,
    get_shared_board,
    create_board,
    add_hours,
    get_hours,
    get_cards,
    create_card,
    update_card
)


urlpatterns = [
    path("", get_boards, name="get_boards"),
    path("shared", get_shared_board, name="get_shared_board"),
    path("create", create_board, name="create_board"),
    path("add-hours/<int:board_id>", add_hours, name="board_add_hours"),
    path("get-hours/<int:board_id>", get_hours, name="board_get_hours"),
    path("cards/<int:board_id>", get_cards, name="get_cards"),
    path("card/create/<int:board_id>", create_card, name="create_card"),
    path("card/update/<int:card_id>", update_card, name="update_card"),
]
