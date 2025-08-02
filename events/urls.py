# events/urls.py

from django.urls import path
from .views import CreateEventView, ListEventsView, RegisterAttendeeView, AttendeeListView

urlpatterns = [
    path('events', CreateEventView.as_view(), name='create_event'),
    path('events/', ListEventsView.as_view(), name='list_events'),
    path('events/<int:event_id>/register', RegisterAttendeeView.as_view(), name='register_attendee'),
    path('events/<int:event_id>/attendees', AttendeeListView.as_view(), name='event_attendees'),
]
