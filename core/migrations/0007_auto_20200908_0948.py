# Generated by Django 2.2.15 on 2020-09-08 09:48

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20200826_1742'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=35, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cotisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=25)),
                ('paye', models.BooleanField(default=False)),
                ('montant_paye', models.PositiveSmallIntegerField()),
                ('reste_paye', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='membre',
            options={'ordering': ('created_at',)},
        ),
        migrations.AddField(
            model_name='membre',
            name='age',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='membre',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='membre',
            name='date_naissance',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='membre',
            name='entraineur',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='membre',
            name='licence_fideration',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='membre',
            name='sexe',
            field=models.CharField(choices=[('H', 'HOMME'), ('F', 'FEMME')], default='M', max_length=2),
        ),
        migrations.AddField(
            model_name='reservation',
            name='duration',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='membre',
            name='categorie',
            field=models.ManyToManyField(blank=True, related_name='membres', to='core.Categorie'),
        ),
        migrations.AddField(
            model_name='membre',
            name='cotisation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='membres', to='core.Cotisation'),
        ),
    ]
