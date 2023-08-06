from model_bakery import baker

from django.contrib.auth.models import Permission
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN

from huscy.subjects.serializers import ContactSerializer


def test_admin_can_create_subject(admin_client):
    response = create_subject(admin_client)

    assert response.status_code == HTTP_201_CREATED


def test_user_with_permissions_can_create_subject(client, user):
    permission = Permission.objects.get(codename='add_subject')
    user.user_permissions.add(permission)

    response = create_subject(client)

    assert response.status_code == HTTP_201_CREATED


def test_user_without_permissions_cannot_create_subject(client):
    response = create_subject(client)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_anonymous_cannot_create_subject(anonymous_client):
    response = create_subject(anonymous_client)

    assert response.status_code == HTTP_403_FORBIDDEN


def create_subject(client):
    contact = baker.prepare('subjects.Contact')

    data = {
        'contact': ContactSerializer(contact).data,
        'is_patient': False,
    }
    return client.post(reverse('subject-list'), data=data, format='json')
