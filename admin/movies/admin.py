from django.contrib import admin

# from docker_compose.simple_project.app.movies.models import Filmwork, GenreFilmwork, PersonFilmwork
from .models import Filmwork, GenreFilmwork, PersonFilmwork, Person


# Register your models here


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline)

    list_display = ('title', 'type', 'creation_date', 'rating', 'created_at', 'updated_at',)
    list_filter = ('type', 'creation_date',)

    search_fields = ('title', 'id')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name',)
    list_filter = ('created_at',)

    search_fields = ('full_name',)