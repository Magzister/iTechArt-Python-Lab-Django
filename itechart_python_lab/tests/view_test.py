import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_get_token_request_unauthorized(api_client):
    url = reverse('token_obtain_pair')
    response = api_client.post(url)
    assert response.status_code == 400


@pytest.mark.django_db
def test_unauthorized_requets(api_client):
    url = reverse('company_list')
    response = api_client.get(url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_authorized_request(api_client, get_or_create_token):
    url = reverse('company_list')
    token = get_or_create_token.access_token
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    response = api_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_admin_only_request_as_no_admin(api_client_with_credentials):
    url = reverse('bank_list')
    api_client = api_client_with_credentials()
    response = api_client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_admin_only_request_as_admin(api_client_with_credentials):
    url = reverse('bank_list')
    api_client = api_client_with_credentials(is_superuser=True, is_staff=True)
    response = api_client.get(url)
    assert response.status_code == 200
