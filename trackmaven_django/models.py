from django.db import models


class BaseModel(models.Model):
    """
    Abstract model for models that require validation before saving.
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
        super(BaseModel, self).save(using='default', *args, **kwargs)
