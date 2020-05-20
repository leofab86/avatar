
class ProfilerRouter:
    def db_for_read(self, model, **hints):
        """Point all operations on profiler models to 'profiler' db"""
        if model._meta.app_label == 'profiler':
            return 'profiler'
        return 'default'

    def db_for_write(self, model, **hints):
        """Point all operations on profiler models to 'profiler' db"""
        if model._meta.app_label == 'profiler':
            return 'profiler'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """Allow any relation if a both models in profiler app"""
        # if obj1._meta.app_label == 'profiler' and obj2._meta.app_label == 'profiler':
        #     return True

        """This allows test database creation."""
        if obj1._meta.app_label == 'contenttypes' and obj2._meta.app_label == 'auth':
            return True

        # return None should default correctly to only allowing relations between models associated with same database
        # allowing relations may be helpful for cases of replica databases
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'profiler':
            return db == 'profiler'
        return None
