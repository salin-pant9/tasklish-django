from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Creates a superuser'

    def handle(self, *args, **kwargs):
        if not get_user_model().objects.filter(username='safal').exists():
            get_user_model().objects.create_superuser(
                username='safal',
                email='safal@test.com',
                password='safal12345'
            )
            print('Superuser has been created')
