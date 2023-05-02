from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Action(models.Model): # Название таблицы в базе данных

    STATUS_CHOICE = (
        ('опубликовано', 'Опубликовано'),
        ('неопубликовано', 'Неопубликовано'),
    )

    title = models.CharField( # CharField - поле с буквенными символами в базе данных
        max_length=100, # Лимит на количество символов содержащихся в поле
        null=True, # Может ли поле содержать пустое (null) значение
        blank=True, # Будт ли необходимым заполнять поле в формах
        verbose_name='Заголовок задачи', # Название поля в админ панели
    )

    slug = models.SlugField( # SlugField - поле хранящее уникальное отображение названия в ссылке
        max_length=255,
        unique_for_date='publish', # Обеспечение уникальности каждой записи из todo list
        verbose_name='Ссылка на запись',
    )

    user = models.ForeignKey( # ForeignKey - внешний ключ-ссылка, связывающая пользователя и запись
        User, # Модель пользователя Django (не кастомная)
        on_delete=models.CASCADE, # Особенность удаления записей связанных с данным автором (вытекает напрямую из SQL)
        related_name='todo_action', # Обратная связь от User'a к Action - можно получить доступ к связанным объектам автора
    )

    content = models.TextField(
        verbose_name='Контент задачи',
    )

    publish = models.DateTimeField( # DateTimeField - поле содержащее дату и точное время поля
        default=timezone.now(), # Время публикации записи (то же самое что и datetime.now(), только с учетом зоны)
        verbose_name='Время публикации'
    )

    created = models.DateTimeField(
        auto_now_add=True, # Создает временную метку в тот момент, когда запись появляется в базе данных
        verbose_name='Время создания задачи', # Название поля в админ панели
    )

    updated = models.DateTimeField(
        auto_now=True, # Дата сохраняется автоматически при сохранении объекта
        verbose_name='Время изменения задачи',
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICE,
        default='опубликовано',
    )

    class Meta:
        ordering = ['-publish'] # Порядок вывода записей в админ панели
        verbose_name = 'Список дел' # Название для отображения модели в админ панели
        verbose_name_plural = 'Список дел' # Название для отображения модели в админ панели во множественном числе

    def __str__(self):
        return self.title # Меняем строковое представление каждого объекта для админ панели

