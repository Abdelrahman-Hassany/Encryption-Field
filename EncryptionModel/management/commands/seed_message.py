from django.core.management.base import BaseCommand
from EncryptionModel.models import Message
from faker import Faker

#should be "Command" Django uses this naming convention
class Command(BaseCommand):
    # Description of the command shown when using --help
    help = 'Seed database with fake Message data'
    
#This method is required and called automatically when the command is executed
#It contains the core logic of your management command
    def handle(self, *args, **options):
        # Create a Faker instance to generate fake names and texts
        faker = Faker()

        # Generate and insert 20 fake Message records
        for _ in range(20):
            name = faker.name()           # Generate fake name
            message = faker.text()        # Generate fake message text

            # > Create a new Message object (automatically encrypted)
            Message.objects.create(
                name=name,
                message=message
            )

        # Print success message to the console
        self.stdout.write(self.style.SUCCESS('Successfully seeded 20 messages.'))
