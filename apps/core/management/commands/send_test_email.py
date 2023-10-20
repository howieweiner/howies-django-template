from django.conf import settings
from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Sends test email to recipient"

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument("recipient", type=str)

    def handle(self, *args, **options):
        recipient = options["recipient"]

        self.stdout.write(
            self.style.NOTICE(f"Sending test email to {recipient}")
        )

        EmailMessage(
            subject='Test Email',
            body='This is a test email',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient]
        ).send(fail_silently=False)
