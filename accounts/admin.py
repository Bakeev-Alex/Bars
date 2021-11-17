from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import StudyGroup, Student, Professor


@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']


@admin.register(Student)
class StudentAdmin(UserAdmin):
    list_display = ['username', 'study_group', 'is_active']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', ('study_group', 'is_active'))}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'study_group'),
        }),
    )
    readonly_fields = ['groups', ]


@admin.register(Professor)
class ProfessorAdmin(UserAdmin):
    list_display = ['username', 'is_active']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    readonly_fields = ['groups', ]
