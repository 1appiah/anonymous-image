from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView,ListAPIView,CreateAPIView
from rest_framework.views import APIView
from . models import Message
from post.serializers import MessageSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import parsers
from django.contrib.auth import get_user_model
# Create your views here.

User = get_user_model()

class CreateImages(CreateAPIView):
    permission_classes = (AllowAny,)
    parser_classes = [parsers.MultiPartParser,parsers.FormParser]


    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self,serializer):
        pk = self.kwargs.get('pk')
        user = User.objects.get(pk=pk)
        serializer.save(owner=user)

class Boss(APIView):
    permission_classes = [AllowAny]
    #parser_classes = [parsers.MultiPartParser,parsers.FormParser]
    def post(self,request,pk,format=None):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self,serializer):
        pk = self.kwargs.get('pk')
        user = User.objects.get(pk=pk)
        serializer.save(owner=user)



class ViewImage(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MessageSerializer
    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(owner=user).order_by('-timestamp')
    
class Dashboard(APIView):
    permission_classes = [AllowAny]

    def get(self,request):
        if request.user.is_authenticated:
            pk = request.user.id
        else:
            pk = "no"
        return Response({'id':pk})
            
     