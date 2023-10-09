from django.contrib.postgres.aggregates import ArrayAgg
from django.http import JsonResponse
from django.db.models import Q
from movies.models import Filmwork


class MoviesApiMixin:
    http_method_names = ('get')
    paginate_by = 50
    model = Filmwork

    def get_queryset(self):
        return super().get_queryset(
        ).prefetch_related(
            'genres',
            'persons',
        ).values(
            'id',
            'title',
            'description',
            'creation_date',
            'type',
            'rating',
        ).annotate(
            genres=ArrayAgg('genres__name', distinct=True),
            actors=ArrayAgg('persons__full_name', filter=Q(personfilmwork__role='actor'),
                            distinct=True),
            directors=ArrayAgg('persons__full_name', filter=Q(personfilmwork__role='director'),
                               distinct=True),
            writers=ArrayAgg('persons__full_name', filter=Q(personfilmwork__role='writer'),
                             distinct=True),
        ).order_by('title')

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)
