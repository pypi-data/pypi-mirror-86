import pytest

from django.contrib.auth.models import Permission
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

from huscy.subjects.serializers import ContactSerializer

pytestmark = pytest.mark.django_db


def test_admin_user_can_update_guardian(admin_client, subject, guardian):
    response = update_guardian(admin_client, subject, guardian)

    assert response.status_code == HTTP_200_OK


def test_user_with_permission_can_update_guardian(client, user, subject, guardian):
    change_permission = Permission.objects.get(codename='change_subject')
    user.user_permissions.add(change_permission)

    response = update_guardian(client, subject, guardian)

    assert response.status_code == HTTP_200_OK


def test_user_without_permission_cannot_update_guardian(client, subject, guardian):
    response = update_guardian(client, subject, guardian)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_anonymous_user_cannot_update_guardian(anonymous_client, subject, guardian):
    response = update_guardian(anonymous_client, subject, guardian)

    assert response.status_code == HTTP_403_FORBIDDEN


def update_guardian(client, subject, guardian):
    return client.put(
        reverse('guardian-detail', kwargs=dict(pk=guardian.pk, subject_pk=subject.pk)),
        data=ContactSerializer(guardian).data,
        format='json',
    )
