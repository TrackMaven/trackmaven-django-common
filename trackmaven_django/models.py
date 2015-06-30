from django.db import models
from django.forms.models import model_to_dict
from django.utils.encoding import force_text


class ChangedModelMixin(object):
    """
    A model mixin that tracks model fields' values and provide some useful
    tools to know what fields have been changed.

    Example:

        >>> c = Company()
        >>> c.has_changed
        False
        >>> c.changed_fields
        []
        >>> c.name = "Nike"
        >>> c.has_changed
        True
        >>> c.changed_fields
        ['name']
        >>> c.diff
        {'name': (None, 'Nike')}

    """

    def __init__(self, *args, **kwargs):
        super(ChangedModelMixin, self).__init__(*args, **kwargs)
        self.__initial = self.to_dict

    @property
    def diff(self):
        """
        Returns a dictionary of all fields whose values have changed and for
        each a tuple of the original vs new field values.

        Example:

            >>> p = Post()
            >>> p.diff
            {}
            >>> p.url = "http://trackmaven.com"
            >>> p.diff
            {
                'url': (None, "http://trackmaven.com")
            }
        """
        d1 = self.__initial
        d2 = self.to_dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if force_text(v) != force_text(d2[k])]
        return dict(diffs)

    @property
    def has_changed(self):
        """
        Returns a boolean indicating if the model's field values have changed.

        Example:

            >>> p = Post.objects.get(pk=1)
            >>> p.has_changed
            False
            >>> p.url = "http://trackmaven.com"
            >>> p.has_changed
            True

        """
        return bool(self.diff)

    @property
    def changed_fields(self):
        """
        Returns a list of the changed fields.

        Example:

            >>> p = Post.objects.get(pk=1)
            >>> p.changed_fields
            []
            >>> p.url = "http://trackmaven.com"
            >>> p.changed_fields
            ["url"]
        """
        return self.diff.keys()

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        super(ChangedModelMixin, self).save(*args, **kwargs)
        self.__initial = self.to_dict

    @property
    def to_dict(self):
        """
        Transform the model into a dictionary.

        Example:

            >>> p = Post(url="http://trackmaven.com", title="Hello")
            >>> p.to_dict
            {"url": "http://trackmaven.com", "title": "Hello"}

        """
        return model_to_dict(
            self, fields=[field.name for field in self._meta.fields])


class BaseModel(models.Model):
    """
    Abstract model for models that require validation before saving.

    Example:

        ::

            from trackmaven_django.models import BaseModel

            class Post(BaseModel):
                text = models.TextField()
                ...

    """
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Tries to clean the model and its fields before saving to avoid database
        errors that might occur from forcing a field to something that doesn't
        follow the DB schema e.g. a string too long for a field.
        """
        self.full_clean()
        super(BaseModel, self).save(*args, **kwargs)


class ChangedModel(ChangedModelMixin, BaseModel):
    """
    Abstract model that combines BaseModel + ChangedModelMixin.
    Includes pre-save validation + ability to see changes on a model.

    Example:

        ::

            from trackmaven_django.models import ChangedModel

            class Post(ChangedModel):
                text = models.TextField()
                ...

    """
    class Meta:
        abstract = True
