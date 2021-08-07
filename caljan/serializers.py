from rest_framework import serializers
from .models import Feedback, User_guest,Menu


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = (
                  'name',
                  'rate',
                  'user')


class PictureSerialiser(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField('get_image_url')
    class Meta:
        model = Menu
        fields = ('name', 'price', 'description','food_class','photo','image_url')
    def get_image_url(self, obj):
        return obj.photo.url


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_guest
        fields = ('name', 'b_date', 'bonus_amount')