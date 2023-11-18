from django.db import models
from django.contrib.auth import get_user_model


class Board(models.Model):
    """
    Represents a board that contains cards. A board has a view which allows
    the board owner to use it as a kanban board, calendar, and list.
    Board can be shared among users.
    """
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='boards'
    )
    shared_with = models.ManyToManyField(
        get_user_model(),
        related_name='shared_boards',
        blank=True
    )

    def __str__(self):
        return self.name


class Card(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        related_name='cards'
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='cards'
    )
    status = models.CharField(max_length=30, default='todo')
    start_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
