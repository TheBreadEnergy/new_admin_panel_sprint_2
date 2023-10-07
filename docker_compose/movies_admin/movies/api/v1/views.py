from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.list import BaseListView

from movies.models import Filmwork


class MoviesListApi(BaseListView):
    model = Filmwork
    http_method_names = ['get']  # Допустимые методы для этого обработчика

    def get_queryset(self):
        # Определяем количество фильмов на одной странице
        items_per_page = 50

        # Получаем номер страницы из запроса
        try:
            page = int(self.request.GET.get('page', 1))
            if page <= 0:
                raise ValueError
        except ValueError:
            # В случае неверного номера страницы возвращаем ошибку
            self.error = {"detail": "Неверный параметр page."}
            return []

        # Рассчитываем индексы для выборки фильмов
        start_index = (page - 1) * items_per_page
        end_index = start_index + items_per_page

        # Если начальный индекс больше общего числа фильмов, возвращаем ошибку
        if start_index >= Filmwork.objects.count():
            self.error = {"detail": "Страница не найдена."}
            return []

        # Возвращаем выборку фильмов
        return Filmwork.objects.all()[start_index:end_index]

    def get_context_data(self, *, object_list=None, **kwargs):
        items_per_page = 50
        page = int(self.request.GET.get('page', 1))

        # Правильно извлекаем связанные данные с учетом уникальности
        filmwork_data = self.get_queryset().annotate(
            genres_list=ArrayAgg('genrefilmwork__genre__name', distinct=True),
            actors_list=ArrayAgg('personfilmwork__person__full_name', filter=Q(personfilmwork__role='actor'),
                                 distinct=True),
            directors_list=ArrayAgg('personfilmwork__person__full_name', filter=Q(personfilmwork__role='director'),
                                    distinct=True),
            writers_list=ArrayAgg('personfilmwork__person__full_name', filter=Q(personfilmwork__role='writer'),
                                  distinct=True),
        ).values(
            'id', 'title', 'description', 'creation_date', 'rating', 'type',
            'genres_list', 'actors_list', 'directors_list', 'writers_list'
        )

        # Рассчитываем общее количество страниц
        total_count = Filmwork.objects.count()
        total_pages = -(-total_count // items_per_page)  # Деление с округлением вверх

        # Определяем номера предыдущей и следующей страницы
        prev_page = page - 1 if page > 1 else None  # Изменили здесь
        next_page = page + 1 if page < total_pages else total_pages

        context = {
            'count': total_count,
            'total_pages': total_pages,
            'prev': prev_page,
            'next': next_page,
            'results': list(filmwork_data),
        }
        return context

    def render_to_response(self, context, **response_kwargs):
        # В случае ошибки возвращаем сообщение об ошибке
        if hasattr(self, "error"):
            return JsonResponse(self.error, status=400)

        # Модифицируем ответ, чтобы он соответствовал требуемой структуре
        for filmwork in context['results']:
            # Переименовываем ключи для соответствия требуемой структуре
            filmwork['genres'] = filmwork.pop('genres_list', [])
            filmwork['actors'] = filmwork.pop('actors_list', [])
            filmwork['directors'] = filmwork.pop('directors_list', [])
            filmwork['writers'] = filmwork.pop('writers_list', [])

        # Возвращаем ответ
        return JsonResponse(context)