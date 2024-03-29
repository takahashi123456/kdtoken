# Generated by Django 3.2.8 on 2022-12-14 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_racestimemodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(blank=True, max_length=100, null=True)),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('bazyou', models.CharField(blank=True, max_length=100, null=True)),
                ('how_to_bet', models.CharField(blank=True, max_length=100, null=True)),
                ('total_money', models.BigIntegerField(default=0)),
                ('win', models.IntegerField(default=0)),
                ('race', models.IntegerField(default=0)),
                ('accuracy', models.FloatField(default=0)),
                ('recovery', models.FloatField(default=0)),
            ],
        ),
    ]
