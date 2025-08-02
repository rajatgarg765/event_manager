import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from events.models import Event, Attendee
from django.utils.timezone import now, timedelta

@pytest.fixture
def event():
    return Event.objects.create(
        name='Test Event',
        location='Chennai',
        start_time=now() + timedelta(days=1),
        end_time=now() + timedelta(days=1, hours=1),
        max_capacity=2
    )

@pytest.mark.django_db
def test_register_attendee_success(event):
    client = APIClient()
    url = reverse('register_attendee', args=[event.id])
    data = {'name': 'John Doe', 'email': 'john@example.com'}
    response = client.post(url, data, format='json')
    assert response.status_code == 201
    assert Attendee.objects.count() == 1

@pytest.mark.django_db
def test_register_attendee_duplicate(event):
    Attendee.objects.create(event=event, name='John', email='john@example.com')
    client = APIClient()
    response = client.post(reverse('register_attendee', args=[event.id]), {
        'name': 'John', 'email': 'john@example.com'
    }, format='json')
    assert response.status_code == 400
    assert 'already registered' in response.json()['error']

@pytest.mark.django_db
def test_register_attendee_full_capacity(event):
    for i in range(2):
        Attendee.objects.create(event=event, name=f'User{i}', email=f'user{i}@example.com')
    client = APIClient()
    response = client.post(reverse('register_attendee', args=[event.id]), {
        'name': 'Extra', 'email': 'extra@example.com'
    }, format='json')
    assert response.status_code == 400
    assert 'Event is full' in response.json()['error']

@pytest.mark.django_db
def test_attendee_list_pagination(event):
    for i in range(25):
        Attendee.objects.create(event=event, name=f'A{i}', email=f'a{i}@mail.com')

    client = APIClient()
    response = client.get(reverse('event_attendees', args=[event.id]), {'page': 2, 'limit': 10})
    data = response.json()
    assert response.status_code == 200
    assert data['current_page'] == 2
    assert len(data['attendees']) == 10
