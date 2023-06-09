from api.filters import AuthorAndTagFilter, IngredientSearchFilter
from api.pagination import CustomPagination
from api.permissions import IsAuthenticatedAuthorOrReadOnly
from api.serializers import (CustomUserSerializer, IngredientSerializer,
                             RecipeSerializer, ShortRecipeSerializer,
                             SubscriptionSerializer,
                             TagSerializer)
from django.shortcuts import HttpResponse, get_object_or_404
from djoser.views import UserViewSet
from recipes.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                            ShoppingСart, Tag)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status, views, viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from users.models import Subscription, User


def pdf_generation(value_list):
    final_list = {}
    for item in value_list:
        name = item[0]
        if name not in final_list:
            final_list[name] = {
                'measurement_unit': item[1],
                'amount': item[2]
            }
        else:
            final_list[name]['amount'] += item[2]
    pdfmetrics.registerFont(
        TTFont('Halogen', 'Halogen.ttf', 'UTF-8'))
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        'attachment; '
        'filename="shopping_list.pdf"'
    )
    page = canvas.Canvas(response)
    page.setFont('Halogen', size=24)
    page.drawString(200, 800, 'Список ингредиентов')
    page.setFont('Halogen', size=16)
    height = 750
    for i, (name, data) in enumerate(final_list.items(), 1):
        page.drawString(75, height, (f'<{i}> {name} - {data["amount"]}, '
                                     f'{data["measurement_unit"]}'))
        height -= 25
    page.showPage()
    page.save()
    return response


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = CustomPagination
    filter_class = AuthorAndTagFilter
    permission_classes = [IsAuthenticatedAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            return self.add_obj(Favorite, request.user, pk)
        if request.method == 'DELETE':
            return self.delete_obj(Favorite, request.user, pk)
        return None

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            return self.add_obj(ShoppingСart, request.user, pk)
        if request.method == 'DELETE':
            return self.delete_obj(ShoppingСart, request.user, pk)
        return None

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients = IngredientAmount.objects.filter(
            recipe__cart__user=request.user).values_list(
            'ingredient__name', 'ingredient__measurement_unit',
            'amount')
        return pdf_generation(ingredients)

    def add_obj(self, model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response({
                'errors': 'Рецепт уже добавлен в список'
            }, status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = ShortRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_obj(self, model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({
            'errors': 'Рецепт уже удален'
        }, status=status.HTTP_400_BAD_REQUEST)


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class SubscriptionViewSet(ListAPIView):
    serializer_class = SubscriptionSerializer
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)


class SubscribeView(views.APIView):
    serializer_class = SubscriptionSerializer
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        if user_id == request.user.id:
            return Response(
                {'Запрещено подписываться на себя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if Subscription.objects.filter(
                user=request.user,
                author_id=user_id
        ).exists():
            return Response(
                {'Вы уже подписаны на автора'},
                status=status.HTTP_400_BAD_REQUEST
            )
        author = get_object_or_404(User, id=user_id)
        Subscription.objects.create(
            user=request.user,
            author_id=user_id
        )
        return Response(
            self.serializer_class(author, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        get_object_or_404(User, id=user_id)
        subscription = Subscription.objects.filter(
            user=request.user,
            author_id=user_id
        )
        if subscription:
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'Вы не подписаны на пользователя'},
            status=status.HTTP_400_BAD_REQUEST
        )
