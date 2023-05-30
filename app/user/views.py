""" Views for the user api """

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)

class CreateUserView(generics.CreateAPIView):
    """ Create a new user in the system """

    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """ Create a new auth token for user """
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    """ the renderer_class ensures that the dfr browsable api is available for this view """


class ManageUserView(generics.RetrieveUpdateAPIView):
    """ Manage the authenticated user """
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    """Authentication classs for authentication, permissions for setting what users are allowed to do, here the only"""
    """ thing that we have specified is that they must be authenticated, but could add more"""

    def get_object(self):
        """ Retrieve and return the authenticated user - override the OG method """
        return self.request.user

