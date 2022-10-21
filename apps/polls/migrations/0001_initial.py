# Generated by Django 3.2.8 on 2022-10-21 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HorseModel',
            fields=[
                ('race_id', models.IntegerField(primary_key=True, serialize=False)),
                ('score', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SampleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=300, null=True)),
            ],
        ),
    ]