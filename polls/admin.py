from django.contrib import admin
from .models import Poll, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

class PollAdmin(admin.ModelAdmin):
    list_display = ("question", "owner", "is_public", "created_at")
    prepopulated_fields = {"slug": ("question",)}
    inlines = [ChoiceInline]

admin.site.register(Poll, PollAdmin)
