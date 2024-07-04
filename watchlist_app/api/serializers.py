from rest_framework import serializers
from watchlist_app.models import WatchList,StreamPlatform,Review

class ReviewSerializer(serializers.ModelSerializer):
    review_user=serializers.StringRelatedField(read_only=True)
    # watchlist=serializers.StringRelatedField() # will return __str__ field
    class Meta:
        model=Review
        # fields="__all__"
        exclude=('watchlist',)
      
      
class WatchListSerializer(serializers.ModelSerializer):
    name_length=serializers.SerializerMethodField()
    #reviews=ReviewSerializer(many=True,read_only=True)
    platform=serializers.CharField(source='platform.name')
    
    class Meta:
        model=WatchList
        fields="__all__" #['id','name','description','active'] 
        # exclude=['active']
    
    def get_name_length(self,object):
        return len(object.title)

class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist=WatchListSerializer(many=True,read_only=True) # nested relationship
    # watchlist=serializers.StringRelatedField(many=True) # will return __str__ field
    class Meta:
        model=StreamPlatform
        fields="__all__"


  
# def txt_length(value): ####custom validator
#     if len(value)<2:
#         raise serializers.ValidationError('description is too short')
    
# class MovieSerializer(serializers.Serializer):
#     id=serializers.IntegerField(read_only=True)
#     name=serializers.CharField()
#     description=serializers.CharField(validators=[txt_length])
#     active=serializers.BooleanField()
    
#     def create(self,validated_data):
#         return Movie.objects.create(**validated_data)
    
#     def validate_name(self,value): # field level validation
#         if len(value)<2:
#             raise serializers.ValidationError('Name should be atleast 2 characters')
#         else:
#             return value
        
#     def validate(self,data): # Object-level validation
#         if data['name']==data['description']:
#             raise serializers.ValidationError('Name and description should not be same')
#         return data
    
