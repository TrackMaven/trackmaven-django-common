from __future__ import unicode_literals

from django.db import models
from trackmaven_django.models import BaseModel, ChangedModel
from trackmaven_django.fields import MultipleChoiceField


class TestModel(models.Model):
    text = models.CharField(max_length=100)

    class Meta:
        app_label = 'tests'
        abstract = True


class TestBaseModel(BaseModel, TestModel):
    pass


class TestChangedModel(ChangedModel, TestModel):
    pass


VALID_CHOICES = [
    'a',
    'b',
]


class TestMultipleChoiceModel(models.Model):
    many = MultipleChoiceField(choices=VALID_CHOICES)
    many_default = MultipleChoiceField(choices=VALID_CHOICES, default=['b'])
