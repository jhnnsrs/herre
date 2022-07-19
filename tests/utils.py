import os

from herre.types import User

DIR_NAME = os.path.dirname(os.path.realpath(__file__))


def build_relative(path):
    return os.path.join(DIR_NAME, path)


async def fake_token_generator(*args, **kwargs):
    return {
        "access_token": "fake_access_token",
        "refresh_token": "fake_refresh_token",
    }


async def fake_user_generator(*args, **kwargs):
    return User(sub="fake_user")
