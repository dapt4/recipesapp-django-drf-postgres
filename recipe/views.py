from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import Doctor, Recipe, Drug
from django.contrib.auth.models import User
from .serializers import DoctorSerializer, RecipeSerializer, DrugSerializer

# Create your views here.

@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def login(request):
    try:
        user = authenticate(
            username=request.data['username'],
            password=request.data['password']
        )
        if not user:
            return Response({"error": "invalid credentials"}, status=status.HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token":token.key}, status=status.HTTP_200_OK)
    except Exception as err:
        print(err)
        return Response({"error": "internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny,])
def register(request):
    try:
        user = User(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        return Response({"status":"done"}, status=status.HTTP_200_OK)
    except Exception as err:
        print(err)
        return Response({"error": "internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['GET','POST'])
def doctor(request):
    try:
        if request.method == 'GET':
            doctors = Doctor.objects.all()
            serializer = DoctorSerializer(doctors, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'POST':
            doctor = Doctor(name=request.data['name'])
            doctor.save()
            serializer = DoctorSerializer(doctor)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as err:
        print(err)
        return Response({"error": "internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['GET','PUT', 'DELETE'])
def edit_doctor(request,id):
    try:
        if request.method == 'GET':
            doctor = Doctor.objects.get(id=id)
            serializer = DoctorSerializer(doctor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            doctor = Doctor.objects.get(id=id)
            doctor.name = request.data['name']
            doctor.save()
            serializer = DoctorSerializer(doctor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            doctor = Doctor.objects.get(id=id)
            doctor.delete()
            serializer = DoctorSerializer(doctor)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as err:
        print(err)
        return Response({"error": "internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['GET','POST'])
def drug(request):
    try:
        if request.method == 'GET':
            drugs = Drug.objects.all()
            serializer = DrugSerializer(drugs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'POST':
            drug = Drug(name=request.data['name'])
            drug.save()
            serializer = DoctorSerializer(drug)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as err:
        print(err)
        return Response({"error": "internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['GET', 'POST'])
def recipe(request):
    try:
        user = request.user
        if request.method == 'GET':
            recipes = user.recipes.all()
            serializer = RecipeSerializer(recipes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'POST':
            recipe = Recipe.objects.create(doctor_id=request.data['doctor'], user=user)
            recipe.drugs.set(request.data['drugs'])
            recipe.save()
            serializer = RecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as err:
        print(err)
        return Response({"error": "internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['GET','PUT','DELETE'])
def edit_recipe(request, id):
    try:
        recipe = Recipe.objects.get(id=id)
        if request.method == 'GET':
            serializer = RecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            doctor = Doctor.objects.get(id=request.data['doctor'])
            recipe.doctor = doctor
            recipe.drugs.set(request.data['drugs'])
            recipe.save()
            serializer = RecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            recipe.delete()
            serializer = RecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    except Exception as err:
        print(err)
        return Response({"error": "internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
