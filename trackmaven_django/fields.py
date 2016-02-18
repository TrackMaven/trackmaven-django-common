from django.db import models
from django.core import exceptions
from django import forms
from django.utils.text import capfirst


class MultiSelectFormField(forms.MultipleChoiceField):
    widget = forms.SelectMultiple


class MultipleChoiceField(models.Field):
    """
    Django Custom Field for MultipleChoiceField

    Example:

       ::

          from django.db import models
          from trackmaven_drf.django_fields import MultipleChoiceField


          class ExampleModel(models.Model):
          channels = MultipleChoiceField(default='facebook,twitter,instagram',
                                   choices=settings.VALID_CHANNEL_NAMES)
    """
    description = "A Django Custom field for storing a list of pre-set choices"
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        super(MultipleChoiceField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'required': not self.blank,
                    'label': capfirst(self.verbose_name),
                    'help_text': self.help_text, 'choices': self.choices}
        if self.has_default():
            defaults['initial'] = self.get_default()
        defaults.update(kwargs)
        return MultiSelectFormField(**defaults)

    def get_internal_type(self):
        # DB wise it is stored and handled just like a TextField
        return "TextField"

    def to_python(self, value):
        if isinstance(value, list):
            return value
        else:
            return value.split(',')

    def get_prep_value(self, value):
        if (isinstance(value, str) or
                isinstance(value, bytes) or isinstance(value, bytearray)):
            return value
        elif isinstance(value, list):
            return ','.join(value)
        else:
            raise Exception('Invalid value type')

    def get_prep_lookup(self, lookup_type, value):
        if lookup_type == 'exact':
            return self.get_prep_value(value)
        elif lookup_type == 'in':
            return [self.get_prep_value(v) for v in value]
        else:
            raise TypeError(
                    'Lookup type {} not supported.'.format(lookup_type))

    def get_choices_selected(self, arr_choices=''):
        if not arr_choices:
            return False
        return [choice[0] for choice in arr_choices]

    def get_choices_default(self):
        # Don't want blanks included since this is a multi select
        return self.get_choices(include_blank=False)

    def contribute_to_class(self, cls, name):
        # Fixes get_field_display for multiple choice fields
        super(MultipleChoiceField, self).contribute_to_class(cls, name)
        if self.choices:
            func = (lambda self, fieldname=name,
                    choicedict=dict(self.choices): ",".join(
                        [choicedict.get(value, value) for value in getattr(
                            self, fieldname)]))
            setattr(cls, 'get_%s_display' % self.name, func)

    def validate(self, value, model_instance):
        arr_choices = self.get_choices_selected(self.get_choices_default())
        for choice in value:
            if choice not in arr_choices:
                raise exceptions.ValidationError(
                        'invalid_choice: %s' % value)
