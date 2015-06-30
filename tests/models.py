from __future__ import unicode_literals

from django.db import models
from trackmaven_django.models import BaseModel, ChangedModel


class TestModel(models.Model):
    text = models.CharField(max_length=100)

    class Meta:
        app_label = 'tests'
        abstract = True


class TestBaseModel(BaseModel, TestModel):
    pass


class TestChangedModel(ChangedModel, TestModel):
    pass
