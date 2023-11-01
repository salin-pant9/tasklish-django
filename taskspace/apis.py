"""
Taskspace-realted APIs
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Taskspace
from .serializers import TaskspaceSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_taskspace_list(req):
    """
    Get the list of Taskspace associated with the loggedin account.
    NOTE: the list will include all collaborated taskspaces as well
    """
    taskspaces = Taskspace.objects.filter(owner=req.user).all()
    if taskspaces:
        return Response(TaskspaceSerializer(taskspaces, many=True).data)
    return Response({"message": "no taskspaces yet"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_taskspace(req):
    """
    Create taskspace for the current user.
    """
    serializer = TaskspaceSerializer(data=req.data)
    serializer.is_valid(raise_exception=True)
    taskspace = serializer.save(owner=req.user)
    return Response(TaskspaceSerializer(taskspace).data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_taskspace(req, taskspace_id):
    """
    Update tasksapce if the tasksapce.owner is the req.user
    """
    taskspace = None
    try:
        taskspace = Taskspace.objects.get(id=taskspace_id)
    except Taskspace.DoesNotExist:
        return Response({"message": "taskspace not found"})
    if not taskspace.owner == req.user:
        return Response({"message": "permission denied"})
    serializer = TaskspaceSerializer(taskspace, data=req.data)
    serializer.is_valid()
    taskspace = serializer.save()
    return Response(TaskspaceSerializer(taskspace).data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_taskspace(req, taskspace_id):
    """
    Delete tasksapce if the tasksapce.owner is the req.user
    """
    taskspace = None
    try:
        taskspace = Taskspace.objects.get(id=taskspace_id)
    except Taskspace.DoesNotExist:
        return Response({"message": "taskspace not found"})
    if not taskspace.owner == req.user:
        return Response({"message": "permission denied"})
    taskspace.delete()
    return Response({"message": "taskspace deleted"})
