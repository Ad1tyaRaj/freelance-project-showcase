from rest_framework import serializers
from .models import User, Newsletter



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email',]
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
class NewsletterSerializer(serializers.Serializer):
    class Meta:
        model = Newsletter
        fields = '__all__'