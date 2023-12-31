# Generated by Django 4.2.5 on 2023-10-14 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('media_manager', '0002_alter_notifications_is_validated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mediafile',
            name='is_approved',
        ),
        migrations.AddField(
            model_name='mediafile',
            name='status',
            field=models.CharField(choices=[('pending', 'en attente'), ('rejected', 'rejecter'), ('accepted', 'accepter')], default='pending', max_length=20),
        ),
        migrations.AddField(
            model_name='notifications',
            name='status',
            field=models.CharField(choices=[('pending', 'en attente'), ('rejected', 'rejecter'), ('accepted', 'accepter')], default='pending', max_length=20),
        ),
        migrations.CreateModel(
            name='NotificationsSourceMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent_date', models.DateField(auto_created=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('description', models.TextField()),
                ('is_validated', models.BooleanField(default=False, null=True)),
                ('status', models.CharField(choices=[('pending', 'en attente'), ('rejected', 'rejecter'), ('accepted', 'accepter')], default='pending', max_length=20)),
                ('source_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='media_manager.sourcemediafile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
