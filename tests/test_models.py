from django.core.exceptions import ValidationError
from .models import TestBaseModel, TestChangedModel

import pytest


def test_has_changed():
    instance = TestChangedModel()
    assert instance.has_changed is False
    instance.text = "Hello"
    assert instance.has_changed is True


def test_changed_fields():
    instance = TestChangedModel()
    assert instance.changed_fields == []
    instance.text = "Hello"
    assert instance.changed_fields == ["text"]


def test_diff():
    instance = TestChangedModel()
    assert instance.diff == {}
    instance.text = "Hello"
    assert instance.diff == {
        "text": ("", "Hello")
    }


def test_full_clean():
    with pytest.raises(ValidationError):
        instance = TestBaseModel(text="hello" * 1024)
        instance.save()


def test_changed_model_full_clean():
    with pytest.raises(ValidationError):
        instance = TestChangedModel(text="hello" * 1024)
        instance.save()
