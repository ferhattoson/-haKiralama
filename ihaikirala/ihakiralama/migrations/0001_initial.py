# Generated by Django 5.0.4 on 2024-04-25 14:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='İHA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ihaAd', models.CharField(max_length=255)),
                ('ihaMarka', models.CharField(max_length=255)),
                ('ihaModel', models.CharField(max_length=255)),
                ('ihaAgirlik', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Kiralanan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('baslangicTarihi', models.DateField()),
                ('bitisTarihi', models.DateField()),
                ('iha', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ihakiralama.i̇ha')),
                ('kullanici', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
