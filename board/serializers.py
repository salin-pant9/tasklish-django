""" Serializers for boards app """
from rest_framework import serializers

from .models import Board, Card, BoardHour
from users.serializers import UserSerializer


class BoardSerializer(serializers.ModelSerializer):
    """Serializer for Board model"""

    owner = serializers.SerializerMethodField()

    def get_owner(self, obj):
        """Get the board owner"""
        return UserSerializer(obj.created_by).data

    class Meta:
        model = Board
        fields = ["id", "name", "description", "owner", "shared_with"]

    def save(self, **kwargs):
        """Save board and add the current user as the board owner"""
        self.validated_data["created_by"] = self.context["user"]  # type: ignore
        return super().save(**kwargs)


class CardSerializer(serializers.ModelSerializer):
    """Serializer for Card model"""

    class Meta:
        model = Card
        fields = "__all__"
        read_only_fields = ["created_by", "board"]

    def save(self, **kwargs):
        """Save card and add the current user as the card owner"""
        self.validated_data["created_by"] = self.context["user"]  # type: ignore
        self.validated_data["board"] = self.context["board"]  # type: ignore
        return super().save(**kwargs)


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
        monday = self.validated_data.get("monday")  # type: ignore
        tuesday = self.validated_data.get("tuesday")  # type: ignore
        wednesday = self.validated_data.get("wednesday")  # type: ignore
        thursday = self.validated_data.get("thursday")  # type: ignore
        friday = self.validated_data.get("friday")  # type: ignore
        saturday = self.validated_data.get("saturday")  # type: ignore
        sunday = self.validated_data.get("sunday")  # type: ignore

        if (
            not monday
            or not tuesday
            or not wednesday
            or not thursday
            or not friday
            or not saturday
            or not sunday
        ):
            raise serializers.ValidationError("You must provide hours for all 7 days.")

        if not isinstance(monday, list):
            raise serializers.ValidationError("Monday hours must be a list of objects")
        if not isinstance(tuesday, list):
            raise serializers.ValidationError("Tuesday hours must be a list of objects")
        if not isinstance(wednesday, list):
            raise serializers.ValidationError(
                "Wednesday hours must be a list of objects"
            )
        if not isinstance(thursday, list):
            raise serializers.ValidationError(
                "Thursday hours must be a list of objects"
            )
        if not isinstance(friday, list):
            raise serializers.ValidationError("Friday hours must be a list of objects")
        if not isinstance(saturday, list):
            raise serializers.ValidationError(
                "Saturday hours must be a list of objects"
            )
        if not isinstance(sunday, list):
            raise serializers.ValidationError("Sunday hours must be a list of objects")

        return super().save(**kwargs)
