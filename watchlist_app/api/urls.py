from django.urls import include, path
from rest_framework.routers import DefaultRouter
from watchlist_app.api.views import (WatchListView,WatchListDetailView,StreamPlatformView,
                                     StreamPlatformDetailView,ReviewListView,ReviewDetailView,
                                     ReviewCreateView,StreamPlatformVs,UserReview,WatchListGV)

router=DefaultRouter()
router.register('platform',StreamPlatformVs,basename='streamplatform')

urlpatterns = [
    path('list/',WatchListView.as_view(),name='watch-list'),
    path('<int:pk>/',WatchListDetailView.as_view(),name='watch-detail'),
    path('list2/',WatchListGV.as_view(),name='watch-list'),
    path('platform/',StreamPlatformView.as_view(),name='stream-platform-list'),
    path('platform/<int:pk>',StreamPlatformDetailView.as_view(),name='stream-platform-detail'),
    path('',include(router.urls)),
    
    # path('review',ReviewListView.as_view(),name='review-list'),
    # path('review/<int:pk>',ReviewDetailView.as_view(),name='review-detail'),
    path('<int:pk>/review-create',ReviewCreateView.as_view(),name='review-create'),
    path('<int:pk>/reviews/',ReviewListView.as_view(),name='review-list'),
    path('review/<int:pk>',ReviewDetailView.as_view(),name='review-detail'),
    path('review/',UserReview.as_view(),name='user-review-detail'),
    #path('review/<str:username>/',UserReview.as_view(),name='user-review-detail'),

]
