# Generated by Django 3.2.3 on 2023-06-01 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_page', '0004_alter_route_route_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stops',
            fields=[
                ('stop_id', models.AutoField(primary_key=True, serialize=False)),
                ('stop_name', models.TextField()),
                ('stop_lat', models.FloatField()),
                ('stop_lon', models.FloatField()),
            ],
        ),
    ]
