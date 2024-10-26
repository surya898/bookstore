from rest_framework import serializers
from django.contrib.auth.models import User
from books.models import carts,review

class bookserializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    price = serializers.IntegerField()
    description = serializers.CharField()
    category = serializers.CharField()
    # image = serializers.ImageField(required = False,default = None)


class userserializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["first_name","last_name","email","username","password"]
        
    def create(self, validated_data):
        return User.objects.create_user(**self.validated_data)    
    
class cartserilizer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    product=serializers.CharField(read_only=True)
    date=serializers.CharField(read_only=True)
    class Meta:
        model=carts
        fields="_all_"
        
class reviewserializer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    product=serializers.CharField(read_only=True)
    class Meta:
        models=review
        fields="_all_"