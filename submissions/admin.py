from django.contrib import admin
from .models import PlantDiagnosis, StoredDiagnosis

@admin.register(PlantDiagnosis)
class PlantDiagnosisAdmin(admin.ModelAdmin):
    list_display = ('diagnosis_title', 'user', 'created_at')
    search_fields = ('diagnosis_title', 'health_condition', 'user__username')
    list_filter = ('created_at',)

@admin.register(StoredDiagnosis)
class StoredDiagnosisAdmin(admin.ModelAdmin):
    list_display = ('name', 'diagnosis_title')
    search_fields = ('name', 'diagnosis_title', 'health_condition')
