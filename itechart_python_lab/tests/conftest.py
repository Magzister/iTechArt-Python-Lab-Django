import uuid
import pytest


from rest_framework import test
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def test_password():
    return 'test-passowrd'


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)
    return make_user


@pytest.fixture
def api_client():
    return test.APIClient()


@pytest.fixture
def get_or_create_token(db, create_user):
    user = create_user()
    token = RefreshToken.for_user(user)
    return token


@pytest.fixture
def api_client_with_credentials(db,
                                create_user,
                                api_client,
                                get_or_create_token):
    def make_api_client(**kwargs):
        user = create_user(**kwargs)
        token = get_or_create_token.access_token
        api_client.force_authenticate(user=user, token=token)
        return api_client
    return make_api_client
