from django.contrib.auth.models import User
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import Recipe
from recipes.serializers import UserSerializer, RecipeSerializer


# Create your views here.




class ListUserView(generics.ListAPIView):
    """
    Provides a get method handler
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RecipesView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    """
    All the APIs for managing recipes
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get(self, request, *args, **kwargs):
        username = self.request.query_params.get('user', None)
        if username is not None:
            user = User.objects.get_by_natural_key(username)
            self.queryset = self.queryset.filter(user=user)

        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        name = request.data.pop('name')
        user_data = request.data.pop('user')
        username = user_data.pop('username')
        user = User.objects.get_by_natural_key(username)
        recipe = Recipe.objects.get(name=name, user=user)
        recipe.delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        name = request.data.pop('name')
        user_data = request.data.pop('user')
        username = user_data.pop('username')
        user = User.objects.get_by_natural_key(username)
        recipe = Recipe.objects.get(name=name, user=user)
        serializer.update(validated_data=request.data, instance=recipe)
        return Response(status=status.HTTP_200_OK)