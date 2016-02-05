import mock
from django import test
from django.core.exceptions import ValidationError
from trackmaven_django import fields

VALID_CHANNEL_NAMES = (
    ('input1', 'input1'),
    ('input2', 'input2'),
    ('input3', 'input3'),
    ('input4', 'input4'),
    ('input5', 'input5'),
    ('input6', 'input6'),
    ('input7', 'input7'),
    ('input8', 'input8'),
    ('input9', 'input9'),
    ('input10', 'input10'),
    ('input11', 'input11'),
    ('input12', 'input12'),
    ('input13', 'input13'),
    ('input14', 'input14'),
)

LIST_OF_CHANNELS = ['input1', 'input2', 'input3', 'input4', 'input5',
                    'input6', 'input7', 'input8', 'input9', 'input10',
                    'input11', 'input12', 'input13', 'input14']


class TestMultipleChoiceField(test.TestCase):
    def test_to_python(self):
        f = fields.MultipleChoiceField(
                choices=VALID_CHANNEL_NAMES)
        self.assertEqual(f.to_python('input1'), ['input1'])
        self.assertEqual(f.to_python('input1,input2,input4'),
                         ['input1', 'input2', 'input4'])

    def test_default(self):
        f = fields.MultipleChoiceField(
                choices=VALID_CHANNEL_NAMES,
                default='input1,input2,input4')
        self.assertEqual(f.get_default(), 'input1,input2,input4')

    def test_get_prep_value(self):
        f = fields.MultipleChoiceField(
                choices=VALID_CHANNEL_NAMES,
                default='input1,input2,input4')
        self.assertEqual(f.get_prep_value('input1'), 'input1')
        self.assertEqual(f.get_prep_value(['input1', 'input2', 'input4']),
                         'input1,input2,input4')

    def test_get_prep_lookup(self):
        f = fields.MultipleChoiceField(
                choices=VALID_CHANNEL_NAMES,
                default='input1,input2,input4')
        self.assertEqual(f.get_prep_lookup('exact', 'input1'), 'input1')
        self.assertEqual(f.get_prep_lookup('exact', 'input1'), 'input1')
        self.assertEqual(f.get_prep_lookup('in', ['input1']), ['input1'])
        self.assertEqual(
                f.get_prep_lookup('exact',
                                  'input1,input2,input4'),
                'input1,input2,input4'
            )
        self.assertEqual(
                f.get_prep_lookup('exact',
                                  ['input1', 'input2', 'input4']),
                'input1,input2,input4'
            )

    def test_get_choices_default(self):
        f = fields.MultipleChoiceField(
                choices=VALID_CHANNEL_NAMES)
        self.assertEqual(tuple(f.get_choices_default()), VALID_CHANNEL_NAMES)

    def test_get_choices_selected(self):
        f = fields.MultipleChoiceField(
                choices=VALID_CHANNEL_NAMES)
        self.assertEqual(f.get_choices_selected(VALID_CHANNEL_NAMES),
                         LIST_OF_CHANNELS)

    def test_validate(self):
        f = fields.MultipleChoiceField(
                choices=VALID_CHANNEL_NAMES)
        fake_model = mock.Mock()
        self.assertEqual(f.validate(['input1', 'input2'], fake_model), None)
        with self.assertRaises(ValidationError):
            f.validate(['giant', 'safeway'], fake_model)
