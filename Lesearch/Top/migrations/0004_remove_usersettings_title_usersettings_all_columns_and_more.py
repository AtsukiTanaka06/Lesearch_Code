# Generated by Django 4.1 on 2023-01-17 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Top', '0003_alter_usersettings_content_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersettings',
            name='title',
        ),
        migrations.AddField(
            model_name='usersettings',
            name='all_columns',
            field=models.TextField(default=None, max_length=500),
        ),
        migrations.AlterField(
            model_name='usersettings',
            name='conversion_columns',
            field=models.TextField(max_length=300),
        ),
        migrations.AlterField(
            model_name='usersettings',
            name='customer_columns',
            field=models.TextField(max_length=300),
        ),
        migrations.AlterField(
            model_name='usersettings',
            name='menu_columns',
            field=models.TextField(max_length=300),
        ),
        migrations.AlterField(
            model_name='usersettings',
            name='platform_columns',
            field=models.TextField(max_length=300),
        ),
        migrations.AlterField(
            model_name='usersettings',
            name='survey_columns',
            field=models.TextField(max_length=300),
        ),
    ]
