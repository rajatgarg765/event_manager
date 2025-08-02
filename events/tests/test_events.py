import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from events.models import Event
from django.utils.timezone import now
from datetime import datetime, timedelta


@pytest.mark.django_db
def test_create_event_success():
    client = APIClient()
    data = {
        'name': 'D1emo Event',
        'location': 'Mumbai',
        'start_time': str(datetime.now()),
        'end_time': str(datetime.now() + timedelta(days=1)),
        'max_capacity': 100
    }
    response = client.post(reverse('create_event'), data, format='json')
    assert response.status_code == 201
    assert Event.objects.count() == 1


@pytest.mark.django_db
def test_create_event_missing_fields():
    client = APIClient()
    response = client.post(reverse('create_event'), {}, format='json')
    assert response.status_code == 422
    assert 'Missing required field' in response.json()['error']


@pytest.mark.django_db
def test_list_events_only_upcoming():
    client = APIClient()
    Event.objects.create(
        name='Future Event',
        location='Delhi',
        start_time=now() + timedelta(days=2),
        end_time=now() + timedelta(days=2, hours=2),
        max_capacity=50
    )
    Event.objects.create(
        name='Past Event',
        location='Goa',
        start_time=now() - timedelta(days=2),
        end_time=now() - timedelta(days=1),
        max_capacity=50
    )
    response = client.get(reverse('list_events'))
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]['name'] == 'Future Event'
