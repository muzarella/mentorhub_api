# Generated by Django 4.2.6 on 2023-10-06 13:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='organization',
            old_name='url',
            new_name='InvitationLink',
        ),
    ]