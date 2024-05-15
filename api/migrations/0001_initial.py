# Generated by Django 4.2.3 on 2024-05-15 05:40

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Masjid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=30)),
                ('alamat', models.CharField(max_length=100)),
                ('luas', models.DecimalField(decimal_places=2, max_digits=16)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
            ],
        ),
        migrations.CreateModel(
            name='Uang',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('Date', models.DateTimeField(auto_now_add=True)),
                ('red_freq', models.IntegerField()),
                ('green_freq', models.IntegerField()),
                ('blue_freq', models.IntegerField()),
                ('value', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Wifi',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ssid', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=70)),
            ],
        ),
    ]
