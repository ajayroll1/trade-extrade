# Generated manually to fix database state

from django.db import migrations


class Migration(migrations.Migration):
    """
    This migration fixes the database state by marking all previous migrations
    as applied without actually running their SQL commands.
    """

    dependencies = [
        ('myapp', '0008_merge_20250509_1555'),  # Updated to reference the existing migration
    ]

    operations = [
        # This is an empty migration that serves as a checkpoint
        # After applying this, we'll use --fake-initial to reset the migration state
    ]
