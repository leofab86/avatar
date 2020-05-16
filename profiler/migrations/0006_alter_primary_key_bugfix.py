# Generated manually on 2020-04-17 23:30


from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('profiler', '0005_auto_20200417_2211'),
    ]

    operations = [
        migrations.RunSQL('ALTER TABLE profiler_teacher ALTER database_profile_id TYPE varchar(200);'),
        migrations.RunSQL('ALTER TABLE profiler_class ALTER database_profile_id TYPE varchar(200);'),
        migrations.RunSQL('ALTER TABLE profiler_class ALTER teacher_id TYPE varchar(200);'),
        migrations.RunSQL('ALTER TABLE profiler_student ALTER database_profile_id TYPE varchar(200);'),
        migrations.RunSQL('ALTER TABLE profiler_student_classes ALTER class_id TYPE varchar(200);'),
        migrations.RunSQL('ALTER TABLE profiler_student_classes ALTER student_id TYPE varchar(200);'),
    ]
