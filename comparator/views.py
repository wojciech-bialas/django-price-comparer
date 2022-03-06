from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response


def home_view(request, *args, **kwargs):
    return render(request, 'home.html', {})

@api_view(['POST'])
def add_product(request):
    print('it works')
    print(request)

    return Response({"message": "OK"})
