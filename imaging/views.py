from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView,ListAPIView,CreateAPIView
from rest_framework.views import APIView
from . models import Message
from post.serializers import MessageSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import parsers
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from cloudinary.uploader import upload
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
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
        uploaded_file = self.request.data.get('image')
        if uploaded_file:
            # Upload to Cloudinary
            upload_result = upload(uploaded_file)
            # Save the public_id to the image field
            serializer.save(owner=user, image=upload_result['public_id'])
        else:
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
    

@method_decorator(cache_page(60 * 5), name='dispatch')  # Cache for 5 minutes
class Dashboard(APIView):
    permission_classes = [IsAuthenticated]

    
    def get(self, request):
        return Response({
            'id': request.user.id,
            'name': request.user.username
        })
            
## image can be deleted by users

@api_view(['GET'])
def delete_image(request,pk):
    mess = Message.objects.get(pk=pk)
    mess.image.delete(save=False) 
    mess.delete()
    return Response('success',status=status.HTTP_202_ACCEPTED)