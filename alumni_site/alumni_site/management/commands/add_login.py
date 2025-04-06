from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from alumni_site.models import Login
from django.utils import timezone

class Command(BaseCommand):
    help = 'Creates a new login record'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, required=True)
        parser.add_argument('--password', type=str, required=True)
        parser.add_argument('--name', type=str, required=True)

    def handle(self, *args, **options):
        try:
            # Hash the password
            hashed_password = make_password(options['password'])
            
            # Create the login record
            login = Login.objects.create(
                email=options['email'],
                password=hashed_password,
                name=options['name'],
                created_at=timezone.now()
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created login record for {options["email"]}')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating login record: {str(e)}')
            ) 