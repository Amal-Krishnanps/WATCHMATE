from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from watchlist_app.models import WatchList,StreamPlatform,Review
from watchlist_app.api.serializers import WatchListSerializer,StreamPlatformSerializer,ReviewSerializer
from watchlist_app.api.permission import IsAdminOrReadonly,IsReviewUserOrReadonly
from watchlist_app.api.throttling import ReviewCreateThrottle,ReviewListThrottle
from watchlist_app.api.pagination import WatchListPagination,WatchListLOPagination,WatchListCursorPagination

from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import filters

from rest_framework.throttling import UserRateThrottle,AnonRateThrottle,ScopedRateThrottle


from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class UserReview(generics.ListAPIView):
    #queryset = Review.objects.all() - overide default to get specific
    # Permission_classes=[IsAuthenticated]
    serializer_class=ReviewSerializer
    # throttle_classes=[UserRateThrottle,AnonRateThrottle]
    # throttle_classes=[ReviewListThrottle]   

    # def get_queryset(self): #Filtering against the user
    #     username=self.kwargs['username']
    #     return Review.objects.filter(review_user__username=username)
    
    def get_queryset(self): #Filtering against query parameters
        username=self.request.query_params.get('username',None)
        return Review.objects.filter(review_user__username=username)
    
# Review section using mixins
###############################################################
# class ReviewListView(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
    
# class ReviewDetailView(mixins.RetrieveModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

########################################################################    


########### Using generic class-based views ####################
class ReviewCreateView(generics.CreateAPIView):
    serializer_class=ReviewSerializer
    permission_classes=[IsAuthenticated]
    throttle_classes=[ReviewCreateThrottle]
    
    def get_queryset(self):
        return Review.objects.all()
        
    def perform_create(self, serializer):
        pk=self.kwargs.get('pk')
        watchlist=WatchList.objects.get(pk=pk)
        
        review_user=self.request.user
        review_user_qs=Review.objects.filter(watchlist=watchlist,review_user=review_user)
        
        if review_user_qs.exists():
            raise ValidationError('You have already reviewed this movie')
        
        if watchlist.number_rating ==0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating=(watchlist.avg_rating + serializer.validated_data['rating']/2)
            
        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()
        
        serializer.save(watchlist=watchlist,review_user=review_user)
        
class ReviewListView(generics.ListAPIView):
    #queryset = Review.objects.all() - overide default to get specific
    Permission_classes=[IsAuthenticated]
    serializer_class=ReviewSerializer
    # throttle_classes=[UserRateThrottle,AnonRateThrottle]
    throttle_classes=[ReviewListThrottle]
    filter_backends=[DjangoFilterBackend]
    filterset_fields=['review_user__username','active']
    
    
    def get_queryset(self):
        pk=self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)
    
class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    permission_classes =[IsReviewUserOrReadonly]#[IsAdminOrReadonly] #[IsAuthenticated]
    # throttle_classes=[UserRateThrottle,AnonRateThrottle]
    # throttle_classes=[ReviewListThrottle]
    throttle_classes=[ScopedRateThrottle]
    throttle_scope='review-detail'
#################################################################

class StreamPlatformVs(viewsets.ModelViewSet): 
    queryset=StreamPlatform.objects.all()
    serializer_class=StreamPlatformSerializer
    
#######viewsets
# class StreamPlatformViewset(viewsets.ViewSet):
#     def list(self,request):
#         queryset=StreamPlatform.objects.all()
#         serializer=StreamPlatformSerializer(queryset,many=True)
#         return Response(data=serializer.data)
    
#     def retrieve(self,request,pk=None):
#         queryset=StreamPlatform.objects.all()
#         watchlist=get_object_or_404(queryset,pk=pk)
#         serializer=StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)
            
        
class StreamPlatformView(APIView):
    permission_classes=[IsAdminOrReadonly]
    
    def get(self,request):
        qs=StreamPlatform.objects.all()
        serializer=StreamPlatformSerializer(qs,many=True)
        return Response(data=serializer.data)

    def post(self,request):
        serializer=StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors)

class StreamPlatformDetailView(APIView):
    permission_classes=[IsAdminOrReadonly]
    
    def get(self,request,*args,**kwargs):
       id=kwargs.get("pk")
       qs=StreamPlatform.objects.get(id=id)
       serializer=StreamPlatformSerializer(qs)
       return Response(serializer.data)

    def put(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=StreamPlatform.objects.get(id=id)
        serializer=StreamPlatformSerializer(data=request.data,instance=obj)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        StreamPlatform.objects.filter(id=id).delete()
        return Response(status=status.HTTP_200_OK)
            
class WatchListView(APIView):
    permission_classes= [IsAdminOrReadonly]
    
    def get(self,request,*args,**kwargs):
        qs=WatchList.objects.all()
        serializer=WatchListSerializer(qs,many=True)
        return Response(data=serializer.data)        

    def post(self,request):
        Serializer=WatchListSerializer(data=request.data)
        if Serializer.is_valid():
            Serializer.save()
            return Response(data=Serializer.data)
        else:
            return Response(data=Serializer.errors)
        
        
class WatchListDetailView(APIView):
    permission_classes = [IsAdminOrReadonly]
    
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=WatchList.objects.get(id=id)
        serializer=WatchListSerializer(qs)
        return Response(data=serializer.data)
    
    def put(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=WatchList.objects.get(id=id)
        serializer=WatchListSerializer(data=request.data,instance=obj)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(serializer.errors,status.HTTP_404_NOT_FOUND)
        
    def delete(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        mov=WatchList.objects.get(id=id)
        mov.delete()
        # Movie.objects.filter(id=id).delete()
        # return Response(data={"message":"Deleted successfully"})
        return Response(status=status.HTTP_200_OK)
        
        
class WatchListGV(generics.ListAPIView):
    queryset = WatchList.objects.all() 
    # Permission_classes=[IsAuthenticated]
    serializer_class=WatchListSerializer
    pagination_class= WatchListCursorPagination  #WatchListLOPagination  # WatchListPagination

    ####### search
    filter_backends= [filters.SearchFilter]
    search_fields=['title','platform__name']
    
    ####  filter
    filter_backends= [filters.OrderingFilter]
    ordering_fields=['avg_rating']