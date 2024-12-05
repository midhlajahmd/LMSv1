# Generated by Django 5.1.3 on 2024-12-04 11:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Authors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(max_length=150)),
            ],
            options={
                'ordering': ['author_name'],
            },
        ),
        migrations.CreateModel(
            name='Genres',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre_name', models.CharField(max_length=150)),
            ],
            options={
                'ordering': ['genre_name'],
            },
        ),
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_name', models.CharField(max_length=200)),
                ('ISBN', models.CharField(max_length=13, unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('rent', models.DecimalField(decimal_places=2, max_digits=8)),
                ('status', models.CharField(choices=[('available', 'Available'), ('unavailable', 'Unavailable')], default='available', max_length=13)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='book_author', to='librarymsv1.authors')),
                ('genre', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='book_genre', to='librarymsv1.genres')),
            ],
        ),
    ]
