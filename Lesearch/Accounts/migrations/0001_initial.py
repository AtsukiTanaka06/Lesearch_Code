# Generated by Django 4.1 on 2023-01-22 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consultantName', models.CharField(max_length=200)),
                ('clientName1', models.CharField(max_length=200, null=True)),
                ('clientName2', models.CharField(max_length=200, null=True)),
                ('clientName3', models.CharField(max_length=200, null=True)),
            ],
        ),
    ]
