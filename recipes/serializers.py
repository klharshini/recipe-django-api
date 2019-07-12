from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from django.contrib.auth.models import User

from recipes.models import Recipe, Ingredient, Step


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "last_name", "first_name", "email")
        extra_kwargs = {
            'username': {
                'validators': [UnicodeUsernameValidator()],
            }
        }


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["text"]


class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ["step_text"]


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, required=False)
    steps = StepSerializer(many=True, required=False)
    user = UserSerializer(required=True)

    def create(self, validated_data):
        steps_data = validated_data.pop('steps')
        ingredients_data = validated_data.pop('ingredients')
        user_data = validated_data.pop('user')
        username = user_data.pop('username')
        user = User.objects.get_by_natural_key(username)
        recipe = Recipe.objects.create(user=user, **validated_data)
        for steps in steps_data:
            Step.objects.create(recipe=recipe, **steps)

        for ingredients in ingredients_data:
            Ingredient.objects.create(recipe=recipe, **ingredients)
        return recipe

    class Meta:
        model = Recipe
        fields = ("name", "user", "steps", "ingredients")

    def update(self, instance, validated_data):
        steps_data = validated_data.pop('steps')
        ingredients_data = validated_data.pop('ingredients')
        Step.objects.filter(recipe=instance).delete()
        Ingredient.objects.filter(recipe=instance).delete()
        for steps in steps_data:
            Step.objects.create(recipe=instance, **steps)

        for ingredients in ingredients_data:
            Ingredient.objects.create(recipe=instance, **ingredients)
        return instance
