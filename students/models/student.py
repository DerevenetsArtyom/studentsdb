# -*- coding: utf-8 -*-
# Allow us to use cyrillic text
from django.db import models


class Student(models.Model):

    """Student Model"""

    # Customisation model's behavior :
    # table's structure / view at admin
    class Meta(object):
        # Clear, readable names in admin interface
        verbose_name = u"Студент"
        verbose_name_plural = u"Студенти"
        ordering = ['last_name']

    # Represents human-readable information
    # __str__ in Python 3
    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)

    # string field ~ VARCHAR
    first_name = models.CharField(
        max_length=256,
        blank=False,
        # name at user/admin interface
        verbose_name=u"Ім'я")

    # string field ~ VARCHAR
    last_name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Прізвище")

    # string field ~ VARCHAR
    middle_name = models.CharField(
        max_length=256,
        blank=True,
        verbose_name=u"По-батькові",
        # useful thing. Set default if blank==True
        default='')

    # date field ~ DATE
    birthday = models.DateField(
        blank=False,
        verbose_name=u"Дата народження",
        # Can be empty
        null=True)

    # Image from file system (MEDIA_ROOT)
    # Django doesn't save binary files in the base
    # Use Pillow library
    photo = models.ImageField(
        blank=True,
        verbose_name=u"Фото",
        null=True)

    # string field ~ VARCHAR
    ticket = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Білет")

    # Long text. Without definite length
    notes = models.TextField(
        blank=True,
        verbose_name=u"Додаткові нотатки")

    #
    student_group = models.ForeignKey('Group',
        verbose_name=u"Група",
        blank=False,
        null=True,
        on_delete=models.PROTECT)
