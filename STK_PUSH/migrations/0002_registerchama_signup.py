# Generated by Django 5.0.2 on 2025-03-19 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('STK_PUSH', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegisterChama',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('name_of_chama', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('id_number', models.IntegerField()),
                ('county', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SignUp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name_of_chama', models.CharField(blank=True, max_length=50)),
                ('password', models.CharField(max_length=128)),
            ],
        ),
    ]
