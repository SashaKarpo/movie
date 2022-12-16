from django.contrib import admin, messages
from .models import Movie
from django.db.models import QuerySet


# Register your models here.
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'currency', 'budget', 'movie_status')
    list_editable = ('rating', 'currency', 'budget')
    ordering = ['-rating', 'name']
    list_per_page = 10
    actions = ['set_dollar', 'set_euro']

    @admin.display(ordering='rating', description='Status')
    def movie_status(self, mov: Movie):
        if mov.rating < 50:
            return 'Не стоит смотреть'
        if mov.rating < 70:
            return 'На один раз'
        if mov.rating <= 85:
            return 'Достойный вашего внимания'
        else:
            return 'Один из лучших'

    @admin.action(description='Установить валюту в доллар')
    def set_dollar(self, request, qs: QuerySet):
        qs.update(currency=Movie.USD)

    @admin.action(description='Установить валюту в евро')
    def set_euro(self, request, qs: QuerySet):
        count_update = qs.update(currency=Movie.EUR)
        self.message_user(
            request,
            f'Было обновлено {count_update} записей',
            messages.ERROR,
        )
