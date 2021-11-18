from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from .models import Quiz, Question, Variant


class QuizEditForm(ModelForm):
    """
    Тест. Поля:
    'title' - Название
    'description' - Описание
    'is_active' - Активность
    """
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'is_active']


class QuestionsForm(ModelForm):
    """
    Вопрос. Поля:
    'title' - Название
    'description' - Описание
    'is_active' - Активность
    'sort' - Сортировка
    """
    class Meta:
        model = Question
        fields = ['title', 'description', 'is_active', 'sort']


# FormSet для теста и вопросов
QuestionsFormSet = inlineformset_factory(Quiz, Question, can_delete=True, form=QuestionsForm)


class VariantsForm(ModelForm):
    """
    Варианты ответа. Поля:
    'title' - Название
    'description' - Описание
    'is_active' - Активность
    'sort' - Сортировка
    'questions' - Варианты ответа
    'correct' - Правильный ответ
    """
    class Meta:
        model = Variant
        fields = ['title', 'is_active', 'sort', 'questions', 'correct']


# FormSet для вопроса и вариантов ответа
VariantsFormSet = inlineformset_factory(Question, Variant, can_delete=True, form=VariantsForm)