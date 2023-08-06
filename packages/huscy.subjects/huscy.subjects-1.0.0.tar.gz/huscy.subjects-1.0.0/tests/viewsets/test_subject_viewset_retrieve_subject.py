import pytest

from django.contrib.auth.models import Permission
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

pytestmark = pytest.mark.django_db


def test_admin_user_can_retrieve_subject(admin_client, subject):
    response = retrieve_subject(admin_client, subject)

    assert response.status_code == HTTP_200_OK


def test_user_with_permission_can_retrieve_subject(client, user, subject):
    permission = Permission.objects.get(codename='view_subject')
    user.user_permissions.add(permission)

    response = retrieve_subject(client, subject)

    assert response.status_code == HTTP_200_OK


def test_user_without_permission_cannot_retrieve_subject(client, subject):
    response = retrieve_subject(client, subject)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_anonymous_user_cannot_retrive_subject(anonymous_client, subject):
    response = retrieve_subject(anonymous_client, subject)

    assert response.status_code == HTTP_403_FORBIDDEN


def retrieve_subject(client, subject):
    return client.get(reverse('subject-detail', kwargs=dict(pk=subject.pk)))
