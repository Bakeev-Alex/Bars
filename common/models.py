from django.db import models


class AbsDescription(models.Model):
    """
    Модель, текстовые описания объекта
    """
    title = models.CharField('Название', max_length=250)
    description = models.TextField('Описание', blank=True, default='')

    class Meta:
        abstract = True


class AbsActive(models.Model):
    """
    Модель, для апределения активности объекта
    """

    is_active = models.BooleanField('Активность', default=True)

    class Meta:
        abstract = True


class AbsCreated(models.Model):
    """
    Модель, для отслеживания даты создания и изменения объекта
    """

    create = models.DateTimeField('Дата создания', auto_now_add=True)
    update = models.DateTimeField('Дата изменения', auto_now=True)

    class Meta:
        abstract = True


class AbsSort(models.Model):
    """
    Модель, для корректной сортировки объектов
    """

    sort = models.IntegerField('Сортировка', default=0, help_text='Чем ниже число, тем приоритетнее позиция. '
                                                                  'Допустимо использование знака "минус".')

    class Meta:
        abstract = True
        ordering = ['sort', ]