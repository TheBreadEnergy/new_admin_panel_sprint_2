import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField('Название', max_length=255)
    description = models.TextField('Описание', blank=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        indexes = [
            models.Index(fields=['name'], name='name_idx'),
        ]

    def __str__(self):
        return self.name


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = 'Жанр кинопроизведения'
        verbose_name_plural = 'Жанры кинопроизведения'
        constraints = [
            models.UniqueConstraint(fields=['film_work', 'genre'], name='filmwork_genre_unique')
        ]
        indexes = [
            models.Index(fields=['film_work'], name='film_work_idx'),
            models.Index(fields=['genre'], name='genre_idx')
        ]

    def __str__(self):
        return self.genre.name


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField('Полное имя', max_length=255)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = 'Участник фильма'
        verbose_name_plural = 'Участники фильма'
        indexes = [
            models.Index(fields=['full_name'], name='full_name_idx'),
        ]

    def __str__(self):
        return self.full_name


class PersonFilmwork(UUIDMixin):
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)

    class PersonFilmworkRole(models.TextChoices):
        ACTOR = 'actor', 'Аctor'
        DIRECTOR = 'director', 'Director'
        WRITER = 'writer', 'Writer'

    role = models.CharField('Роль',
                            max_length=8,
                            choices=PersonFilmworkRole.choices,
                            default=PersonFilmworkRole.ACTOR,
                            )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = 'Участник кинопроизведения'
        verbose_name_plural = 'Участники кинопроизведения'
        constraints = [
            models.UniqueConstraint(fields=['film_work', 'person', 'role'], name='film_work_person_role_unique')
        ]
        indexes = [
            models.Index(fields=['person'], name='person_idx'),
            models.Index(fields=['film_work'], name='filmwork_idx'),
            models.Index(fields=['role'], name='role_idx'),
        ]

    def __str__(self):
        return self.person.full_name


class Filmwork(UUIDMixin, TimeStampedMixin):
    title = models.CharField('Название', max_length=255)
    description = models.TextField('Описание', blank=True)
    creation_date = models.DateTimeField('Дата примьеры')
    rating = models.FloatField('Рейтинг', blank=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(100)])

    class FilmworkType(models.TextChoices):
        MOVIE = 'movie', 'Movie'
        TV_SHOW = 'tv_show', 'TV Show'

    type = models.CharField('Тип',
                            max_length=7,
                            choices=FilmworkType.choices,
                            default=FilmworkType.MOVIE,
                            )

    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    persons = models.ManyToManyField(Person, through='PersonFilmwork')

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = 'Кинопроизведение'
        verbose_name_plural = 'Кинопроизведения'
        indexes = [
            models.Index(fields=['title'], name='title_idx'),
            models.Index(fields=['rating'], name='rating_idx'),
            models.Index(fields=['creation_date'], name='creation_date_idx'),
        ]

    def __str__(self):
        return self.title
