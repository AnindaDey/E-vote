# Generated by Django 5.2.4 on 2025-07-20 07:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_candidate_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='ballot',
            unique_together={('position', 'candidate')},
        ),
    ]
