""" Serializers for boards app """
from rest_framework import serializers

from .models import Board, Card


class BoardSerializer(serializers.ModelSerializer):
    """ Serializer for Board model """
    owner = serializers.ReadOnlyField(source='created_by')

    class Meta:
        model = Board
        fields = ['id', 'name', 'description', 'owner', 'shared_with']

    def save(self, **kwargs):
        """ Save board and add the current user as the board owner """
        self.validated_data['created_by'] = self.context['request'].user
        return super().save(**kwargs)


class CardSerializer(serializers.ModelSerializer):
    """ Serializer for Card model """
    class Meta:
        model = Card
        fields = '__all__'
