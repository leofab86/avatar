from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from profiler.models.school_system import Student, Teacher, DatabaseProfile, Class


class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = ('student_id', 'student_name', 'classes')

    def __init__(self, *args, recursive_levels=None, **kwargs):
        super(StudentSerializer, self).__init__(*args, **kwargs)
        if recursive_levels == 1 and 'classes' in self.fields:
            del self.fields['classes']
        if recursive_levels and recursive_levels > 1:
            new_recursive_levels = recursive_levels - 1
            self.fields['classes'] = ClassSerializer(
                many=True, read_only=True, recursive_levels=new_recursive_levels
            )


class ClassSerializer(ModelSerializer):
    students = PrimaryKeyRelatedField(source='student_set', many=True, read_only=True)

    class Meta:
        model = Class
        fields = ('class_id', 'class_type', 'teacher', 'students')

    def __init__(self, *args, recursive_levels=None, **kwargs):
        super(ClassSerializer, self).__init__(*args, **kwargs)
        if recursive_levels == 1 and 'students' in self.fields:
            del self.fields['students']
        if recursive_levels and recursive_levels > 1:
            new_recursive_levels = recursive_levels - 1
            self.fields['students'] = StudentSerializer(
                source='student_set', many=True, read_only=True, recursive_levels=new_recursive_levels
            )


class TeacherSerializer(ModelSerializer):
    classes = PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Teacher
        fields = ('teacher_id', 'teacher_name', 'classes')

    def __init__(self, *args, recursive_levels=None, **kwargs):
        super(TeacherSerializer, self).__init__(*args, **kwargs)
        if recursive_levels == 1 and 'classes' in self.fields:
            del self.fields['classes']
        if recursive_levels and recursive_levels > 1:
            new_recursive_levels = recursive_levels - 1
            self.fields['classes'] = ClassSerializer(
                many=True, read_only=True, recursive_levels=new_recursive_levels
            )


class DatabaseProfileSerializer(ModelSerializer):
    class Meta:
        model = DatabaseProfile
        response_fields = (
            'db_profile_name',
            'db_profile_id',
            'teachers',
            'classes',
            'students',
            'completion_progress',
        )
        create_request_fields = response_fields + (
            'class_types',
            'classes_per_teacher',
            'classes_per_student'
        )

    def __init__(self, *args, teacher_levels=None, class_levels=None, student_levels=None, **kwargs):
        if "data" in kwargs:
            self.Meta.fields = self.Meta.create_request_fields
        else:
            self.Meta.fields = self.Meta.response_fields

        super(DatabaseProfileSerializer, self).__init__(*args, **kwargs)

        if teacher_levels:
            self.fields['teacher_set'] = TeacherSerializer(many=True, read_only=True, recursive_levels=teacher_levels)
        if class_levels:
            self.fields['class_set'] = ClassSerializer(many=True, read_only=True, recursive_levels=class_levels)
        if student_levels:
            self.fields['student_set'] = StudentSerializer(many=True, read_only=True, recursive_levels=student_levels)

