""" Models realted tests """
import pytest
from mixer.backend.django import mixer

from django.contrib.auth import get_user_model

pytestmark = pytest.mark.django_db


def test_custom_user_str_returns_username():
    """ str(CustomUser) should return username """
    user = mixer.blend(get_user_model(), username="safal")
    assert str(user) == "safal", "Should return username"


def test_otp_str_returns_username():
    """ str(otp) should return username """
    user = mixer.blend(get_user_model(), username="safal")
    otp = mixer.blend("users.OTP", user=user)
    assert str(otp) == user.username, "Should return username"


def test_otp_generate_code():
    """ otp.generate_code produce 6-character token """
    user = mixer.blend(get_user_model(), username="safal")
    otp = mixer.blend("users.OTP", user=user)
    otp.generate_code()
    assert len(otp.code) == 6, "Code should be 6-character token"
