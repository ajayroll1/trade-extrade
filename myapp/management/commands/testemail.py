from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Test Django email configuration'

    def handle(self, *args, **options):
        try:
            send_mail(
                subject='Django Test Email',
                message='This is a test email from your Django application.',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS('Successfully sent test email'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to send email: {str(e)}'))