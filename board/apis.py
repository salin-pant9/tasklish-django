""" API endpoints for the Board app. """
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from .serializers import BoardSerializer, BoardHoursSerializer, CardSerializer
from .models import Board, Card


################### Board ###################
@swagger_auto_schema(
    method="get",
    responses={200: BoardSerializer(many=True)},
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_boards(request):
    """Get all boards for the current user."""
    boards = request.user.boards.all()
    serializer = BoardSerializer(boards, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method="get",
    responses={200: BoardSerializer(many=True)},
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_shared_board(request):
    """Get all boards shared with the current user."""
    boards = request.user.shared_boards.all()
    serializer = BoardSerializer(boards, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method="post",
    request_body=BoardSerializer,
    responses={200: BoardSerializer()},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_board(request):
    """Create a new board."""
    serializer = BoardSerializer(data=request.data, context={"user": request.user})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@swagger_auto_schema(
    method="put",
    request_body=BoardHoursSerializer,
    responses={
        200: BoardHoursSerializer(),
        404: "Board not found.",
    },
)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def add_hours(request, board_id):
    """Add hours to a board."""
    try:
        board = request.user.boards.get(id=board_id)
    except Board.DoesNotExist:
        return Response({"error": "Board not found."}, status=404)

    serializer = BoardHoursSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    board.hours = serializer.save()
    board.save()

    return Response(BoardSerializer(board).data)


@swagger_auto_schema(method="get", responses={200: BoardHoursSerializer()})
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_hours(request, board_id):
    """Get hours for a board."""
    try:
        board = request.user.boards.get(id=board_id)
    except Board.DoesNotExist:
        return Response({"error": "Board not found."}, status=404)
    serializer = BoardHoursSerializer(board.hours)
    return Response(serializer.data)


################### Card ###################
@swagger_auto_schema(
    method="get",
    responses={200: CardSerializer(many=True)},
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_cards(request, board_id):
    """Get all cards for a board."""
    try:
        board = request.user.boards.get(id=board_id)
    except Board.DoesNotExist:
        return Response({"error": "Board not found."}, status=404)
    cards = board.cards.all()
    serializer = CardSerializer(cards, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method="post",
    request_body=CardSerializer,
    responses={200: CardSerializer()},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_card(request, board_id):
    """Create a new card."""

    try:
        board = request.user.boards.get(id=board_id)
    except Board.DoesNotExist:
        return Response({"error": "Board not found."}, status=404)

    serializer = CardSerializer(
        data=request.data, context={"user": request.user, "board": board}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@swagger_auto_schema(
    method="put",
    request_body=CardSerializer,
    responses={200: CardSerializer()},
)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_card(request, card_id):
    """Update a Card."""

    try:
        card = Card.objects.get(id=card_id)
    except Card.DoesNotExist:
        return Response({"error": "Card not found."}, status=404)

    serializer = CardSerializer(card, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@swagger_auto_schema(
    method="delete",
    responses={200: CardSerializer()},
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_card(request, card_id):
    """Delete a Card."""

    try:
        card = Card.objects.get(id=card_id)
    except Card.DoesNotExist:
        return Response({"error": "Card not found."}, status=404)

    card.delete()
    return Response({"message": "Card deleted."})
