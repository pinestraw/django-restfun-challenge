import pytest
import os
import json
from mixer.backend.django import mixer
from django.conf import settings


@pytest.fixture
def user():
    data = {
        "id": 1,
        "username": "test",
        "email": "test@test.com",
        "first_name": "Test",
        "last_name": "Test",
        "password": "test@12345",
    }
    return mixer.blend(settings.AUTH_USER_MODEL, **data)


def load_fixture(request, fixture_name):
    this_dir = os.path.split(request.module.__file__)[0]
    return json.load(open(os.path.join(this_dir, "fixtures", fixture_name), "r"))


@pytest.fixture(scope="function")
def input_fixtures(request):
    def _input_fixtures(file_name):
        return load_fixture(request, file_name)

    return _input_fixtures
