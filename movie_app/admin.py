from django.contrib import admin
from .models import Movie


# Register your models here.
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'year', 'budget', 'movie_status')
    list_editable = ('rating', 'year', 'budget')
    ordering = ['-rating', 'name']
    list_per_page = 10

    @admin.display(ordering='rating', description='Status')
    def movie_status(self, mov: Movie):
        if mov.rating < 50:
            return 'Не стоит смотреть'
        if mov.rating < 70:
            return 'На один раз'
        if mov.rating <=85:
            return 'Достойный вашего внимания'
        else:
            return 'Один из лучших'
