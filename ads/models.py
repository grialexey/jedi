# -*- coding: utf-8 -*-
from django.db import models


class Ad(models.Model):
    SELL = "sell"
    BUY = "buy"
    OTHER = "other"
    AD_CATEGORY = (
        (SELL, u"Продажа"),
        (BUY, u"Покупка"),
        (OTHER, u"Разное")
    )

    id = models.IntegerField(primary_key=True, verbose_name=u"ID темы")
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"Заголовок")
    short_title = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"Короткий заголовок")
    category = models.CharField(max_length=10, choices=AD_CATEGORY, default=OTHER, verbose_name=u"Категория")
    price = models.PositiveIntegerField(blank=True, null=True, verbose_name=u"Цена")
    added = models.DateTimeField(verbose_name=u"Дата добавления")
    author = models.ForeignKey("Author", verbose_name=u"Автор")
    description = models.TextField(verbose_name=u"Текст объявления")

    class Meta:
        verbose_name = u"Объявление"
        verbose_name_plural = u"Объявления"
        ordering = ["-added", ]

    def __unicode__(self):
        return self.title


class Author(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name=u"ID на форуме")
    name = models.CharField(max_length=255, verbose_name=u"Имя")

    class Meta:
        verbose_name = u"Автор"
        verbose_name_plural = u"Авторы"

    def __unicode__(self):
        return self.name