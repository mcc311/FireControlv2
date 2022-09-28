from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Weapon
from .serializers import *

@api_view(['GET', 'POST'])
def weapons_list(request):
    if request.method == 'GET':
        data = Weapon.objects.all()

        serializer = WeaponSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = WeaponSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
def weapons_detail(request, id):
    try:
        weapon = Weapon.objects.get(id=id)
    except Weapon.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = WeaponSerializer(weapon, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        weapon.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)