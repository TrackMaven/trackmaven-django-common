Changelog
=========

Version <X>
-----------

<YYYY-MM-DD>

<Short description of what has changed>

- <List of changes>
- <One by one>

Version 1.0.0
-------------

2016-02-18

Bug fixes:
- Fixed an issue with the MultipleChoiceField where input were not validated.
- Fixed an issue with the MultipleChoiceField which did not allow an empty value.

Migration:
- Changed the `choices` of the MultipleChoiceField to be a single iterable (instead of nested tuples).

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


Version 0.0.3
-------------

2016-02-18

Improvements:
- Added fields.MultipleChoiceField


Version 0.0.2
-------------

2015-06-30

Initial release

- Added `ChangedModel`
- Added `get_object_or_make`
- Added docs
