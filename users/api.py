"""API Views for users"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema


from .serializers import (
    LoginSerializer,
    UserSerializer,
    RegisterSerializer,
    PasswordResetSerializer,
    LoginResponseSerializer,
)
from .models import OTP
from .utils import OTPAction


@swagger_auto_schema(
    method="post",
    responses={200: LoginResponseSerializer()},
    request_body=LoginSerializer,
)
@api_view(["POST"])
def login_view(request):
    """
    Takes `username` and `password` to validate user.
    Upon successful validation, user details along with token is returned

    Request:
    {
        "username": "",
        "password": ""
    }

    Response:
    {
        "user" : {},
        "token": "",
        "login_message" : ""
    }
    """

    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data
    token, _ = Token.objects.get_or_create(user=user)

    response = {
        "user": UserSerializer(user).data,
        "token": token.key,
    }

    serializer = LoginResponseSerializer(data=response)  # type: ignore
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method="post",
    responses={200: LoginResponseSerializer()},
    request_body=RegisterSerializer,
)
@api_view(["POST"])
def signup_view(request):
    """
    Takes initial users details to create an account.
    Upon successful account creation, registration email is sent
    to the email used during registration. Also, user and token details
    are returned.

    Response:
    {
        "user": {},
        "token": ""
    }
    """
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data
    # This will dispath a signal to send email
    _ = OTP.objects.create(user=user, otp_for=OTPAction.REGISTRATION)
    # Return Token and user info
    token = Token.objects.create(user=user)
    response = {"user": UserSerializer(user).data, "token": token.key}
    response_serializer = LoginResponseSerializer(data=response)  # type: ignore
    response_serializer.is_valid(raise_exception=True)
    return Response(response_serializer.data, status=201)


@swagger_auto_schema(
    method="get",
    responses={
        200: "Please check your email for the next step",
        400: "Please check your email for the next step",
    },
)
@api_view(["GET"])
def password_reset_request(_, email):
    """
    Check if user exists with the given email. If exists, check if is_active is
    set to True. If user is active, generate a token and send the token via email.
    """
    try:
        user = get_user_model().objects.get(email=email)
        _ = OTP.objects.create(user=user, otp_for=OTPAction.PASSWORD_RESET)
    except get_user_model().DoesNotExist:
        return Response(
            {"error": "Please check your email for the next step"}, status=400
        )
    return Response({"message": "Please check your email for the next step"})


@swagger_auto_schema(
    method="get",
    responses={
        200: "Thank you for confirming your account",
        400: "Invalid OTP",
    },
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def confirm_otp(req, otp_code):
    """
    Check if the OTP exists and is associated the current user.
    If so, confirm the OTP.
    """
    otp_list = req.user.otp.all()
    for otp in otp_list:
        if otp.code == otp_code:
            if otp.otp_for == OTPAction.REGISTRATION:
                # Confirm registration
                user = req.user
                user.is_verified = True
                user.save()
                otp.delete()
                return Response({"message": "Thank you for confirming your account"})
            if otp.otp_for == OTPAction.PASSWORD_RESET:
                # Confirm password reset
                return redirect(
                    reverse("password_reset_confirm", kwargs={"otp_code": otp.code})
                )
    return Response({"message": "Invalid OTP"})


@swagger_auto_schema(
    method="post",
    responses={
        200: "Your password has been updated",
        400: "OTP is invalid",
    },
    request_body=PasswordResetSerializer,
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def password_reset_confirm(req, otp_code):
    """
    Given a otp_code, if its is valid let the user update their password.
    """
    serializer = PasswordResetSerializer(data=req.data)
    serializer.is_valid(raise_exception=True)
    try:
        otp = OTP.objects.get(code=otp_code, user=req.user)
        user = req.user
        new_password = serializer.validated_data
        user.set_password(new_password)
        user.save()
        otp.delete()
        return Response({"message": "Your password has been updated"})
    except OTP.DoesNotExist:
        return Response({"message": "OTP is invalid"})
