import pytest
from django import test
from django.core.exceptions import ValidationError
from trackmaven_django import fields
from .models import TestMultipleChoiceModel


VALID_CHOICES = [
    'a', 'b', 'c',
]


class TestMultipleChoiceField(test.TestCase):
    def test_to_python(self):
        f = fields.MultipleChoiceField(choices=VALID_CHOICES)
        self.assertEqual(f.to_python('a'), ['a'])
        self.assertEqual(f.to_python('a,b,c'), ['a', 'b', 'c'])
        self.assertEqual(f.to_python('b,a,c'), ['a', 'b', 'c'])
        self.assertEqual(f.to_python(None), [])

    def test_default(self):
        f = fields.MultipleChoiceField(choices=VALID_CHOICES, default=['a'])
        self.assertEqual(f.get_default(), ['a'])

    def test_get_prep_value(self):
        f = fields.MultipleChoiceField(choices=VALID_CHOICES, default='a,b,c')
        self.assertEqual(f.get_prep_value('a'), 'a')
        self.assertEqual(f.get_prep_value(['a', 'b', 'c']), 'a,b,c')
        self.assertEqual(f.get_prep_value(['c', 'b', 'a']), 'a,b,c')
        self.assertEqual(f.get_prep_value(None), None)

    def test_get_prep_lookup(self):
        f = fields.MultipleChoiceField(choices=VALID_CHOICES, default='a,b,c')
        self.assertEqual(f.get_prep_lookup('exact', 'a'), 'a')
        self.assertEqual(f.get_prep_lookup('exact', ['a', 'b', 'c']), 'a,b,c')
        self.assertEqual(f.get_prep_lookup('exact', ['b', 'c', 'a']), 'a,b,c')

    def test_validate(self):
        f = fields.MultipleChoiceField(choices=VALID_CHOICES)
        self.assertEqual(f.validate(['a', 'b']), None)
        with self.assertRaises(ValidationError):
            f.validate(['giant', 'safeway'])


class TestMultipleChoiceFieldModel(test.TestCase):
    def test_valid(self):
        model = TestMultipleChoiceModel()
        model.many = ['a']
        model.save()
        assert model.many == ['a']

    def test_invalid(self):
        model = TestMultipleChoiceModel()
        with pytest.raises(ValidationError):
            model.many = ['c']

    def test_none(self):
        model = TestMultipleChoiceModel(many=None)
        assert model.many == []

    def test_exact_one(self):
        model = TestMultipleChoiceModel.objects.create(many=['a', 'b'])
        result = TestMultipleChoiceModel.objects.get(many=['a', 'b'])
        assert result == model
        result = TestMultipleChoiceModel.objects.get(many=['b', 'a'])
        assert result == model
        result = TestMultipleChoiceModel.objects.filter(many=['a'])
        assert list(result) == []

    def test_exact_none(self):
        model = TestMultipleChoiceModel.objects.create(many=None)
        result = TestMultipleChoiceModel.objects.get(many=[])
        assert result == model
        result = TestMultipleChoiceModel.objects.filter(many=['a'])
        assert list(result) == []

    def test_exact_default(self):
        model = TestMultipleChoiceModel.objects.create(many=None)
        result = TestMultipleChoiceModel.objects.get(many_default=['b'])
        assert result == model
