from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.functional import cached_property

from featureflag.conf import get_settings


class TimestampedModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeatureFlag(TimestampedModel):
    name = models.CharField(max_length=100, unique=True)
    everyone = models.BooleanField(null=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.name} everyone={self.everyone}>"

    @classmethod
    def get(cls, name):
        try:
            return cls.objects.get(name=name)
        except cls.DoesNotExist:
            if get_settings("CREATE_MISSING"):
                return cls.objects.create(
                    name=name, everyone=get_settings("CREATE_DEFAULT", default=None)
                )
            raise

    def is_active(self, obj=None):
        if self.everyone:
            return True
        if self.everyone is False or obj is None:
            return False

        return obj in self.related_objects

    @cached_property
    def related_objects(self):
        return [obj.content_object for obj in self.flagged_objects.all()]


class FlaggedObject(TimestampedModel):
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, blank=True, null=True
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey()
    feature_flag = models.ForeignKey(
        FeatureFlag,
        related_name="flagged_objects",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    def __str__(self):
        return str(self.content_object)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.content_type} {self.object_id}>"
