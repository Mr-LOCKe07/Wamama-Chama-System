# Generated by Django 4.2.20 on 2025-03-20 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('STK_PUSH', '0004_article'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='link',
            field=models.URLField(max_length=500),
        ),
    ]
