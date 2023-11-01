"""
Model serializers for Taskspace
"""
#pylint: disable=W0223
from rest_framework import serializers

from .models import Taskspace


class TaskspaceSerializer(serializers.Serializer):
    """ Taskspace model fields required for CRUD actions """
    id = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    owner = serializers.CharField(required=False)
    created_date = serializers.CharField(required=False)
    updated_date = serializers.CharField(required=False)

    def create(self, validated_data):
        """
        Create and return new Taskspace object
        """
        name = validated_data.get('name', None)
        description = validated_data.get('description', None)
        if name is None:
            return serializers.ValidationError("'name' is required")
        taskspace = Taskspace.objects.create(
                name=name,
                description=description,
                owner=validated_data['owner'])
        return taskspace

    def update(self, instance, validated_data):
        """
        Update and return updated Taskspace object
        """
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class TaskSerializer(serializers.Serializer):
    """ Task model fields required for CRUD actions """
    title = serializers.CharField()
    description = serializers.CharField(required=False)
    taskspace = serializers.ReadOnlyField()
