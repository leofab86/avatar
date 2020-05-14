from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from profiler.models import Student, Teacher, DatabaseProfile, Class


class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = ('student_id', 'student_name', 'classes')

    def __init__(self, *args, children=None, full_children=None, **kwargs):
        super(StudentSerializer, self).__init__(*args, **kwargs)
        if children is False:
            del self.fields['classes']
        if full_children is True:
            self.fields['classes'] = ClassSerializer(many=True, read_only=True, children=False)


class ClassSerializer(ModelSerializer):
    students = PrimaryKeyRelatedField(source='student_set', many=True, read_only=True)

    class Meta:
        model = Class
        fields = ('class_id', 'class_type', 'teacher', 'students')

    def __init__(self, *args, children=None, full_children=None, **kwargs):
        super(ClassSerializer, self).__init__(*args, **kwargs)
        if children is False:
            del self.fields['students']
        if full_children is True:
            self.fields['students'] = StudentSerializer(source='student_set', many=True, read_only=True, children=False)


class TeacherSerializer(ModelSerializer):
    classes = PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Teacher
        fields = ('teacher_id', 'teacher_name', 'classes')

    def __init__(self, *args, **kwargs):
        children = kwargs.pop('children', None)
        full_children = kwargs.pop('full_children', None)
        super(TeacherSerializer, self).__init__(*args, **kwargs)
        if children is False:
            del self.fields['classes']
        if full_children is True:
            self.fields['classes'] = ClassSerializer(many=True, read_only=True, children=False)


class DatabaseProfileSerializer(ModelSerializer):
    class Meta:
        model = DatabaseProfile
        response_fields = (
            'db_profile_name',
            'db_profile_id',
            'teachers',
            'classes',
            'students',
            'completion_progress'
        )
        create_request_fields = response_fields + (
            'class_types',
            'classes_per_teacher',
            'classes_per_student'
        )

    def __init__(self,  *args, children=None, recursive_children=None, full_recursive_children=None, **kwargs):
        if "data" in kwargs:
            self.Meta.fields = self.Meta.create_request_fields
        else:
            self.Meta.fields = self.Meta.response_fields
        super(DatabaseProfileSerializer, self).__init__(*args, **kwargs)
        if children:
            children_fields = {
                'classes': ClassSerializer(source='class_set', many=True, read_only=True, children=False),
                'teachers': TeacherSerializer(source='teacher_set', many=True, read_only=True, children=False),
                'students': StudentSerializer(source='student_set', many=True, read_only=True, children=False)
            }
            for child in children:
                self.fields[f'{child}_set'] = children_fields[child]
        if recursive_children:
            recursive_children_fields = {
                'classes': ClassSerializer(source='class_set', many=True, read_only=True, children=True),
                'teachers': TeacherSerializer(source='teacher_set', many=True, read_only=True, children=True),
                'students': StudentSerializer(source='student_set', many=True, read_only=True, children=True)
            }
            for child in recursive_children:
                self.fields[f'{child}_set'] = recursive_children_fields[child]
        if full_recursive_children:
            full_recursive_children_fields = {
                'classes': ClassSerializer(source='class_set', many=True, read_only=True, full_children=True),
                'teachers': TeacherSerializer(source='teacher_set', many=True, read_only=True, full_children=True),
                'students': StudentSerializer(source='student_set', many=True, read_only=True, full_children=True)
            }
            for child in full_recursive_children:
                self.fields[f'{child}_set'] = full_recursive_children_fields[child]
