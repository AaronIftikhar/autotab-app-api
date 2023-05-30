# """ Serliazers for recipe APIs """

from rest_framework import serializers
from core.models import (Project,ProjectInstance,User,TabInstance)


class TabInstanceMainFileSerializer(serializers.ModelSerializer):
    """ Serializer for uploading main datafile to tab instance """

    class Meta:
        model = TabInstance
        fields = ['id','main_data']
        read_only_fields = ['id']
        extra_kwargs = {'main_data':{'required':'True'}}

class TabInstanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = TabInstance
        fields = ['id','tab_instance_name','main_data']
        read_only_fields = ['id',]

class ProjectInstanceSerializer(serializers.ModelSerializer):

    project_instance = serializers.StringRelatedField(many=False)
    tabinstances = TabInstanceSerializer(many=True, read_only=True)

    class Meta:
        model = ProjectInstance
        fields = ['id','project_instance_name','project_instance_slug','project_instance','tabinstances']
        read_only_fields = ['id','project_instance','project_instance_slug','tabinstances']

class ProjectSerializer(serializers.ModelSerializer):

    projectinstances = ProjectInstanceSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id','project_title','project_title_slug','company_name_project','projectinstances']
        read_only_fields = ['id','company_name_project','project_title_slug','projectinstances']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['company_name','email',]
        read_only_fields = ['company_name','email',]



# class ProjectInstanceSummarySerializer(serializers.ModelSerializer):

#     class Meta:
#         model = ProjectInstance
#         fields = ['project_instance_name']


# class ProjectDetailSerializer(serializers.ModelSerializer):
#     instances = ProjectInstanceSummarySerializer(read_only=True, many=True)

#     class Meta:
#         model = Project
#         fields = ['project_title', 'instances']


# # the first serializer, for the project
# class ProjectSummarySerializer(serializers.ModelSerializer):
#     """ Serializer for projects """

#     class Meta:
#         model = Project
#         fields = ['project_title']


#     def create(self,validated_data):
#         """ Create project """

#         project = Project.objects.create(**validated_data)

#         return project

# # the main serializer for the instance
# class ProjectInstanceSerializer(serializers.ModelSerializer):
#     """ Serializer for uploading data files to projects """

#     project = ProjectSummarySerializer(read_only = True)

#     class Meta:
#         model = ProjectInstance
#         fields = ['project','project_instance_name']


#     def create(self, validated_data):
#         request = self.context['request']

#         project_pk = request.data.get('project')
#         #project_pk = attempt_json_deserialize(project_pk, expect_type=str)
#         validated_data['project_id'] = project_pk

#         instance = super().create(validated_data)

#         return instance

#     def update(self, instance, validated_data):
#         request = self.context['request']

#         project_data = request.data.get('project')
#         #project_data = attempt_json_deserialize(project_data, expect_type=str)
#         validated_data['project_id'] = project_data

#         instance = super().update(instance, validated_data)

#         return instance



# class ProjectSerializer(serializers.ModelSerializer):
#     """ Serializer for projects """

#     """ Add the project instances serializer """
#     #project_instances = ProjectInstanceSerializer(many=True, required = False)

#     class Meta:
#         model = Project
#         fields = ['id','project_title']
#         read_only_fields = ['id','company_name_project']

    # def _get_or_create_project_instances(self,project_instances,project):
    #     """ Handle getting or creating project_instances as needed """

    #     auth_user = self.context['request'].user
    #     for project_instance in project_instances:
    #         project_instance_obj, created = ProjectInstance.objects.get_or_create(
    #             user = auth_user,
    #             **project_instance,
    #         )
    #         project.project_instances.add(project_instance_obj)


    # def create(self,validated_data):
    #     """ Create project """

    #     project_instances = validated_data.pop('project_instances',[])

    #     project = Project.objects.create(**validated_data)

    #     self._get_or_create_project_instances(project_instances,project)

    #     return project


    # def update(self,instance,validated_data):
    #     """ Update project """
    #     project_instances = validated_data.pop('project_instances',[])

    #     if project_instances is not None:
    #         instance.project_instances.clear()
    #         self._get_or_create_project_instances(project_instances,instance)

    #     for attr, value in validated_data.items():
    #         setattr(instance,attr,value)

    #     instance.save()
    #     return instance









# class RecipeImageSerializer(serializers.ModelSerializer):
#     """ Serializer for uploading images to recipes """

#     class Meta:
#         model = Recipe
#         fields = ['id','image']
#         read_only_fields = ['id']
#         extra_kwargs = {'image':{'required':'True'}}

# from core.models import (
#     Recipe,
#     Tag,
#     Ingredient,
# )

# class IngredientSerializer(serializers.ModelSerializer):
#     """ Serializer for ingredients"""

#     class Meta:
#         model = Ingredient
#         fields = ['id','name']
#         read_only_fields = ['id']


# class TagSerializer(serializers.ModelSerializer):
#     """ Serializer for tags """

#     class Meta:
#         model = Tag
#         fields = ['id','name']
#         read_only_fields = ['id']

# """ Have to move the tag serializer above RecipeSerializer, as we're gunna nest it"""

# class RecipeSerializer(serializers.ModelSerializer):
#     """ Serializer for recipes """

#     tags = TagSerializer(many=True, required = False)
#     ingredients = IngredientSerializer(many=True, required = False)
#     """ By default, nested serializer is read only, have to overwrite methods to change that"""
#     class Meta:
#         model = Recipe
#         fields = ['id','title','time_minutes','price','link','tags','ingredients',]
#         read_only_fields = ['id']

#     def _get_or_create_tags(self,tags,recipe):
#         """ Handle getting or creating tags as needed """
#         auth_user = self.context['request'].user
#         for tag in tags:
#             tag_obj, created = Tag.objects.get_or_create(
#                 user = auth_user,
#                 **tag,
#             )
#             recipe.tags.add(tag_obj)

#     def _get_or_create_ingredients(self,ingredients,recipe):
#         """ Handle getting or creating ingredients as needed """
#         auth_user = self.context['request'].user
#         for ingredient in ingredients:
#             ingredient_obj, create = Ingredient.objects.get_or_create(
#                 user = auth_user,
#                 **ingredient,
#             )
#             recipe.ingredients.add(ingredient_obj)

#     """ Create this method here and then call in both create and update methods"""

#     def create(self, validated_data):
#         """ custome logic to create a recipe via serializer """
#         tags = validated_data.pop('tags',[])
#         ingredients = validated_data.pop('ingredients',[])
#         """ This takes (pops) the tags from the validated data and assigns to "tags" variable """
#         """ If it exists, take it, if not default to empty array []"""
#         recipe = Recipe.objects.create(**validated_data)
#         """ So, pop the tags and then create the recipe with the remaining validated data"""
#         #auth_user = self.context['request'].user
#         """ Gets the authenticated user"""
#         self._get_or_create_tags(tags,recipe)
#         self._get_or_create_ingredients(ingredients,recipe)
#         # for tag in tags:
#         #     tag_obj, created = Tag.objects.get_or_create(
#         #         user = auth_user,
#         #         **tag
#         #     )
#         #     recipe.tags.add(tag_obj)
#         # """ Add tags back in to recipe """
#         # """ Get or create is helper method, it gets value if already exists, or creates if not with vals you passed in"""
#         # """ This is the logic that avoids duplicate tags"""
#         # """ The **tag takes ALL VALUES stored in the tag, so in future if we add more attributes, they will be inluded"""
#         return recipe

#     def update(self,instance,validated_data):
#         """ Update recipe """
#         tags = validated_data.pop('tags',[])
#         ingredients = validated_data.pop('ingredients',[])

#         if tags is not None:
#             instance.tags.clear()
#             self._get_or_create_tags(tags,instance)

#         if ingredients is not None:
#             instance.ingredients.clear()
#             self._get_or_create_ingredients(ingredients,instance)

#         for attr, value in validated_data.items():
#             setattr(instance,attr,value)

#         instance.save()
#         return instance



# class RecipeDetailSerializer(RecipeSerializer):
#     """ Serializer for recipe detail view - its just an extension of the recipe serializer"""

#     class Meta(RecipeSerializer.Meta):
#         fields = RecipeSerializer.Meta.fields + ["description"]


