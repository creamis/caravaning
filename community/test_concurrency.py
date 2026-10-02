from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from threading import Barrier

from django.contrib.auth import get_user_model
from django.db import close_old_connections
from django.test import TransactionTestCase
from django.urls import reverse
from django.utils import timezone

from .models import (
    Publication,
    CommunityEvent,
    EventRegistration,
)


class ConcurrentRegistrationTests(TransactionTestCase):

    def test_two_users_last_place(self):
        User = get_user_model()

        organizer = User.objects.create_user(
            username="organizer_concurrent"
        )
        users = [
            User.objects.create_user(
                username=f"camper_concurrent_{i}"
            )
            for i in range(2)
        ]

        publication = Publication.objects.create(
            author=organizer,
            publication_type="EVENT",
            title="Prueba simultánea",
            slug="prueba-simultanea",
            description="Prueba de última plaza",
            location="Cazorla",
            status="PUBLISHED",
        )

        event = CommunityEvent.objects.create(
            publication=publication,
            starts_at=timezone.now() + timedelta(days=7),
            capacity=1,
        )

        url = reverse(
            "community:event_register",
            kwargs={"slug": publication.slug},
        )

        barrier = Barrier(2)

        def register(user):
            from django.test import Client

            close_old_connections()
            try:
                client = Client()
                client.force_login(user)
                barrier.wait(timeout=10)
                response = client.post(url)
                return response.status_code
            finally:
                close_old_connections()

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(register, users))

        registered = EventRegistration.objects.filter(
            event=event
        ).count()

        print(
            "\nRespuestas:", results,
            "\nInscripciones:", registered
        )

        self.assertLessEqual(
            registered,
            1,
            "Se ha superado el aforo de la quedada."
        )

        self.assertEqual(
            registered,
            1,
            "Ninguno de los usuarios consiguió inscribirse."
        )
