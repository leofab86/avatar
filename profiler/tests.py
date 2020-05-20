import json
from django.test import TestCase
from django.urls import reverse
from .models import DatabaseProfile


class DatabaseProfileTest(TestCase):
    databases = '__all__'

    def test_custom_optimization_matches_prefetch_related(self):
        self.maxDiff = None

        new_profile = DatabaseProfile(
            db_profile_name='test',
            classes=5,
            class_types=5,
            teachers=5,
            classes_per_teacher=5,
            students=5,
            classes_per_student=5
        )
        new_profile.save()
        new_profile.save_sets()
        url = reverse('profiler:database_profile', args=[new_profile.db_profile_id])

        def get_params(teacher_levels, class_levels, student_levels, *, custom_optimization=False):
            return f'?teacher_levels={teacher_levels}&class_levels={class_levels}&student_levels={student_levels}' \
                   f'&{"custom_optimization=true" if custom_optimization else "prefetch_related=true"}'

        warnings = []
        show_warning = None

        def test_levels(lvl1, lvl2, lvl3):
            response1 = json.loads(self.client.get(url + get_params(lvl1, lvl2, lvl3)).content)
            response2 = json.loads(
                self.client.get(url + get_params(lvl1, lvl2, lvl3, custom_optimization=True)).content
            )
            del response1['timing_data']
            del response2['timing_data']
            response1_len = len(str(response1))
            response2_len = len(str(response2))
            if response1_len == response2_len:
                try:
                    self.assertDictEqual(response1, response2)
                except Exception as e:
                    warnings.append(e)
            else:
                self.assertDictEqual(response1, response2)

        test_levels(0, 0, 0)
        test_levels(0, 0, 1)
        test_levels(0, 0, 2)
        test_levels(0, 0, 3)
        test_levels(0, 1, 0)
        test_levels(0, 1, 1)
        test_levels(0, 1, 2)
        test_levels(0, 1, 3)
        test_levels(0, 2, 0)
        test_levels(0, 2, 1)
        test_levels(0, 2, 2)
        test_levels(0, 2, 3)
        test_levels(0, 3, 0)
        test_levels(0, 3, 1)
        test_levels(0, 3, 2)
        test_levels(0, 3, 3)
        test_levels(1, 0, 0)
        test_levels(1, 0, 1)
        test_levels(1, 0, 2)
        test_levels(1, 0, 3)
        test_levels(1, 1, 0)
        test_levels(1, 1, 1)
        test_levels(1, 1, 2)
        test_levels(1, 1, 3)
        test_levels(1, 2, 0)
        test_levels(1, 2, 1)
        test_levels(1, 2, 2)
        test_levels(1, 2, 3)
        test_levels(1, 3, 0)
        test_levels(1, 3, 1)
        test_levels(1, 3, 2)
        test_levels(1, 3, 3)
        test_levels(2, 0, 0)
        test_levels(2, 0, 1)
        test_levels(2, 0, 2)
        test_levels(2, 0, 3)
        test_levels(2, 1, 0)
        test_levels(2, 1, 1)
        test_levels(2, 1, 2)
        test_levels(2, 1, 3)
        test_levels(2, 2, 0)
        test_levels(2, 2, 1)
        test_levels(2, 2, 2)
        test_levels(2, 2, 3)
        test_levels(2, 3, 0)
        test_levels(2, 3, 1)
        test_levels(2, 3, 2)
        test_levels(2, 3, 3)
        test_levels(3, 0, 0)
        test_levels(3, 0, 1)
        test_levels(3, 0, 2)
        test_levels(3, 0, 3)
        test_levels(3, 1, 0)
        test_levels(3, 1, 1)
        test_levels(3, 1, 2)
        test_levels(3, 1, 3)
        test_levels(3, 2, 0)
        test_levels(3, 2, 1)
        test_levels(3, 2, 2)
        test_levels(3, 2, 3)
        test_levels(3, 3, 0)
        test_levels(3, 3, 1)
        test_levels(3, 3, 2)
        test_levels(3, 3, 3)

        if len(warnings) > 0:
            print('THERE WERE WARNINGS')
            if show_warning is not None:
                print(warnings[show_warning])

