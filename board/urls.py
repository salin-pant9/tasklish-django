from django.urls import path

from .apis import (
    get_boards,
    get_shared_board,
    create_board,
    add_hours,
)


urlpatterns = [
    path("", get_boards, name="get_boards"),
    path("shared", get_shared_board, name="get_shared_board"),
    path("create", create_board, name="create_board"),
    path("add-hours/<int:board_id>", add_hours, name="board_add_hours"),
]
