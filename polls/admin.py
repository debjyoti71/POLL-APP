from django.contrib import admin
from .models import Poll, Choice, User

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

class PollAdmin(admin.ModelAdmin):
    list_display = ("question", "owner", "is_public", "created_at")
    prepopulated_fields = {"slug": ("question",)}
    inlines = [ChoiceInline]

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'created_at', 'super_user')
    search_fields = ('username', 'email')
    ordering = ('created_at',)

admin.site.register(User, UserAdmin)
admin.site.register(Poll, PollAdmin)
