# Generated by Django 2.2.16 on 2020-10-20 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_tournament_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='date',
            field=models.DateTimeField(blank=True),
        ),
    ]
