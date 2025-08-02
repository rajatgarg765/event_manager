from django.db import IntegrityError
from django.utils.timezone import localtime, get_current_timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_datetime
from django.utils.timezone import now, make_aware
from django.core.paginator import Paginator
from events.models import Event, Attendee


class CreateEventView(APIView):
    REQUIRED_FIELDS = ['name', 'location', 'start_time', 'end_time', 'max_capacity']

    def post(self, request):
        data = request.data

        # Validate required fields
        missing_fields = [field for field in self.REQUIRED_FIELDS if field not in data]
        if missing_fields:
            return Response(
                {
                    'error': f'Missing required field(s): {", ".join(missing_fields)}'
                },
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        # Validate datetime and max_capacity
        try:
            start_time = make_aware(parse_datetime(data['start_time']))
            end_time = make_aware(parse_datetime(data['end_time']))
            max_capacity = int(data['max_capacity'])

            if start_time >= end_time:
                return Response(
                    {'error': 'start_time must be earlier than end_time'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if max_capacity <= 0:
                return Response(
                    {'error': 'max_capacity must be a positive integer'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except (ValueError, TypeError):
            return Response(
                {'error': 'Invalid data format for start_time, end_time, or max_capacity'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            event = Event.objects.create(
                name=data['name'],
                location=data['location'],
                start_time=start_time,
                end_time=end_time,
                max_capacity=max_capacity
            )
            return Response({'id': event.id, 'message': 'Event created'}, status=status.HTTP_201_CREATED)

        except IntegrityError:
            return Response(
                {'error': 'Duplicate event with same name, location, start_time, and end_time'},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ListEventsView(APIView):
    def get(self, request):
        tz = get_current_timezone()
        upcoming = Event.objects.filter(start_time__gte=now()).order_by('start_time')
        data = [{
            'id': e.id,
            'name': e.name,
            'location': e.location,
            'start_time': localtime(e.start_time).strftime('%Y-%m-%d %H:%M:%S'),
            'end_time': localtime(e.end_time).strftime('%Y-%m-%d %H:%M:%S'),
            'max_capacity': e.max_capacity,
            'created_on': localtime(e.created_on).strftime('%Y-%m-%d %H:%M:%S'),
            'timezone': str(tz),
        } for e in upcoming]
        return Response(data, status=status.HTTP_200_OK)


class RegisterAttendeeView(APIView):
    def post(self, request, event_id):
        try:
            data = request.data
            event = Event.objects.get(id=event_id)

            if event.attendees.count() >= event.max_capacity:
                return Response({'error': 'Event is full'}, status=status.HTTP_400_BAD_REQUEST)

            if Attendee.objects.filter(event=event, email=data['email']).exists():
                return Response({'error': 'Attendee already registered'}, status=status.HTTP_400_BAD_REQUEST)

            attendee = Attendee.objects.create(
                event=event,
                name=data['name'],
                email=data['email']
            )
            return Response({'id': attendee.id, 'message': 'Registration successful'}, status=status.HTTP_201_CREATED)

        except Event.DoesNotExist:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

from django.core.paginator import Paginator, EmptyPage

class AttendeeListView(APIView):
    def get(self, request, event_id):
        try:
            page = int(request.GET.get('page', 1))
            per_page = int(request.GET.get('limit', 10))

            attendees = Attendee.objects.filter(event_id=event_id).order_by('created_on')
            paginator = Paginator(attendees, per_page)

            if page > paginator.num_pages or page < 1:
                return Response(
                    {'error': f'Page {page} out of range. Only {paginator.num_pages} page(s) available.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            page_obj = paginator.page(page)

            data = [{
                'id': a.id,
                'name': a.name,
                'email': a.email,
                'created_on': localtime(a.created_on).strftime('%Y-%m-%d %H:%M:%S'),
            } for a in page_obj]

            return Response({
                'attendees': data,
                'total_pages': paginator.num_pages,
                'current_page': page,
                'count': paginator.count,
                'next_page': page + 1 if page < paginator.num_pages else None,
                'prev_page': page - 1 if page > 1 else None,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
