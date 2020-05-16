# Generated manually on 2020-04-19 20:30


from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('profiler', '0010_auto_20200420_0031'),
    ]

    operations = [
        migrations.RunSQL('ALTER TABLE profiler_teacher ALTER db_profile_id TYPE int;'),
        migrations.RunSQL('ALTER TABLE profiler_class ALTER db_profile_id TYPE int;'),
        migrations.RunSQL('ALTER TABLE profiler_class ALTER teacher_id TYPE int;'),
        migrations.RunSQL('ALTER TABLE profiler_student ALTER db_profile_id TYPE int;'),
        migrations.RunSQL('ALTER TABLE profiler_student_classes ALTER class_id TYPE int;'),
        migrations.RunSQL('ALTER TABLE profiler_student_classes ALTER student_id TYPE int;'),
    ]
