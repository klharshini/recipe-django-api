
from django.urls import path
from .views import ListUserView, RecipesView

urlpatterns = [
    path('users/', ListUserView.as_view(), name="users-all"),
    path('recipes/', RecipesView.as_view(), name="recipe-crud")
]