# Generated by Django 2.2.14 on 2020-09-15 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20200914_1902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membre',
            name='categorie',
            field=models.ManyToManyField(blank=True, null=True, related_name='membres', to='core.Categorie'),
        ),
    ]
