from django.contrib import admin
from .models import SubmissionData, LanguageData, savedCodeData, savedNoteData

admin.site.register(LanguageData)
admin.site.register(SubmissionData)
admin.site.register(savedCodeData)
admin.site.register(savedNoteData)