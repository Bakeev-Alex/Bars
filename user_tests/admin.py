import nested_admin

from django.contrib import admin

from .models import Quiz, Question, Variant


class VariantsAdmin(nested_admin.NestedStackedInline):
    model = Variant
    fields = ('title', 'is_active', 'correct')
    extra = 0
    classes = ['collapse']


class QuestionsAdmin(nested_admin.NestedStackedInline):
    model = Question
    fields = ('title', 'description', 'is_active')
    extra = 0
    classes = ['collapse']
    inlines = (VariantsAdmin,)


@admin.register(Quiz)
class QuizAdmin(nested_admin.NestedModelAdmin):
    list_display = ('title', 'description', 'is_active')
    fieldsets = (
        (None, {'fields': ('title', 'description', ('sort', 'is_active'),
                           ('create', 'update'))}),
    )
    readonly_fields = ('create', 'update')
    inlines = [QuestionsAdmin, ]


@admin.register(Question)
class QuestionsAdmin(nested_admin.NestedModelAdmin):
    list_display = ('title', 'description', 'is_active')
    inlines = (VariantsAdmin, )
