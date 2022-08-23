from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import CustomUserSerializer
from rest_framework.response import Response

""" 

APIView for creating new users.
Input: email, password
Output: new user details.

"""
class SignUpView(APIView):
    def post(self, request):
        print(request.data)
        serializer = CustomUserSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print("data = ",serializer.data)

        return Response(serializer.data)