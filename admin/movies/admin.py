from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import Filmwork, GenreFilmwork, PersonFilmwork, Person, User


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


class CustomUserAdmin(UserAdmin):
    model = User

    list_display = ('email',)
    list_filter = ('email',)
    fieldsets = (
        (None, {'fields': ('email',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',)}
         ),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = []


# Re-register UserAdmin
admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)
