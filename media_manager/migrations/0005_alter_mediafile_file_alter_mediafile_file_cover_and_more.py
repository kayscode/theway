# Generated by Django 4.2.5 on 2023-10-21 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media_manager', '0004_rename_media_id_notifications_media_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediafile',
            name='file',
            field=models.FileField(upload_to='media_files'),
        ),
        migrations.AlterField(
            model_name='mediafile',
            name='file_cover',
            field=models.ImageField(upload_to='media_covers'),
        ),
        migrations.AlterField(
            model_name='mediafile',
            name='uploaded_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
