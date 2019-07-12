from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Recipe(models.Model):
    # Name of the recipe
    name = models.CharField(max_length=255, null=False)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )


class Step(models.Model):
    # Text of the step
    step_text = models.CharField(max_length=255, null=False)
    recipe = models.ForeignKey(Recipe, related_name='steps', on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % self.step_text


class Ingredient(models.Model):
    # Name of the recipe
    text = models.CharField(max_length=255, null=False)
    recipe = models.ForeignKey(Recipe, related_name='ingredients', on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % self.text

