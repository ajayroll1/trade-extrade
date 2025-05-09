# Generated manually to fix migration issue

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                # Include all operations from 0002_auto_20250505_1350 but as state_operations only
                # This tells Django the models exist in the state without trying to create tables again
            ],
        ),
    ]