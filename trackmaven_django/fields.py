from django.utils.text import capfirst
from django.core import exceptions
from django.forms import MultipleChoiceField as MultiChoiceFormField
from django.contrib.postgres.fields import ArrayField


class MultipleChoiceField(ArrayField):
    description = "A field for storing a list of pre-set choices"

    def __init__(self, *args, **kwargs):
        super(MultipleChoiceField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'required': not self.blank,
                    'label': capfirst(self.verbose_name),
                    'help_text': self.help_text, 'choices': self.choices}
        if self.has_default():
            defaults['initial'] = self.get_default()
        defaults.update(kwargs)
        return MultiChoiceFormField(**defaults)

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
                    self.error_messages['invalid_choice'] % value)
