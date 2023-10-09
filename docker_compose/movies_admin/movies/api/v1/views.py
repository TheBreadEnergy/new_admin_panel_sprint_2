from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from .mixin import MoviesApiMixin


class MoviesListApi(MoviesApiMixin, BaseListView):

    def get_context_data(self, *, object_list=None, **kwargs):
        movies_qs = self.get_queryset()
        paginator, page, queryset, _ = self.paginate_queryset(
            movies_qs,
            self.paginate_by
        )
        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(queryset),
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_context_data(self, *, object_list=None, **kwargs):
        return {**kwargs['object']}
