from django.contrib import admin
from import_export.admin import ImportExportModelAdmin


class NovadataModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    ...
