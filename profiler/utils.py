from profiler.models import DatabaseProfile, Teacher, Student, Class
from profiler.serializers import DatabaseProfileSerializer, TeacherSerializer, ClassSerializer, StudentSerializer


def custom_data_optimization(db_profile_id, teacher_levels, class_levels, student_levels):
    db_profile = DatabaseProfile.objects.get(db_profile_id=db_profile_id)
    db_profile = DatabaseProfileSerializer(db_profile).data
    teachers = []
    classes = []
    students = []
    include_classes = False
    include_students = False
    students_with_classes = {} if (class_levels == 3 or student_levels == 2) else None
    students_with_classes_with_students = {} if student_levels == 3 else None

    if teacher_levels > 0:
        include_classes = teacher_levels > 1 or class_levels > 0 or student_levels > 1
        include_students = include_classes and (teacher_levels > 2 or class_levels > 1 or student_levels > 0)
        prefetch_command = 'classes' if include_classes else None
        prefetch_command = 'classes__student_set' if include_students else prefetch_command
        teachers = Teacher.objects.filter(db_profile_id=db_profile_id).prefetch_related(prefetch_command)
        recursive_levels = 2 if include_classes else 1
        recursive_levels = 3 if include_students else recursive_levels
        teachers = TeacherSerializer(teachers, many=True, recursive_levels=recursive_levels).data

    if class_levels > 0 and not include_classes:
        include_students = class_levels > 1 or student_levels > 0
        prefetch_command = 'student_set' if include_students else None
        classes = Class.objects.filter(db_profile_id=db_profile_id).prefetch_related(prefetch_command)
        recursive_levels = 2 if include_students else 1
        classes = ClassSerializer(classes, many=True, recursive_levels=recursive_levels).data

    if student_levels > 0 and not include_students:
        students = Student.objects.filter(db_profile_id=db_profile_id)
        students = StudentSerializer(students, many=True, recursive_levels=1).data

    if include_classes:
        for teacher in teachers:
            this_teacher_classes = teacher['classes']
            if class_levels == 1 and include_students:
                def remove_students(c):
                    new_class = c.copy()
                    del new_class['students']
                    return new_class

                new_classes = list(map(remove_students, this_teacher_classes))
                classes = classes + new_classes
            else:
                classes = classes + list(map(lambda c: c.copy(), this_teacher_classes))
            if include_students:
                for _class in this_teacher_classes:
                    new_class = _class.copy()
                    this_class_students = new_class['students']
                    new_class['students'] = list(map(lambda s: s.copy(), _class['students']))
                    if students_with_classes is not None or students_with_classes_with_students is not None:
                        for student in this_class_students:
                            student_id = student['student_id']
                            if students_with_classes is not None:
                                new_class_without_students = new_class.copy()
                                del new_class_without_students['students']
                                if student_id not in students_with_classes:
                                    new_student = student.copy()
                                    new_student['classes'] = [new_class_without_students]
                                    students_with_classes[student_id] = new_student
                                else:
                                    students_with_classes[student_id]['classes'] \
                                        .append(new_class_without_students)
                            if students_with_classes_with_students is not None:
                                if student_id not in students_with_classes_with_students:
                                    new_student = student.copy()
                                    new_student['classes'] = [new_class]
                                    students_with_classes_with_students[student_id] = new_student
                                else:
                                    students_with_classes_with_students[student_id]['classes'].append(new_class)

    if class_levels == 3:
        students = []
        used_students = {}
        for _class in classes:
            new_students = []
            for student in _class['students']:
                student_id = student['student_id']
                new_students.append(students_with_classes[student_id])
                if student_id not in used_students:
                    used_students[student_id] = True
                    if student_levels == 1:
                        students.append(student)
                    if student_levels == 2:
                        students.append(students_with_classes[student_id])
                    if student_levels == 3:
                        students.append(students_with_classes_with_students[student_id])
            _class['students'] = new_students

    if student_levels == 2 and class_levels != 3:
        for student in students:
            student['classes'] = students_with_classes[student['student_id']]['classes']

    if student_levels == 3 and class_levels != 3:
        print('do something')

    if teacher_levels > 0:
        db_profile['teacher_set'] = teachers
    if class_levels > 0:
        db_profile['class_set'] = classes
    if student_levels > 0:
        db_profile['student_set'] = students

    return db_profile
