""" Serializers for boards app """
from rest_framework import serializers

from .models import Board, Card, BoardHour


class BoardSerializer(serializers.ModelSerializer):
    """Serializer for Board model"""

    owner = serializers.ReadOnlyField(source="created_by")

    class Meta:
        model = Board
        fields = ["id", "name", "description", "owner", "shared_with"]

    def save(self, **kwargs):
        """Save board and add the current user as the board owner"""
        self.validated_data["created_by"] = self.context["request"].user  # type: ignore
        return super().save(**kwargs)


class CardSerializer(serializers.ModelSerializer):
    """Serializer for Card model"""

    class Meta:
        model = Card
        fields = "__all__"


class BoardHoursSerializer(serializers.ModelSerializer):
    """Serializer for Board model with hours"""

    class Meta:
        model = BoardHour
        fields = "__all__"

    def save(self, **kwargs):
        """
        The hours needs to be a list of objects with the following structure:
        {
            "monday": [
                {
                    start: "09:00",
                    end: "17:00",
                },
                {
                    start: "19:00",
                    end: "21:00",
                }
            ]
        }
        """

        return super().save(**kwargs)
