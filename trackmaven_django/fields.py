from django.db import models
from django.core import exceptions
from django import forms
from django.utils.text import capfirst
from django.utils.six import with_metaclass


class MultiSelectFormField(forms.MultipleChoiceField):
    widget = forms.SelectMultiple


# Ensure it works with python 2 and 3
# https://docs.djangoproject.com/en/1.7/howto/custom-model-fields/#the-subfieldbase-metaclass
class MultipleChoiceField(with_metaclass(models.SubfieldBase, models.Field)):
    """
    Django Custom Field for MultipleChoiceField. Behind the scenes stores
    a list as a comma seperated string.

    Example:

       ::

        from django.db import models
        from trackmaven_django.fields import MultipleChoiceField

        VALID_CHOICES = [
            'a',
            'b'
        ]

        class ExampleModel(models.Model):
            channels = MultipleChoiceField(
                default=['a'], choices=VALID_CHOICES)
    """
    description = "A Django Custom field for storing a list of pre-set choices"

    def __init__(self, *args, **kwargs):
        kwargs['null'] = True
        super(MultipleChoiceField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'required': not self.blank,
            'label': capfirst(self.verbose_name),
            'help_text': self.help_text,
            'choices': sorted(self.choices),
        }
        if self.has_default():
            defaults['initial'] = self.get_default()
        defaults.update(kwargs)
        return MultiSelectFormField(**defaults)

    def get_internal_type(self):
        # DB wise it is stored and handled just like a TextField
        return "TextField"

    def to_python(self, value):
        if value is None:
            cleaned = []
        elif isinstance(value, list):
            cleaned = value
        else:
            if len(value) == 0:
                cleaned = []
            else:
                cleaned = value.split(',')
        cleaned = sorted(cleaned)
        self.validate(cleaned)
        return cleaned

    def get_prep_value(self, value):
        if value is None:
            return None
        elif (isinstance(value, str) or
              isinstance(value, bytes) or isinstance(value, bytearray)):
            cleaned = sorted(value.split(','))
            return ','.join(cleaned)
        elif isinstance(value, list):
            return ','.join(sorted(value))
        else:
            raise Exception('Invalid value type')

    def get_prep_lookup(self, lookup_type, value):
        if lookup_type == 'exact':
            return self.get_prep_value(sorted(value))
        else:
            raise TypeError(
                'Lookup type {} not supported.'.format(lookup_type))

    def validate(self, value):
        for item in value:
            if item not in sorted(self.choices):
                raise exceptions.ValidationError('invalid_choice: %s' % item)
