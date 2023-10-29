from django.db import models
from datetime import datetime
from django.urls import reverse


class Bot(models.Model):
    """ bot """
    title = models.CharField(verbose_name="Заголовок", max_length=150, unique=True)
    token = models.CharField(verbose_name="Токен", max_length=160, unique=True)
    description = models.TextField("Описание", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.token

    class Meta:
        verbose_name = "Бот"
        verbose_name_plural = "Бот"
        ordering = ['id']

class Chat(models.Model):
    """ chat_id """
    name = models.CharField(verbose_name="Админ", max_length=150, unique=True)
    chat_id = models.BigIntegerField(verbose_name="Чат", unique=True)
    token = models.ForeignKey(Bot, verbose_name="Токен", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Чат"
        verbose_name_plural = "Чат"
        ordering = ['id']