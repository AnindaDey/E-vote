# Generated by Django 5.2.4 on 2025-07-20 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_candidate_unique_together_position_description_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ballot',
            options={'verbose_name_plural': 'Ballots'},
        ),
        migrations.AlterUniqueTogether(
            name='ballot',
            unique_together={('candidate', 'position', 'election')},
        ),
    ]
