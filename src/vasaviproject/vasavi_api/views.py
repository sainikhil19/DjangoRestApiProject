from django.shortcuts import render

# Create your views he
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from . import models
from . import permission
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class HelloApiView(APIView):
    """class to test APIView."""

    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Returns a list of APIView features."""

        an_apiview = [
            'uses HTTP methids as function (get,post,patch,put,delete)',
            'It is similar to a traditional Django View',
            'Gives you the most control over your logic',
            'Is mapped manually to URLs'
        ]
        """here we return the response in the form of a json file dictionary"""
        return Response({'message':'Hello!','an_apiview':an_apiview})

    def post(self, request):
        """create a hello message with our name"""

        serializer = serializers.HelloSerializer(data = request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = "Hello {0}".format(name)
            return Response({'message':message})
        else:
            return Response(
            serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Handles updating an Object"""

        return Response({'method': 'put'})

    def patch(self, request, pk=None):
        """Patch request, Only updates fileds provided in the request"""

        return Response({'method': 'patch'})

    def delete(self, request, pk=None):
        """Delete an Object"""

        return Response({'method': 'delete'})

class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""

    serializer_class=serializers.HelloSerializer

    def list(self, request):
        """Return a hello message"""

        a_viewset = [
            'Uses action (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLs using routers',
            'Prvides more functionality with less code'
        ]
        return Response({'message':'Hello!','a_viewset':a_viewset})

    def create(self, request):
        """Takes care of HTTP post functionalities"""
        """Create a new Hello Message"""
        serializer = serializers.HelloSerializer(data = request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = "Hello {0}".format(name)
            return Response({'message':message})
        else:
            return Response(
            serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handles getting an object by its ID"""

        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """Handles updating an object by its ID"""

        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """Handles updating part of object"""

        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """Handles removing an object by its ID"""

        return Response({'http_method': 'DESTROY'})


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and udating profiles,"""

    serializer_class = serializers.UserProfileSerializer

    queryset = models.UserPreferences.objects.all()

    authentication_classes = (TokenAuthentication,)
    permission_classes = (permission.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name','email')


class LoginViewSet(viewsets.ViewSet):
    """Checks email and password and returns an auth token"""

    serializer_class = AuthTokenSerializer

    def create(self, request):
        """Use the ObtainAuthToken APIView to validate and create a token"""
        return ObtainAuthToken().post(request)


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and uploading profile feed item"""

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permission.PostOwnStatus, IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        """sets the user profile to the logged in user"""

        serializer.save(user_profile=self.request.user)
