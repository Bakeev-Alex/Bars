from django.db import models
from django.contrib.auth.models import User

from common.models import AbsActive


class StudyGroup(AbsActive):

    title = models.CharField('Название группы', max_length=250)

    class Meta:
        verbose_name = 'Учебная группа'
        verbose_name_plural = 'Учебные группы'

    def __str__(self):
        return self.title


class Student(User):

    study_group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, verbose_name='Учебная группа',
                                    related_name='student')

    class Meta:
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'

    def __str__(self):
        return self.username


class Professor(User):

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'

    def __str__(self):
        return self.username
