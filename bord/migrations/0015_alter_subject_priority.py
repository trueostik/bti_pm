# Generated by Django 4.2 on 2024-03-16 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bord', '0014_alter_task_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='priority',
            field=models.CharField(choices=[('AA', 'Високий'), ('BB', 'Звичайний'), ('CC', 'Низький')], default='AA', max_length=3),
        ),
    ]
