from django.db import models
import uuid

class UniqueStringIDField(models.CharField):
    """
    Custom AutoField for generating unique string IDs.
    """

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 36)  # Default to UUID length
        kwargs['default'] = kwargs.get('default', self.generate_unique_id)
        kwargs['editable'] = kwargs.get('editable', False)
        kwargs['unique'] = kwargs.get('unique', True)
        super().__init__(*args, **kwargs)

    def generate_unique_id(self):
        return str(uuid.uuid4())  # You can replace with custom unique ID generator
