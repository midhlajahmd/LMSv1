# Generated by Django 5.1.3 on 2024-12-08 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('librarymsv1', '0008_studentprofile_delete_studentmembership'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
