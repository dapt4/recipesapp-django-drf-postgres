from django.contrib.auth.models import User
from .models import Doctor, Recipe, Drug
from rest_framework import serializers

class DoctorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'name']

class DrugSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Drug
        fields = ['id','name']

class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    doctor = serializers.SlugRelatedField(
        read_only = True,
        slug_field = 'name'
    )
    user = serializers.SlugRelatedField(
        read_only = True,
        slug_field = 'username'
    )
    drugs = serializers.SlugRelatedField(
        many=True,
        read_only = True,
        slug_field = 'name'
    )
    class Meta:
        model = Recipe
        fields = ['id', 'doctor', 'user', 'drugs']
