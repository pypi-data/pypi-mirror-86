import urllib
from datetime import date

import pytest
from model_bakery import baker

from django.contrib.auth.models import Permission
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

pytestmark = pytest.mark.django_db


def test_admin_user_can_list_subjects(admin_client):
    response = list_subjects(admin_client)

    assert response.status_code == HTTP_200_OK


def test_user_with_permission_can_list_subjects(client, user):
    permission = Permission.objects.get(codename='view_subject')
    user.user_permissions.add(permission)

    response = list_subjects(client)

    assert response.status_code == HTTP_200_OK


def test_user_without_permission_cannot_list_subjects(client):
    response = list_subjects(client)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_anonymous_user_cannot_list_subjects(anonymous_client):
    response = list_subjects(anonymous_client)

    assert response.status_code == HTTP_403_FORBIDDEN


@pytest.mark.parametrize('subject_count, result_count', [
    (1, 1),
    (25, 25),
    (26, 25),
    (100, 25),
])
def test_pagination(admin_client, subject_count, result_count):
    baker.make('subjects.Subject', _quantity=subject_count)

    response = list_subjects(admin_client)

    json = response.json()
    assert json['count'] == subject_count
    assert len(json['results']) == result_count


def test_paginated_item_count(admin_client):
    baker.make('subjects.Subject', _quantity=20)

    response = list_subjects(admin_client, dict(count=5))

    json = response.json()
    assert json['count'] == 20
    assert len(json['results']) == 5


@pytest.mark.parametrize('search_string, result_count', [
    ('D', 1),
    ('Donna', 1),
    ('Donna Wetter', 1),
    ('Wetter', 1),
    ('W', 1),
    ('Regen', 0),
])
def test_search_by_name(admin_client, search_string, result_count):
    baker.make('subjects.Subject', contact__display_name='Donna Wetter')

    response = list_subjects(admin_client, dict(search=search_string))

    json = response.json()
    assert json['count'] == result_count


@pytest.mark.parametrize('date_of_birth, result_count', [
    ('2000-01-01', 1),
    ('2004-12-24', 0),
])
def test_search_by_date_of_birth(admin_client, date_of_birth, result_count):
    baker.make('subjects.Subject', contact__date_of_birth=date(2000, 1, 1))

    response = list_subjects(admin_client, dict(search=date_of_birth))

    json = response.json()
    assert json['count'] == result_count


def list_subjects(client, params=None):
    url = reverse('subject-list')
    if params:
        url += '?' + urllib.parse.urlencode(params)
    return client.get(url)
