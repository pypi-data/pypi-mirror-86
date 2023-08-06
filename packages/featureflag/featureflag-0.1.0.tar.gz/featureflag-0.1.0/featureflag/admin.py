from django.contrib import admin
from django.db.models import Count

from featureflag.models import FeatureFlag, FlaggedObject


class FlaggedObjectInline(admin.TabularInline):
    model = FlaggedObject
    extra = 1


@admin.register(FeatureFlag)
class FeatureFlagAdmin(admin.ModelAdmin):
    inlines = (FlaggedObjectInline,)
    search_fields = ("name",)
    list_display = ("name", "everyone", "created_at", "updated_at", "total_objects")

    def get_queryset(self, request):
        queryset = super(FeatureFlagAdmin, self).get_queryset(request)
        return queryset.annotate(total_objects=Count("flagged_objects"))

    def total_objects(self, obj):
        return obj.total_objects

    total_objects.short_description = "Flagged Objects"
