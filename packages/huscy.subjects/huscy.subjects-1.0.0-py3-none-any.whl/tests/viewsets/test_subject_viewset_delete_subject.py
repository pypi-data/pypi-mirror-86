import pytest

from django.contrib.auth.models import Permission
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN

pytestmark = pytest.mark.django_db


def test_admin_user_can_delete_subject(admin_client, subject):
    response = delete_subject(admin_client, subject)

    assert response.status_code == HTTP_204_NO_CONTENT


def test_user_with_permission_can_delete_subject(client, user, subject):
    permission = Permission.objects.get(codename='delete_subject')
    user.user_permissions.add(permission)

    response = delete_subject(client, subject)

    assert response.status_code == HTTP_204_NO_CONTENT


def test_user_without_permission_cannot_delete_subject(client, subject):
    response = delete_subject(client, subject)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_anonymous_user_cannot_delete_subject(anonymous_client, subject):
    response = delete_subject(anonymous_client, subject)

    assert response.status_code == HTTP_403_FORBIDDEN


def delete_subject(client, subject):
    return client.delete(reverse('subject-detail', kwargs=dict(pk=subject.pk)))
