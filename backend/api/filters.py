from django.contrib.auth import get_user_model
from django_filters.rest_framework import FilterSet, filters
from recipes.models import Recipe, Tag
from rest_framework.filters import SearchFilter
from distutils.util import strtobool

User = get_user_model()


class IngredientSearchFilter(SearchFilter):
    search_param = 'name'


class RecipesFilter(FilterSet):
    tags = filters.MultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )
    author = filters.ModelChoiceFilter(
        queryset=User.objects.all(),
    )
    is_favorited = filters.NumberFilter(
        method='get_is_favorited',
    )
    is_in_shopping_cart = filters.NumberFilter(
        method='get_is_in_shopping_cart',
    )
    print('Фильтр вызван')

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        print('Фильтр get_is_favorited вызван')
        if strtobool(value) and user.is_authenticated:
            return queryset.filter(favorites__user=user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        print('Фильтр get_is_in_shopping_cart вызван')
        if strtobool(value) and user.is_authenticated:
            return queryset.filter(shoppingcart_recipe__user=user)
        return queryset
