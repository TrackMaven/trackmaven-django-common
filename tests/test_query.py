from .models import TestBaseModel
from trackmaven_django.query import get_object_or_make
import pytest


@pytest.mark.django_db
def test_get_object_or_make_existing():
    instance = TestBaseModel.objects.create(text="test")
    retrieved_instance, existing = get_object_or_make(TestBaseModel, text="test")
    assert instance == retrieved_instance
    assert existing is True


@pytest.mark.django_db
def test_get_object_or_make_not_existing():
    instance, existing = get_object_or_make(TestBaseModel, text="test")
    assert instance.text == "test"
    assert existing is False
