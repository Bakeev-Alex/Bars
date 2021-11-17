from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from .models import Quiz, Question, Variant


class QuizEditForm(ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'is_active']


class QuestionsForm(ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'description', 'is_active', 'sort']


QuestionsFormSet = inlineformset_factory(Quiz, Question, can_delete=True, form=QuestionsForm)


class VariantsForm(ModelForm):
    class Meta:
        model = Variant
        fields = ['title', 'is_active', 'sort', 'questions', 'correct']


VariantsFormSet = inlineformset_factory(Question, Variant, can_delete=True, form=VariantsForm)