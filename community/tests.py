from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import (
    Publication,
    CommunityEvent,
    EventRegistration,
)


class CommunityEventTests(TestCase):

    def setUp(self):
        User = get_user_model()

        self.user1 = User.objects.create_user(
            username="test_camper_1",
            password="TestPassword123!",
        )

        self.user2 = User.objects.create_user(
            username="test_camper_2",
            password="TestPassword123!",
        )

        self.publication = Publication.objects.create(
            author=self.user1,
            publication_type="EVENT",
            title="Quedada de prueba",
            slug="quedada-de-prueba",
            description="Una quedada para probar las inscripciones.",
            location="Cazorla",
            status="PUBLISHED",
        )

        self.event = CommunityEvent.objects.create(
            publication=self.publication,
            starts_at=timezone.now() + timedelta(days=7),
            capacity=1,
        )

        self.register_url = reverse(
            "community:event_register",
            kwargs={"slug": self.publication.slug},
        )

        self.unregister_url = reverse(
            "community:event_unregister",
            kwargs={"slug": self.publication.slug},
        )

    def test_registration(self):
        self.client.force_login(self.user1)
        response = self.client.post(self.register_url)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            EventRegistration.objects.filter(
                event=self.event,
                user=self.user1,
            ).exists()
        )

    def test_duplicate_registration(self):
        self.client.force_login(self.user1)

        self.client.post(self.register_url)
        self.client.post(self.register_url)

        self.assertEqual(
            EventRegistration.objects.filter(
                event=self.event,
                user=self.user1,
            ).count(),
            1,
        )

    def test_capacity_limit(self):
        EventRegistration.objects.create(
            event=self.event,
            user=self.user1,
        )

        self.client.force_login(self.user2)
        self.client.post(self.register_url)

        self.assertFalse(
            EventRegistration.objects.filter(
                event=self.event,
                user=self.user2,
            ).exists()
        )

    def test_past_event(self):
        self.event.starts_at = (
            timezone.now() - timedelta(days=1)
        )
        self.event.save()

        self.client.force_login(self.user1)
        self.client.post(self.register_url)

        self.assertEqual(
            EventRegistration.objects.filter(
                event=self.event
            ).count(),
            0,
        )

    def test_unregister(self):
        EventRegistration.objects.create(
            event=self.event,
            user=self.user1,
        )

        self.client.force_login(self.user1)
        response = self.client.post(self.unregister_url)

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            EventRegistration.objects.filter(
                event=self.event,
                user=self.user1,
            ).exists()
        )

    def test_database_prevents_duplicates(self):
        EventRegistration.objects.create(
            event=self.event,
            user=self.user1,
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                EventRegistration.objects.create(
                    event=self.event,
                    user=self.user1,
                )

    def test_anonymous_registration_redirects(self):
        response = self.client.post(self.register_url)

        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            EventRegistration.objects.count(),
            0,
        )


class CommunityFinalTests(TestCase):

    def setUp(self):
        from django.contrib.auth import get_user_model
        from datetime import timedelta
        from django.utils import timezone

        User = get_user_model()

        self.organizer = User.objects.create_user(
            username="organizer_final",
            password="TestPassword123!",
        )

        self.visitor = User.objects.create_user(
            username="visitor_final",
            password="TestPassword123!",
        )

        self.publication = Publication.objects.create(
            author=self.organizer,
            publication_type="EVENT",
            title="Quedada final de prueba",
            slug="quedada-final-prueba",
            description="Prueba de seguridad",
            location="Cazorla",
            status="PUBLISHED",
        )

        self.event = CommunityEvent.objects.create(
            publication=self.publication,
            starts_at=timezone.now() + timedelta(days=7),
            capacity=1,
        )

    def test_past_datetime_rejected(self):
        from .event_forms import EventProposalForm
        from datetime import timedelta
        from django.utils import timezone

        past = timezone.localtime(
            timezone.now() - timedelta(hours=2)
        )

        form = EventProposalForm(
            data={
                "title": "Prueba",
                "description": "Prueba de horario",
                "location": "Cazorla",
                "starts_at": past.date().isoformat(),
                "start_time": past.strftime("%H:%M"),
            }
        )

        form.is_valid()

        self.assertIn("start_time", form.errors)

    def test_future_datetime_accepted(self):
        from .event_forms import EventProposalForm
        from datetime import timedelta
        from django.utils import timezone

        future = timezone.localtime(
            timezone.now() + timedelta(days=3)
        )

        form = EventProposalForm(
            data={
                "title": "Prueba",
                "description": "Prueba de horario",
                "location": "Cazorla",
                "starts_at": future.date().isoformat(),
                "start_time": future.strftime("%H:%M"),
            }
        )

        form.is_valid()

        self.assertNotIn("start_time", form.errors)

    def test_organizer_can_view_participants(self):
        self.client.force_login(self.organizer)

        response = self.client.get(
            reverse(
                "community:event_participants",
                kwargs={"slug": self.publication.slug},
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_other_user_cannot_view_participants(self):
        self.client.force_login(self.visitor)

        response = self.client.get(
            reverse(
                "community:event_participants",
                kwargs={"slug": self.publication.slug},
            )
        )

        self.assertEqual(response.status_code, 403)

    def test_anonymous_cannot_view_participants(self):
        response = self.client.get(
            reverse(
                "community:event_participants",
                kwargs={"slug": self.publication.slug},
            )
        )

        self.assertEqual(response.status_code, 302)

    def test_last_place_cannot_be_overbooked_sequentially(self):
        from django.contrib.auth import get_user_model

        EventRegistration.objects.create(
            event=self.event,
            user=self.organizer,
        )

        self.client.force_login(self.visitor)

        self.client.post(
            reverse(
                "community:event_register",
                kwargs={"slug": self.publication.slug},
            )
        )

        self.assertEqual(
            EventRegistration.objects.filter(
                event=self.event
            ).count(),
            1,
        )
