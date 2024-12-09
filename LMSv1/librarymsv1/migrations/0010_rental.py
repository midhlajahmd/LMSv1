# Generated by Django 5.1.3 on 2024-12-08 18:03

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('librarymsv1', '0009_studentprofile_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rental',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rental_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('due_date', models.DateTimeField(blank=True, null=True)),
                ('is_rented', models.BooleanField(default=True)),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='librarymsv1.books')),
                ('student_profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='librarymsv1.studentprofile')),
            ],
        ),
    ]
