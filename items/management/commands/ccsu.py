
from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        admin_user = User.objects.create(
            email="admin@web.top",
            role='admin',
            is_staff=True,
            is_superuser=True,
            is_active=True,

        )
        admin_user.set_password("querty")
        admin_user.save()
        print("admin_created")

        moderator = User.objects.create(
            email="moder@web.top",
            role='moderator',
            is_staff=True,
            is_superuser=False,
            is_active=True,


        )

        moderator.set_password('qwerty')
        moderator.save()
        print('Moderator Created')

        user = User.objects.create(
            email="user@web.top",
            role='user',
            is_staff=False,
            is_superuser=False,
            is_active=True,

        )
        user.set_password('qwerty')
        user.save()
        print('user Created')