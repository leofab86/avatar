from profiler.models import DatabaseProfile, Teacher, Student, Class
from profiler.serializers import DatabaseProfileSerializer, TeacherSerializer, ClassSerializer, StudentSerializer
from common.logging import Timing


def custom_data_optimization(db_profile_id, teacher_levels, class_levels, student_levels):
    timing = Timing('custom_data_optimization')
    timing_data = {}
    db_profile = DatabaseProfile.objects.get(db_profile_id=db_profile_id)
    timing.start('db_profile_evaluate_queryset')
    db_profile = DatabaseProfileSerializer(db_profile).data
    timing_data['db_profile_evaluate_queryset'] = timing.end('db_profile_evaluate_queryset')
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
        timing.start('teachers_query_and_serialize')
        teachers = [t.serialize(recursive_levels=recursive_levels) for t in teachers]
        timing_data['teachers_query_and_serialize'] = timing.end('teachers_query_and_serialize')

    if (class_levels > 0 or student_levels == 3) and not include_classes:
        include_students = class_levels > 1 or student_levels > 0
        prefetch_command = 'student_set' if include_students else None
        classes = Class.objects.filter(db_profile_id=db_profile_id).prefetch_related(prefetch_command)
        recursive_levels = 2 if include_students else 1
        timing.start('classes_query_and_serialize')
        classes = [c.serialize(recursive_levels=recursive_levels) for c in classes]
        timing_data['classes_query_and_serialize'] = timing.end('classes_query_and_serialize')

    if student_levels > 0 and student_levels != 3 and not include_students:
        prefetch_command = 'classes' if student_levels > 1 else None
        recursive_levels = 2 if student_levels > 1 else 1
        timing.start('students_query_and_serializer')
        students = Student.objects.filter(db_profile_id=db_profile_id).prefetch_related(prefetch_command)
        students = [s.serialize(recursive_levels=recursive_levels) for s in students]
        timing_data['students_query_and_serializer'] = timing.end('students_query_and_serializer')

    timing.start('custom_optimization_iterations')
    if teacher_levels > 0 and (class_levels > 0 or student_levels > 1 or (teacher_levels > 1 and student_levels == 1)):
        used_students = {}
        for teacher in teachers:
            this_teacher_classes = teacher['classes']
            for _class in this_teacher_classes:
                if include_students:
                    new_class = _class.copy()
                    this_class_students = new_class['students']
                    new_class['students'] = list(map(lambda s: s.copy(), _class['students']))
                    save_students_with_classes = []
                    if (students_with_classes is not None) or \
                            (students_with_classes_with_students is not None) or \
                            student_levels == 1:
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
                                save_students_with_classes.append(students_with_classes[student_id])
                            if students_with_classes_with_students is not None:
                                if student_id not in students_with_classes_with_students:
                                    new_student = student.copy()
                                    new_student['classes'] = [new_class]
                                    students_with_classes_with_students[student_id] = new_student
                                else:
                                    students_with_classes_with_students[student_id]['classes'].append(new_class)
                            if student_id not in used_students:
                                used_students[student_id] = True
                                if student_levels == 2:
                                    students.append(students_with_classes[student_id])
                                if student_levels == 3:
                                    students.append(students_with_classes_with_students[student_id])
                                if student_levels == 1:
                                    students.append(student)
                if class_levels == 3:
                    classes.append(dict(new_class, students=save_students_with_classes))
                elif class_levels == 2:
                    classes.append(new_class)
                elif class_levels == 1:
                    new_class = _class
                    if include_students:
                        new_class = _class.copy()
                        del new_class['students']
                    classes.append(new_class)
                if include_students and teacher_levels < 3:
                    del _class['students']
            if include_classes and teacher_levels == 1:
                del teacher['classes']

    if teacher_levels == 0 and (class_levels > 0 or student_levels == 3):
        if include_students:
            used_students = {}
            for _class in classes:
                save_students_with_classes = []
                for student in _class['students']:
                    student_id = student['student_id']
                    if students_with_classes is not None:
                        new_class_without_students = _class.copy()
                        del new_class_without_students['students']
                        if student_id not in students_with_classes:
                            new_student = student.copy()
                            new_student['classes'] = [new_class_without_students]
                            students_with_classes[student_id] = new_student
                        else:
                            students_with_classes[student_id]['classes'] \
                                .append(new_class_without_students)
                        save_students_with_classes.append(students_with_classes[student_id])
                    if students_with_classes_with_students is not None:
                        if student_id not in students_with_classes_with_students:
                            new_student = student.copy()
                            new_student['classes'] = [_class.copy()]
                            students_with_classes_with_students[student_id] = new_student
                        else:
                            students_with_classes_with_students[student_id]['classes'].append(_class.copy())
                    if student_id not in used_students:
                        used_students[student_id] = True
                        if student_levels == 2:
                            students.append(students_with_classes[student_id])
                        if student_levels == 3:
                            students.append(students_with_classes_with_students[student_id])
                        if student_levels == 1:
                            students.append(student)
                if class_levels == 3:
                    _class['students'] = save_students_with_classes
                elif class_levels == 1 and student_levels > 0:
                    del _class['students']

    timing_data['custom_optimization_iterations'] = timing.end('custom_optimization_iterations')

    if teacher_levels > 0:
        db_profile['teacher_set'] = teachers
    if class_levels > 0:
        db_profile['class_set'] = classes
    if student_levels > 0:
        db_profile['student_set'] = students

    return db_profile, timing_data
