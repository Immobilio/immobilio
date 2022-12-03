# Generated by Django 4.1.3 on 2022-12-02 23:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Caracteristic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.BooleanField()),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Immobilier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surface', models.FloatField()),
                ('prix', models.FloatField()),
                ('nb_pieces', models.IntegerField()),
                ('caracteristic', models.ManyToManyField(to='main.caracteristic')),
                ('program_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.program')),
            ],
        ),
    ]
