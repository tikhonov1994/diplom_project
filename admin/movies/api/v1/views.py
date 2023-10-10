from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from ...models import Filmwork, RoleChoices


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']
    queryset = Filmwork.objects.all()

    def get_queryset(self):
        queryset = self.queryset.prefetch_related('genres', 'persons').values(
            'id', 'title', 'description', 'creation_date', 'rating', 'type',
        ).annotate(
            genres=ArrayAgg('genres__name', distinct=True),
            actors=ArrayAgg('persons__full_name', filter=Q(persons__personfilmwork__role=RoleChoices.ACTOR),
                            distinct=True),
            directors=ArrayAgg('persons__full_name', filter=Q(persons__personfilmwork__role=RoleChoices.DIRECTOR),
                               distinct=True),
            writers=ArrayAgg('persons__full_name', filter=Q(persons__personfilmwork__role=RoleChoices.WRITER),
                             distinct=True)
        )

        return queryset

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )

        return {
            'results': list(paginator.get_page(self.request.GET.get('page'))),
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
        }


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    def get_context_data(self, **kwargs):
        return kwargs['object']
