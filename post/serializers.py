from rest_framework import serializers

from . models import Post,Comments
from users.models import NewUser
from imaging.models import Message



class RegisterUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = ('email','password','username','first_name','id')
        model = NewUser
        extra_kwargs = {'password':{'write_only':True},'id':{'read_only':True}}


    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance





class PostSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name ='post-detail',
        lookup_field ='pk'
    )
    my_user_data = serializers.SerializerMethodField(read_only = True)
    #author = RegisterUserSerializer()
    class Meta:
        fields = ('my_user_data','url','id','author','title','body','created_at')
        model = Post
        extra_kwargs = {'author':{'read_only':True}}

        
    def create(self, validated_data):
    #    #email = validated_data.pop('email')
        #author = validated_data.pop('author')
        request = self.context.get('request')
 #
        obj = Post.objects.create(author=request.user,**validated_data)
    #    #print(obj,email)
        return obj

    def get_my_user_data(self,obj):
        request = self.context.get('request')

        
        if obj.like.contains(request.user):
            like = True
        else:
            like = False
        commen = []
        com = Comments.objects.filter(postc=obj).order_by('-created_at')
        com_num = Comments.objects.filter(postc=obj).count()
        total = 0
        for v in obj.like.all():
            total = total + 1

        for k in com:
            commen.append({'id':k.id,'name':k.author.username,'body':k.body})
        
        return{
            "user":obj.author.username,
            "first_name":obj.author.first_name,
            "like":like,
            "com_num":com_num,
            "total":total,
            "coms":commen,
        }

### home serializer to list all post even when user has logged out  
class PostHomeSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name ='post-detail',
        lookup_field ='pk'
    )
    my_user_data = serializers.SerializerMethodField(read_only = True)
    
    class Meta:
        fields = ('my_user_data','url','id','author','title','total_likes','body','created_at')
        model = Post
        extra_kwargs = {'author':{'read_only':True}}

    def get_my_user_data(self,obj):
        request = self.context.get('request')
        com_num = Comments.objects.filter(postc=obj).count()
        total = 0
        for v in obj.like.all():
            total = total + 1
        return{
            "user":obj.author.username,
            "first_name":obj.author.first_name,
            "com_num":com_num,
            "total":total,
        }
  
#### 
### post comment serializer
class PostcommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['body']
        model = Comments

## serializer for creating post
class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['title','body','id']
        model = Post

### for message model in imaging app

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id','image','owner','timestamp']
        model = Message
        extra_kwargs = {'owner':{'read_only':True},'timestamp':{'read_only':True},}
