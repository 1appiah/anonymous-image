from django.shortcuts import render

from . models import Post,Comments
from . serializers import PostSerializer,PostcommentSerializer,PostHomeSerializer,CreatePostSerializer
from rest_framework import generics, permissions
from .permissions import IsAuthorOrReadOnly
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
## list home post
class HomePostList(generics.ListAPIView):
    serializer_class = PostHomeSerializer
    queryset = Post.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)




class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


#class PostList(generics.ListCreateAPIView):
#    permission_classes = (AllowAny,)
#    queryset = Post.objects.all()
#    serializer_class = CreatePostSerializer
#
#    def perform_create(self, serializer):
#        serializer.save(author=self.request.user)

class UserBlogList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        post = Post.objects.filter(author=request.user)
        context = {'request':request}

        datas = PostSerializer(post,many=True,context=context)
    
        return Response(datas.data, status=status.HTTP_202_ACCEPTED)
        #return Response(datas.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request):
        pass
## listing all authors-- should include only authors who have created a post.

## all post of a selected author
class ListAuthorPost(APIView):
    permission_classes = (AllowAny,)

    def get(self,request,pk):
        post = Post.objects.filter(author=pk)
        context = {'request':request}

        datas = PostHomeSerializer(post,many=True,context=context)
    
        return Response(datas.data, status=status.HTTP_202_ACCEPTED)

## like_view at detail view by using a heart icon
@api_view(['GET'])
@permission_classes([AllowAny])
def likePost(request,pk):
    post = Post.objects.get(pk=pk)
    user = request.user
    try:
        if post.like.contains(user):
            post.like.remove(user)
            post.save()
            like = False
            post.total_likes = post.like.count()
            post.save()
            return Response({like:like}, status=status.HTTP_202_ACCEPTED)
        else:
            post.like.add(user)
            post.save()
            like = True
            post.total_likes = post.like.count()
            post.save()
            return Response({like:like}, status=status.HTTP_202_ACCEPTED)
    except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST','get'])
def postcomment(request,pk):
    post = Post.objects.get(pk=pk)
    serial = request.data
    body = serial['comment']['body']
    comments = Comments(body=body,postc=post,author=request.user)
    comments.save()

    return Response( status=status.HTTP_202_ACCEPTED)


    
# getting newest and popular posts
@api_view(['GET'])
def newest_post(request):
    post = Post.objects.all().order_by('-created_at')[:4]
    popular = Post.objects.all().order_by('-total_likes')[:4]

    context = {'request':request}
    newest = PostHomeSerializer(post,many=True,context=context).data
    popular = PostHomeSerializer(popular,many=True,context=context).data

    return Response({'popular':popular,'newest':newest},status=status.HTTP_202_ACCEPTED)


## create post
@api_view(['POST'])
def createpost(request):
    datas = request.data
    print(datas)
    post = Post(**datas)
    post.author = request.user
    post.save()
    ### send out email to subscribed mails after post gets created
    return Response( status=status.HTTP_202_ACCEPTED)

## receive subscribed emails into a model and use it to send out notifications when new post gets added