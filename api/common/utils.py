import random
import string

def generate_unique_id(model_class, field_name="id", length=8):
    """
    Generate a unique ID for a given model class and field.
    
    :param model_class: The model class to check uniqueness against.
    :param field_name: The field in the model where uniqueness is required.
    :param length: The length of the generated ID (default is 8).
    :return: A unique ID.
    """
    while True:
        unique_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        if not model_class.objects.filter(**{field_name: unique_id}).exists():
            return unique_id
