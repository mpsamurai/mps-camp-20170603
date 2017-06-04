from django.contrib import admin

# Register your models here.
from events import models

@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Document)
class DocumentAdmin(admin.ModelAdmin):
    pass

@admin.register(models.EventQuestions)
class EventQuestionsAdmin(admin.ModelAdmin):
    pass
