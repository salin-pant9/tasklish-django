""" API endpoints for the Board app. """
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from .serializers import BoardSerializer


@swagger_auto_schema(
    method="get",
    responses={200: BoardSerializer(many=True)},
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_boards(request):
    """ Get all boards for the current user. """
    boards = request.user.boards.all()
    serializer = BoardSerializer(boards, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method="get",
    responses={200: BoardSerializer(many=True)},
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_shared_board(request):
    """ Get all boards shared with the current user. """
    boards = request.user.shared_boards.all()
    serializer = BoardSerializer(boards, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method="post",
    request_body=BoardSerializer,
    responses={200: BoardSerializer()},
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_board(request):
    """ Create a new board. """
    serializer = BoardSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
