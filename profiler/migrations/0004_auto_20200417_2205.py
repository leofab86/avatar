# Generated by Django 3.0.4 on 2020-04-17 22:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiler', '0003_auto_20200417_2144'),
    ]

    operations = [
        migrations.RenameField(
            model_name='class',
            old_name='teacher_id',
            new_name='teacher',
        ),
    ]
