# Generated by Django 4.1 on 2023-01-18 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Top', '0004_remove_usersettings_title_usersettings_all_columns_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersettings',
            name='user_data',
            field=models.BinaryField(default=None),
        ),
    ]
