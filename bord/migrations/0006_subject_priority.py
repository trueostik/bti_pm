# Generated by Django 4.2.2 on 2023-08-05 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bord', '0005_subject_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='priority',
            field=models.CharField(choices=[('HI', 'Високий'), ('NO', 'Звичайний'), ('LO', 'Низький')], default='NO', max_length=2),
        ),
    ]