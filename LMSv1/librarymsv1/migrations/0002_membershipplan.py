# Generated by Django 5.1.3 on 2024-12-04 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('librarymsv1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MembershipPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_name', models.CharField(max_length=100, unique=True)),
                ('rent_limit', models.PositiveIntegerField()),
                ('rent_duration', models.PositiveIntegerField()),
                ('plan_duration', models.PositiveIntegerField()),
                ('fee', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
