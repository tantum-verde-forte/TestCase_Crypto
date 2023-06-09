# Generated by Django 4.1.7 on 2023-03-19 07:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cryptocurrency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('price', models.CharField(max_length=100)),
                ('market_volume', models.CharField(max_length=100)),
                ('change', models.CharField(max_length=100)),
                ('favourites', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
