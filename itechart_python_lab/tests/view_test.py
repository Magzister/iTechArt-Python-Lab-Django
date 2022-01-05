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
