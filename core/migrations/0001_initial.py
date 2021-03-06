# Generated by Django 2.2.15 on 2020-09-29 16:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=35, unique=True)),
            ],
            options={
                'ordering': ('nom',),
            },
        ),
        migrations.CreateModel(
            name='Cotisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=25)),
                ('paye', models.BooleanField(default=False)),
                ('montant', models.PositiveSmallIntegerField(default=4000)),
                ('montant_paye', models.PositiveSmallIntegerField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Membre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=35, unique=True)),
                ('sexe', models.CharField(choices=[('H', 'HOMME'), ('F', 'FEMME')], default='H', max_length=2)),
                ('tel', models.CharField(blank=True, max_length=13, null=True)),
                ('date_naissance', models.DateField(blank=True, null=True)),
                ('age', models.SmallIntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('mail', models.EmailField(blank=True, max_length=254, null=True)),
                ('profession', models.CharField(max_length=35, null=True)),
                ('entraineur', models.BooleanField(default=False)),
                ('tournoi', models.BooleanField(default=False)),
                ('licence_fideration', models.BooleanField(default=False)),
                ('categorie', models.ManyToManyField(blank=True, related_name='membres', to='core.Categorie')),
                ('cotisation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='membres', to='core.Cotisation')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='Terrain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matricule', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('duration', models.PositiveSmallIntegerField(default=1)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('eclairage', models.BooleanField(default=False)),
                ('eclairage_paye', models.BooleanField(default=False)),
                ('entrainement', models.BooleanField(default=False)),
                ('type_match', models.CharField(choices=[('E', 'Entrainement'), ('M', 'Match'), ('T', 'Tournoi')], default='M', max_length=25)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('players', models.ManyToManyField(blank=True, related_name='reservations', to='core.Membre')),
                ('terrain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='core.Terrain')),
            ],
        ),
    ]
