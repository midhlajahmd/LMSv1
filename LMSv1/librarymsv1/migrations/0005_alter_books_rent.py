# Generated by Django 5.1.3 on 2024-12-05 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('librarymsv1', '0004_bookcontent_book_name_books_added_date_books_hidden_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='rent',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=8, null=True),
        ),
    ]
