import textwrap

from django.db import models
from django.contrib.auth.models import User

from common.models import AbsDescription, AbsActive, AbsCreated, AbsSort


class Quiz(AbsDescription, AbsActive, AbsCreated, AbsSort):
    """
    Тест
    """

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'
        ordering = ['id']

    def __str__(self):
        return textwrap.shorten(self.title, width=80, placeholder=f'{self.title[:10]}...')


class Question(AbsDescription, AbsActive, AbsCreated, AbsSort):
    """
    Вопрос
    """

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name='Тест', related_name='questions')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return textwrap.shorten(self.title, width=80, placeholder=f'{self.title[:10]}...')


class Variant(AbsActive, AbsCreated, AbsSort):
    """
    Вариант ответа
    """

    questions = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос', related_name='variants')
    correct = models.BooleanField('Правильный ответ', default=False)
    title = models.CharField('Название', max_length=250)

    class Meta:
        verbose_name = 'Вариант'
        verbose_name_plural = 'Варианты'

    def __str__(self):
        return textwrap.shorten(self.title, width=80, placeholder=f'{self.title[:10]}...')


class UniqueValue(AbsCreated):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='unique_user')
    unique_value = models.CharField('Уникальный идентификатор теста', max_length=100)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name='Тест', related_name='unique_quiz', null=True, blank=True)

    class Meta:
        verbose_name = 'Уникальное значение'
        verbose_name_plural = 'Уникальные значения'

    def __str__(self):
        return self.unique_value


class Answer(AbsCreated):
    unique = models.ForeignKey(UniqueValue, on_delete=models.CASCADE, related_name='result_unique', verbose_name='Идентификатор теста')
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Вопрос', related_name='result_questions')
    variant = models.ForeignKey(Variant, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='', related_name='result_variant')
    correct_answer = models.BooleanField('Правильный ответ', default=False)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return f'Answer to the question-{self.question}'
