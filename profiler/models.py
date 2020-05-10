import random
from django.db import models
from django.core.exceptions import ValidationError


class_type_names = [
    'Math', 'Science', 'English', 'Social Studies', 'Calculus', 'Physics', 'Biology', 'Chemistry',
    'Computer Science', 'Theater', 'Art', 'Philosophy', 'Law', 'Business', 'Nursing', 'Medicine'
]


class DatabaseProfile(models.Model):
    db_profile_name = models.CharField(max_length=200)
    db_profile_id = models.AutoField(primary_key=True)
    classes = models.IntegerField()
    class_types = models.IntegerField()
    teachers = models.IntegerField()
    classes_per_teacher = models.IntegerField()
    students = models.IntegerField()
    classes_per_student = models.IntegerField()

    def __str__(self):
        return self.db_profile_name

    def clean(self):
        if self.classes_per_teacher > self.classes:
            raise ValidationError({'classes_per_teacher': 'Cannot have more classes per teacher than classes.'})
        if self.classes_per_student > self.classes:
            raise ValidationError({'classes_per_student': 'Cannot have more classes per student than classes.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super(DatabaseProfile, self).save(*args, **kwargs)
        teacher_list = Teacher.save_teacher_set(db_profile=self, total_teachers=self.teachers)
        class_list = Class.save_class_set(
            db_profile=self,
            total_classes=self.classes,
            teacher_list=teacher_list,
            classes_per_teacher=self.classes_per_teacher,
            class_types=self.class_types
        )
        Student.save_student_set(
            db_profile=self,
            total_students=self.students,
            class_list=class_list,
            classes_per_student=self.classes_per_student
        )
        return self


class Teacher(models.Model):
    db_profile = models.ForeignKey(DatabaseProfile, on_delete=models.CASCADE)
    teacher_name = models.CharField(max_length=200)
    teacher_id = models.AutoField(primary_key=True)

    @staticmethod
    def save_teacher_set(*, db_profile, total_teachers):
        teacher_list = []
        while len(teacher_list) < total_teachers:
            teacher = Teacher(
                db_profile=db_profile,
                teacher_name='Billy_Bob'
            )
            teacher.save()
            teacher_list.append(teacher)

        return teacher_list


class Class(models.Model):
    db_profile = models.ForeignKey(DatabaseProfile, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, related_name='classes', blank=True, null=True, on_delete=models.SET_NULL)
    class_id = models.AutoField(primary_key=True)
    class_type = models.CharField(max_length=200)

    @staticmethod
    def save_class_set(*, db_profile, total_classes, teacher_list, classes_per_teacher, class_types):
        class_list = []
        random_class_type_sample = random.sample(class_type_names, class_types)
        unused_class_type_list = random_class_type_sample.copy()
        available_teachers = list(map(lambda teacher: {'teacher_instance': teacher, 'classes': 0}, teacher_list))

        print('available_teachers', available_teachers)

        def assign_teacher():
            teacher_index = random.randint(0, len(available_teachers) - 1)
            teacher = available_teachers[teacher_index]
            teacher['classes'] = teacher['classes'] + 1
            if teacher['classes'] == classes_per_teacher:
                del available_teachers[teacher_index]
            return teacher['teacher_instance']

        def assign_class_type():
            if len(unused_class_type_list) != 0:
                return unused_class_type_list.pop()
            return random_class_type_sample[random.randint(0, class_types - 1)]

        while len(class_list) < total_classes:
            class_instance = Class(
                db_profile=db_profile,
                teacher=assign_teacher(),
                class_type=assign_class_type()
            )
            class_instance.save()
            class_list.append(class_instance)

        return class_list


class Student(models.Model):
    db_profile = models.ForeignKey(DatabaseProfile, on_delete=models.CASCADE)
    classes = models.ManyToManyField(Class)
    student_name = models.CharField(max_length=200)
    student_id = models.AutoField(primary_key=True)

    @staticmethod
    def save_student_set(*, db_profile, total_students, class_list, classes_per_student):
        student_list = []
        while len(student_list) < total_students:
            student = Student(
                db_profile=db_profile,
                student_name='John_Doe'
            )
            student.save()
            student_list.append(student)
            class_assignment_list = random.sample(class_list, classes_per_student)
            for _class in class_assignment_list:
                student.classes.add(_class)

