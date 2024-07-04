from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from watchlist_app.api import serializers
from watchlist_app import models

class StreamPlatformsTestCase(APITestCase):
    
    def setup(self):
        self.user=User.objects.create_user(username="example",password="Password@123")
        self.token=Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token'+self.token.key)
        
        self.stream=models.StreamPlatform.objects.create(name="Netflix",
                                                          about="#1 Streaming Platform",
                                                          website="http://www.netflix.in.com")
    
    def test_stream_platform_create(self):
        data={
            "name":"Netflix",
            "about":"#1 Streaming Platform",
            "website":"http://www.netflix.in.com"
        }
        response=self.client.post(reverse('stream-platform-list'), data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        
    def test_streamplatform_list(self):
        response=self.client.get(reverse('stream-platform-list'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_streamplatform_ind(self):
        respoense=self.client.get(reverse('stream-platform-detail',args=(self.stream.id,)))