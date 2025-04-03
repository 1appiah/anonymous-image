from django.shortcuts import render
from post.serializers import RegisterUserSerializer
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny,IsAuthenticated

User = get_user_model()

# Create your views here.

class CustomUserCreate(APIView):

    def post(self,request):
        reg_serializer = RegisterUserSerializer(data=request.data)
        if reg_serializer.is_valid():
            print(reg_serializer.validated_data.get('email'))
            newuser = reg_serializer.save()
            if newuser:
                return Response({"cond":"sucess!"},status=status.HTTP_201_CREATED)
        print("something went bad")
        return Response(reg_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class AllAuthors(ListAPIView):
    permission_classes = (AllowAny,)

    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer


