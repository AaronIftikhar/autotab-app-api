from rest_framework import (
    viewsets,
    mixins,
    status,
)

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from core.models import (Project, ProjectInstance, TabInstance,User)
#TabInstance

from project.serializers import (
    TabInstanceSerializer,
    ProjectInstanceSerializer,
    ProjectSerializer,
    UserSerializer,
    TabInstanceMainFileSerializer,
    TabInstanceWeightFileSerializer,
    TabInstanceDictionaryFileSerializer,
    TabInstanceRecodeFileSerializer,
    TabInstanceRegroupFileSerializer
)

from project import serializers

class UserListView(generics.ListAPIView):

    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]
    #authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        """Retrieve recipes for authenticated user"""
        return self.queryset.filter(company_name=self.request.user.company_name)
    """ Overriding get_queryset method to make sure ONLY user's companies' projects are shown"""


class ProjectListView(generics.ListCreateAPIView):

    queryset = Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    permission_classes = [IsAuthenticated]
    #authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        """Retrieve recipes for authenticated user"""
        return self.queryset.filter(company_name_project=self.request.user.company_name)
    """ Overriding get_queryset method to make sure ONLY user's companies' projects are shown"""

    def perform_create(self, serializer):
        """Create a new project."""
        serializer.save(user=self.request.user)


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    permission_classes = [IsAuthenticated]
    #authentication_classes = [TokenAuthentication]
    lookup_field = "project_title_slug"

    def get_queryset(self):
        """Retrieve only instances """
        return self.queryset.filter(company_name_project=self.request.user.company_name)
    """ Overriding get_queryset method to make sure ONLY user's companies' projects are shown"""


class ProjectInstanceList(generics.ListCreateAPIView):

    queryset = ProjectInstance.objects.all()
    serializer_class = serializers.ProjectInstanceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Create a new project instance """
        project_title_slug = self.kwargs.get('project_title_slug')
        ind_project_title = Project.objects.get(project_title_slug = project_title_slug)

        serializer.save(project_instance = ind_project_title, user=self.request.user)

    def get_queryset(self):
        """Retrieve only instances from specific project"""
        project_title_slug = self.kwargs.get('project_title_slug')
        ind_project_title = Project.objects.get(project_title_slug =project_title_slug)

        return self.queryset.filter(project_instance=ind_project_title,company_name_project_instance=self.request.user.company_name)
    """ Overriding get_queryset method to make sure ONLY user's companies' projects are shown"""


class ProjectInstanceDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = ProjectInstance.objects.all()
    serializer_class = serializers.ProjectInstanceSerializer
    permission_classes = [IsAuthenticated]
    #authentication_classes = [TokenAuthentication]
    lookup_field = "project_instance_slug"

    def get_queryset(self):
        """Retrieve only instances """
        return self.queryset.filter(company_name_project_instance=self.request.user.company_name)

    def perform_update(self, serializer):
        """Create a new project."""
        serializer.save()


class TabInstanceList(viewsets.ModelViewSet):

    queryset = TabInstance.objects.all()
    serializer_class = serializers.TabInstanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipes for authenticated user"""

        project_instance = self.kwargs.get('project_instance_slug')
        ind_project_instance = ProjectInstance.objects.get(project_instance_slug =project_instance)

        return self.queryset.filter(project_instance_tab_instance=ind_project_instance, company_name_project_instance_tab = self.request.user.company_name)

    """ Overriding get_queryset method to make sure ONLY user's recipes are shown"""

    def get_serializer_class(self):
        """Return the serializer class for request"""

        if self.action == 'list':
            return serializers.TabInstanceSerializer
        elif self.action == 'upload_file':
            return serializers.TabInstanceMainFileSerializer
        elif self.action == 'upload_weights':
            return serializers.TabInstanceWeightFileSerializer
        elif self.action == 'upload_dictionary':
            return serializers.TabInstanceDictionaryFileSerializer
        elif self.action == 'upload_recode':
            return serializers.TabInstanceRecodeFileSerializer
        elif self.action == 'upload_regroup':
            return serializers.TabInstanceRegroupFileSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new tab instance """
        project_instance_slug = self.kwargs.get('project_instance_slug')
        ind_project_instance_title = ProjectInstance.objects.get(project_instance_slug = project_instance_slug)

        serializer.save(project_instance_tab_instance = ind_project_instance_title, user = self.request.user)


    @action(methods=['POST'],detail=True,url_path = 'upload-file')
    def upload_file(self,request, pk=None,project_instance_slug=None,project_title_slug=None):
        """ Upload a file to instance"""
        tabinstance = self.get_object()
        serializer = self.get_serializer(tabinstance,data=request.data)

        if serializer.is_valid():
            serializer.save()
            """ save image to db """
            return Response(serializer.data, status = status.HTTP_200_OK)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


    @action(methods=['POST'],detail=True,url_path = 'upload-weights')
    def upload_weights(self,request, pk=None,project_instance_slug=None,project_title_slug=None):
        """ Upload a file to instance"""
        tabinstance = self.get_object()
        serializer = self.get_serializer(tabinstance,data=request.data)

        if serializer.is_valid():
            serializer.save()
            """ save image to db """
            return Response(serializer.data, status = status.HTTP_200_OK)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


    @action(methods=['POST'],detail=True,url_path = 'upload-dictionary')
    def upload_dictionary(self,request, pk=None,project_instance_slug=None,project_title_slug=None):
        """ Upload a file to instance"""
        tabinstance = self.get_object()
        serializer = self.get_serializer(tabinstance,data=request.data)

        if serializer.is_valid():
            serializer.save()
            """ save image to db """
            return Response(serializer.data, status = status.HTTP_200_OK)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


    @action(methods=['POST'],detail=True,url_path = 'upload-recode')
    def upload_recode(self,request, pk=None,project_instance_slug=None,project_title_slug=None):
        """ Upload a file to instance"""
        tabinstance = self.get_object()
        serializer = self.get_serializer(tabinstance,data=request.data)

        if serializer.is_valid():
            serializer.save()
            """ save image to db """
            return Response(serializer.data, status = status.HTTP_200_OK)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'],detail=True,url_path = 'upload-regroup')
    def upload_regroup(self,request, pk=None,project_instance_slug=None,project_title_slug=None):
        """ Upload a file to instance"""
        tabinstance = self.get_object()
        serializer = self.get_serializer(tabinstance,data=request.data)

        if serializer.is_valid():
            serializer.save()
            """ save image to db """
            return Response(serializer.data, status = status.HTTP_200_OK)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)









# """ Views for the recipe APIs """

# from rest_framework import (
#     viewsets,
#     mixins,
#     status,
# )

# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated

# from core.models import (Project)

# from client import serializers

# class RecipeViewSet(viewsets.ModelViewSet):
#     """ Model view set is specifically set up to work with models """
#     """ View for manage recipe APIs (plural as it will generate multiple endpoints)"""

#     serializer_class = serializers.RecipeDetailSerializer
#     queryset = Recipe.objects.all()
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         """Retrieve recipes for authenticated user"""
#         return self.queryset.filter(user=self.request.user).order_by('-id')
#     """ Overriding get_queryset method to make sure ONLY user's recipes are shown"""

#     def get_serializer_class(self):
#         """Return the serializer class for request"""

#         if self.action == 'list':
#             return serializers.RecipeSerializer
#         elif self.action == 'upload_image':
#             return serializers.RecipeImageSerializer

#         """ Action allow you to add cutom functionality to viewset"""
#         """ All default actions are in django files, "upload image" is custom"""

#         return self.serializer_class

#     def perform_create(self,serializer):
#         """ Create a new recipe - this method is built in to the viewset """
#         """ When we perform a creation of a new obect through this model viewset, call this methos as part of that creation """
#         serializer.save(user=self.request.user)

#     @action(methods=['POST'],detail=True,url_path = 'upload-image')
#     def upload_image(self,request, pk=None):
#         """ Upload an image to recipe"""
#         recipe = self.get_object()
#         serializer = self.get_serializer(recipe,data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             """ save image to db """
#             return Response(serializer.data, status = status.HTTP_200_OK)

#         return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

#     """ Added a custom action using action decorator provided by drf """
#     """ decorator lets you specify different http methods supported by custom action"""
#     """ Here we only expect POST, but can create actions that take all types of request """
#     """ Details = True, action applied to detail portion of viewset - is a specific id of a recipe that image is attached ti"""
#     """ The non detailed view would be the list view."""


# class TagViewSet(mixins.DestroyModelMixin,
#                  mixins.UpdateModelMixin,
#                  mixins.ListModelMixin,
#                  viewsets.GenericViewSet):
#     """ Manage tags in the database """
#     """ MIXIN HAS TO GO BEFORE GENERICS, GENERIC LAST IN IMPORTS"""

#     serializer_class = serializers.TagSerializer
#     queryset = Tag.objects.all()
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         """Retrieve tags for authenticated user only"""
#         return self.queryset.filter(user=self.request.user).order_by('-name')


# class IngredientViewSet(mixins.DestroyModelMixin,
#                 mixins.UpdateModelMixin,
#                 mixins.ListModelMixin,
#                 viewsets.GenericViewSet):
#     """ Manage ingreidents in the database """

#     serializer_class = serializers.IngredientSerializer
#     queryset = Ingredient.objects.all()
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         """Retrieve ingredients for authenticated user only"""
#         return self.queryset.filter(user=self.request.user).order_by('-name')
#     """" -name, means order my name in reverse """



