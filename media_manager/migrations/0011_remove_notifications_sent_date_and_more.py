# Generated by Django 4.2.5 on 2023-10-22 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media_manager', '0010_remove_notifications_is_validated_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notifications',
            name='sent_date',
        ),
        migrations.RemoveField(
            model_name='notificationssourcemedia',
            name='sent_date',
        ),
        migrations.AddField(
            model_name='notifications',
            name='request_type',
            field=models.CharField(choices=[('creation-request', 'creation-request'), ('deletion-request', 'delete-request')], default='creation-request', max_length=20),
        ),
        migrations.AddField(
            model_name='notificationssourcemedia',
            name='request_type',
            field=models.CharField(choices=[('creation-request', 'creation-request'), ('deletion-request', 'delete-request')], default='creation-request', max_length=20),
        ),
    ]
