import pytest

from django.contrib.auth.models import Permission
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

from huscy.subjects.serializers import ContactSerializer

pytestmark = pytest.mark.django_db


def test_admin_user_can_update_subject(admin_client, subject):
    response = update_subject(admin_client, subject)

    assert response.status_code == HTTP_200_OK


def test_user_with_permissions_can_update_subject(client, user, subject):
    permission = Permission.objects.get(codename='change_subject')
    user.user_permissions.add(permission)

    response = update_subject(client, subject)

    assert response.status_code == HTTP_200_OK


def test_user_without_permissions_cannot_update_subject(client, subject):
    response = update_subject(client, subject)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_anonymous_user_cannot_update_subject(anonymous_client, subject):
    response = update_subject(anonymous_client, subject)

    assert response.status_code == HTTP_403_FORBIDDEN


def update_subject(client, subject):
    return client.put(
        reverse('subject-detail', kwargs=dict(pk=subject.pk)),
        data=dict(
            contact=ContactSerializer(subject.contact).data,
            is_patient=False,
        ),
        format='json'
    )
