from django.contrib import admin, messages
from .models import Movie
from django.db.models import QuerySet


# Register your models here.
class RatingFilter(admin.SimpleListFilter):
    title = 'Фильтр по рейтингу'
    parameter_name = 'rating'

    def lookups(self, request, model_admin):
        return [
            ('<40', 'Низкий'),
            ('от 40 до 59', 'Cредний'),
            ('от 60 до 79', 'Высокий'),
            ('>=80', 'Высочайший')
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<40':
            return queryset.filter(rating__lt=40)
        if self.value() == 'от 40 до 59':
            return queryset.filter(rating__gte=40).filter(rating__lt=60)
        if self.value() == 'от 60 до 79':
            return queryset.filter(rating__gte=60).filter(rating__lt=80)
        if self.value() == '>=80':
            return queryset.filter(rating__gte=80)
        return queryset


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    # fields = []
    # exclude = ['slug']
    # readonly_fields = []
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'rating', 'currency', 'budget', 'movie_status')
    list_editable = ('rating', 'currency', 'budget')
    ordering = ['-rating', 'name']
    list_per_page = 10
    actions = ['set_dollar', 'set_euro']
    search_fields = ['name__istartswith', 'rating']
    list_filter = ['name', 'currency', RatingFilter]

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
