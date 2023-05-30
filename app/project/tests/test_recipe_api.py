# """ Tests for project APIs """

from decimal import Decimal
import tempfile
import os

from PIL import Image

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Project,ProjectInstance
)
from project.serializers import (
    ProjectSerializer,
)
""" Have a simple serializer which just lists all recipes, then have a detailed one which the user can"""
""" click to access more details about that recipe"""


PROJECTS_URL = reverse('project-list')

def detail_url(project_id):
    """ Create and return a project detail URL. This is a function and not hard coded as the URL is dynamic, changes depending on id """
    return reverse('project:project-detail',args=[project_id])

def create_user(**params):
    """ Create and return a new user"""
    return get_user_model().objects.create_user(**params)

def create_project(user,**params):
    """ Create and return a sample project """
    defaults = {
        'project_title' : 'Sample project title',
        }

    defaults.update(params)
    """ SO this creates a project instance with default parameters, if we want to update certain params, we can do"""
    """ create project (user, 'project_title'="testProject") for eg, it will update project_title and use defaults for the rest"""

    project = Project.objects.create(user = user,**defaults)

    return project


class PrivateRecipeAPITests(TestCase):
    """ Test authenticated API requests """

    def setUp(self):

        self.client = APIClient()
        """ Gives us a test client """
        self.user = create_user(email='user@example.com', password = 'testpass123')
        self.client.force_authenticate(self.user)

    def test_creating_two_projects_same_company(self):

            user1 = get_user_model().objects.create_user(
                email = "aaron@test.com",
                password = "password"
            )

            user2 = get_user_model().objects.create_user(
                email = "marina@test.com",
                password = "password1"
            )

            aaron_project = Project.objects.create(user = user1, project_title = "AaronProject")
            marina_project = Project.objects.create(user = user2, project_title = "MarinaProject")

            #print(aaron_project.user)
            #print(aaron_project.user.company_name)

            projects = Project.objects.filter(company_name_project=user1.company_name)

            self.assertEqual(projects.count(),2)

    def test_retrieve_project(self):
        """ Test retrieveing a list of projects """
        create_project(user=self.user)
        Project.objects.create(user = self.user, project_title = "AaronProject")
        """ Crete two identical project instances """

        res = self.client.get(PROJECTS_URL)
        """call here the url and assign the values to response, this makes the request to the API"""

        projects = Project.objects.all().order_by('-id')
        """ Return list of recipes but ID, in reverse order"""

        serializer = ProjectSerializer(projects, many=True)

        self.assertEqual(res.status_code,status.HTTP_200_OK)
        #self.assertEqual(res.data,serializer.data)
        """ Check that the response dictionary (res.data) is equal to data dictionary of object passed through serializer"""

    # def test_project_list_limited_to_company(self):
    #     """ Test list of projects is limited to authenticated user """
    #     other_user = create_user(email = 'other@testing.com', password = 'otherpass123')

    #     create_project(user=other_user)
    #     create_project(user=self.user)

    #     """ Here we have created a project from 2 users, one is "Other user" and one is our authenticated user from above"""

    #     res = self.client.get(PROJECTS_URL)
    #     """ Here we should only see the project for the authenticated (logged in) user"""

    #     projects = Project.objects.filter(company_name_project=self.user.company_name)
    #     # make sure you filter by company name
    #     serializer = ProjectSummarySerializer(projects, many=True)

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data,serializer.data)

    # def test_create_project(self):
    #     """ Test creating a project """
    #     payload = {
    #         'project_title':'New Exciting Project',
    #         }

    #     res = self.client.post(PROJECTS_URL, payload)
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        #project = Project.objects.get(id = res.data['id'])

        #self.assertEqual(project.user, self.user)



    # def test_partial_update_of_project(self):
    #     """ Test a partial update of a project """
    #     project = create_project(
    #         user = self.user,
    #         project_title = 'Sample recipe title',
    #         )

    #     payload = {'project_title':'New Project title'}
    #     url = detail_url(project.id)
    #     res = self.client.patch(url, payload)

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     project.refresh_from_db()
    #     self.assertEqual(project.project_title,payload['project_title'])
    #     self.assertEqual(project.user,self.user)
    #     self.assertEqual(project.company_name_project,self.user.company_name)

    # def test_create_project_with_new_tags(self):
    #     """ Test creating a new project with tags """

    #     payload = {
    #         'project_title':'HMT',
    #         'project_instances':[{'project_instance_name':'Thai'},{'project_instance_name':'Dinner'}]
    #     }

    #     res = self.client.post(PROJECTS_URL,payload,format='json')

    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    #     """" Expect 201 response when successfully created"""
    #     projects = Project.objects.filter(company_name_project=self.user.company_name)

    #     self.assertEqual(projects.count(),1)
    #     project = projects[0]
    #     self.assertEqual(project.project_instances.count(),2)
    #     for project_instance in payload['project_instances']:

    #         exists = project.project_instances.filter(
    #             project_instance_name = project_instance['project_instance_name'],
    #             user = self.user,
    #         ).exists()
    #         self.assertTrue(exists)


    # def test_create_project_with_existing_instances(self):
    #     """ TEst creating a project with existsing instances"""
    #     instance_new_wave = ProjectInstance.objects.create(user=self.user,project_instance_name='Wave 3')
    #     payload = {
    #         'project_title':'HMT',
    #         'project_instances':[{'project_instance_name':'Wave 3'},{'project_instance_name':'Wave 4'}],
    #     }
    #     """ So one tag in the create recipe already exists as we explictly created it above (Wave 3)"""

    #     res = self.client.post(PROJECTS_URL,payload,format='json')

    #     """ Expected behaviour here is to have 2 instances (Wave 3 and Wave 2) and not to have 3 (a dupe Wave 3 instance)"""

    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     projects = Project.objects.filter(company_name_project=self.user.company_name)
    #     self.assertEqual(projects.count(),1)
    #     project = projects[0]
    #     self.assertEqual(project.project_instances.count(),2)
    #     self.assertIn(instance_new_wave,project.project_instances.all())
    #     """This is testing, does the tag_indian exist, or has it created a duplicate"""
    #     for project_instance in payload['project_instances']:
    #         exists = project.project_instances.filter(
    #             project_instance_name = project_instance['project_instance_name'],
    #             user = self.user,
    #         ).exists()
    #         self.assertTrue(exists)

    # def test_create_tag_on_update_recipe(self):
    #     """ If we update a project, but provide a instance that does not exist, then create that instance in system"""
    #     project = create_project(user=self.user)
    #     """This is the helper function we created to make a generic recipe"""
    #     payload = {'project_instances':[{'project_instance_name':'Wave 100'}]}

    #     url = detail_url(project.id)

    #     res=self.client.patch(url,payload,format='json')

    #     self.assertEqual(res.status_code,status.HTTP_200_OK)

    #     new_instance = ProjectInstance.objects.get(user=self.user,project_instance_name='Wave 100')

    #     self.assertIn(new_instance,project.project_instances.all())


    # def test_create_project_with_new_tags_and_user_with_same_company_can_see(self):

    #     user1 = get_user_model().objects.create_user(
    #             email = "aaron@stack.com",
    #             password = "password"
    #         )

    #     user2 = get_user_model().objects.create_user(
    #             email = "marina@stack.com",
    #             password = "password1"
    #         )

    #     payload_user1_project = {
    #         'project_title':'HMT',
    #         'project_instances':[{'project_instance_name':'Thai'},{'project_instance_name':'Dinner'}]
    #     }

    #     self.client.force_authenticate(user1)

    #     res = self.client.post(PROJECTS_URL,payload_user1_project,format='json')

    #     """ res.data should equal Projects filtered by user2 (as they're the same company)"""

    #     projects_user_2 = Project.objects.filter(company_name_project=user2.company_name)

    #     ind_project_user_2 = projects_user_2[0]
    #     print(res.data)
    #     print(projects_user_2)
    #     print(ind_project_user_2)

        #print(ind_project_user_2.project_instances)



    # def test_create_recipe_with_new_tags(self):
    #     """ Test creating a new recipe with tags """
    #     payload = {
    #         'title':'Thai prawn curry',
    #         'time_minutes':30,
    #         'price':Decimal('2.50'),
    #         'tags':[{'name':'Thai'},{'name':'Dinner'}]
    #     }
#         res = self.client.post(RECIPES_URL,payload,format='json')

#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)
#         """" Expect 201 response when successfully created"""
#         recipes = Recipe.objects.filter(user=self.user)

#         self.assertEqual(recipes.count(),1)
#         recipe = recipes[0]
#         self.assertEqual(recipe.tags.count(),2)
#         for tag in payload['tags']:
#             exists = recipe.tags.filter(
#                 name = tag['name'],
#                 user = self.user,
#             ).exists()
#             self.assertTrue(exists)











# from decimal import Decimal
# import tempfile
# import os

# from PIL import Image

# from django.contrib.auth import get_user_model
# from django.test import TestCase
# from django.urls import reverse

# from rest_framework import status
# from rest_framework.test import APIClient

# from core.models import (
#     Recipe,
#     Tag,
#     Ingredient,
# )
# from recipe.serializers import (
#     RecipeSerializer,
#     RecipeDetailSerializer,
# )
# """ Have a simple serializer which just lists all recipes, then have a detailed one which the user can"""
# """ click to access more details about that recipe"""



# RECIPES_URL = reverse('recipe:recipe-list')

# def detail_url(recipe_id):
#     """ Create and return a recipe detail URL. This is a function and not hard coded as the URL is dynamic, changes depending on id """
#     return reverse('recipe:recipe-detail',args=[recipe_id])


# def image_upload_url(recipe_id):
#     """ Create and return and image upload URL """
#     return reverse('recipe:recipe-upload-image',args=[recipe_id])


# def create_recipe(user,**params):
#     """ Create and return a sample recipe """
#     defaults = {
#         'title' : 'Sample recipe title',
#         'time_minutes':22,
#         'price':Decimal('5.5'),
#         'description':'Sample description',
#         'link':'http://example.com/recipe.pdf',
#         }

#     defaults.update(params)
#     """ SO this creates a recipe instance with default parameters, if we want to update certain params, we can do"""
#     """ create reciepe (user, 'time_minutes'=24) for eg, it will update time_minutes and use defaults for the rest"""

#     recipe = Recipe.objects.create(user = user,**defaults)

#     return recipe


# def create_user(**params):
#     """ Create and return a new user"""
#     return get_user_model().objects.create_user(**params)

# """ Just creating the helper function above to quickly create users for unit tests"""


# class PublicRecipeAPITests(TestCase):
#     """ Test unathenticated API requests """

#     def setUp(self):

#         self.client = APIClient()
#         """ Gives us a test client """

#     def test_auth_required(self):
#         """" Test authorisation is required to retrieve recipes """
#         res = self.client.get(RECIPES_URL)

#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


# class PrivateRecipeAPITests(TestCase):
#     """ Test authenticated API requests """

#     def setUp(self):

#         self.client = APIClient()
#         """ Gives us a test client """
#         self.user = create_user(email='user@example.com', password = 'testpass123')
#         self.client.force_authenticate(self.user)

#     def test_retrieve_recipes(self):
#         """ Test retrieveing a list of recipes """
#         create_recipe(user=self.user)
#         create_recipe(user=self.user)
#         """ Crete two identical recipe instances """

#         res = self.client.get(RECIPES_URL)
#         """call here the url and assign the values to response, this makes the request to the API"""

#         recipes = Recipe.objects.all().order_by('-id')
#         """ Return list of recipes but ID, in reverse order"""

#         serializer = RecipeSerializer(recipes, many=True)
#         self.assertEqual(res.status_code,status.HTTP_200_OK)
#         self.assertEqual(res.data,serializer.data)
#         """ Check that the response dictionary (res.data) is equal to data dictionary of object passed through serializer"""


#     def test_recipe_list_limited_to_user(self):
#         """ Test list of recipe is limited to authenticated user """
#         other_user = create_user(email = 'other@example.com', password = 'otherpass123')

#         create_recipe(user=other_user)
#         create_recipe(user=self.user)

#         """ Here we have created a recipie from 2 users, one is "Other user" and one is our authenticated user from above"""

#         res = self.client.get(RECIPES_URL)
#         """ Here we should only see the recipe for the authenticated (logged in) user"""

#         recipes = Recipe.objects.filter(user=self.user)
#         serializer = RecipeSerializer(recipes, many=True)

#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data,serializer.data)

#     def test_get_recipe_detail(self):
#         """ Test get recipe detail"""
#         recipe = create_recipe(user=self.user)

#         url = detail_url(recipe.id)
#         res = self.client.get(url)

#         serializer = RecipeDetailSerializer(recipe)
#         self.assertAlmostEqual(res.data, serializer.data)

#     def test_create_recipe(self):
#         """ Test creating a recipe """
#         payload = {
#             'title':'sample recipe',
#             'time_minutes':30,
#             'price':Decimal('5.9'),
#             }

#         res = self.client.post(RECIPES_URL, payload)

#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)
#         recipe = Recipe.objects.get(id = res.data['id'])

#         for k,v in payload.items():
#             self.assertEqual(getattr(recipe,k),v)
#             """ getattr is a python function """
#         self.assertEqual(recipe.user, self.user)

#     def test_partial_update(self):
#         """ Test a partial update of a recipe """
#         original_link = "https://example.com/recipe.pdf"
#         """ Create and orginal link here to test patching the title but keeping other fields (i.e the link) the same"""
#         recipe = create_recipe(
#             self.user,
#             title = 'Sample recipe title',
#             link = original_link,
#             )

#         payload = {'title':'New recipe title'}
#         url = detail_url(recipe.id)
#         res = self.client.patch(url, payload)

#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         recipe.refresh_from_db()
#         self.assertEqual(recipe.title,payload['title'])
#         self.assertEqual(recipe.link,original_link)
#         self.assertEqual(recipe.user,self.user)

#     def test_full_update(self):
#             """ Test a full update of a recipe """

#             recipe = create_recipe(
#                 self.user,
#                 title = 'Sample recipe title',
#                 link = 'https://example.com/recipe.pdf',
#                 description = "sample recipe description"
#                 )

#             payload = {
#                 'title':'New recipe title',
#                 'link': 'https://example.com/new-recipe.pdf',
#                 'description' : "new recipe description",
#                 'time_minutes':10,
#                 'price':Decimal('2.50'),
#             }

#             url = detail_url(recipe.id)
#             res = self.client.put(url,payload)

#             self.assertEqual(res.status_code, status.HTTP_200_OK)
#             recipe.refresh_from_db()

#             for k,v in payload.items():
#                 self.assertEqual(getattr(recipe,k),v)
#                 """ getattr is a python function """
#             self.assertEqual(recipe.user, self.user)

#     def test_create_recipe_with_new_tags(self):
#         """ Test creating a new recipe with tags """
#         payload = {
#             'title':'Thai prawn curry',
#             'time_minutes':30,
#             'price':Decimal('2.50'),
#             'tags':[{'name':'Thai'},{'name':'Dinner'}]
#         }
#         res = self.client.post(RECIPES_URL,payload,format='json')

#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)
#         """" Expect 201 response when successfully created"""
#         recipes = Recipe.objects.filter(user=self.user)

#         self.assertEqual(recipes.count(),1)
#         recipe = recipes[0]
#         self.assertEqual(recipe.tags.count(),2)
#         for tag in payload['tags']:
#             exists = recipe.tags.filter(
#                 name = tag['name'],
#                 user = self.user,
#             ).exists()
#             self.assertTrue(exists)

#     def test_create_recipe_with_existing_tag(self):
#         """ TEst creating a recipe with existsing tag"""
#         tag_indian = Tag.objects.create(user=self.user,name='Indian')
#         payload = {
#             'title':'Pongal',
#             'time_minutes':60,
#             'price':Decimal('4.50'),
#             'tags':[{'name':'Indian'},{'name':'Breakfast'}],
#         }
#         """ So one tag in the create recipe already exists as we explictly created it above (Indian)"""

#         res = self.client.post(RECIPES_URL,payload,format='json')

#         """ Expected behaviour here is to have 2 tags (Indian and Brekfast) and not to have 3 (a dupe Indian tag)"""

#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)
#         recipes = Recipe.objects.filter(user=self.user)
#         self.assertEqual(recipes.count(),1)
#         recipe = recipes[0]
#         self.assertEqual(recipe.tags.count(),2)
#         self.assertIn(tag_indian,recipe.tags.all())
#         """This is testing, does the tag_indian exist, or has it created a duplicate"""
#         for tag in payload['tags']:
#             exists = recipe.tags.filter(
#                 name = tag['name'],
#                 user = self.user,
#             ).exists()
#             self.assertTrue(exists)


#     def test_create_tag_on_update_recipe(self):
#         """ If we update a recipe, but provide a tag that does not exist, then create that tag in system"""
#         recipe = create_recipe(user=self.user)
#         """This is the helper function we created to make a generic recipe"""
#         payload = {'tags':[{'name':'Lunch'}]}
#         url = detail_url(recipe.id)
#         res=self.client.patch(url,payload,format='json')

#         self.assertEqual(res.status_code,status.HTTP_200_OK)

#         new_tag = Tag.objects.get(user=self.user,name='Lunch')
#         self.assertIn(new_tag,recipe.tags.all())

#     def test_update_recipe_assign_tag(self):
#         """ Test assigning an existing tag when updating a recipe"""
#         tag_breakfast = Tag.objects.create(user=self.user, name='Breakfast')
#         recipe = create_recipe(user=self.user)
#         recipe.tags.add(tag_breakfast)

#         """ Create a breakfast tag, create generic recipe and then assign tag to recipe ^^"""

#         tag_lunch = Tag.objects.create(user=self.user,name='Lunch')
#         payload = {'tags':[{'name':'Lunch'}]}

#         """ Create a lunch tag and then a payload designed to change the tags of our recipe"""
#         """ In this case, we are changing breakfast tag to lunch in the recipe"""
#         url = detail_url(recipe.id)
#         res = self.client.patch(url, payload,format='json')

#         self.assertEqual(res.status_code,status.HTTP_200_OK)
#         self.assertIn(tag_lunch,recipe.tags.all())
#         self.assertNotIn(tag_breakfast,recipe.tags.all())

#     def test_clear_recipe_tags(self):
#         """ Test clearing a recipes tags"""

#         tag = Tag.objects.create(user=self.user, name='Dessert')
#         recipe = create_recipe(user=self.user)
#         recipe.tags.add(tag)

#         payload = {'tags':[]}
#         """Passing an empty list of tags and then patching that will clear all tags"""
#         url = detail_url(recipe.id)
#         res = self.client.patch(url, payload,format='json')

#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(recipe.tags.count(),0)

#     def test_create_recipe_with_new_ingredients(self):

#         """Test creating a new recipe with ingredients """

#         payload = {
#             'title':'Cauliflower Tacos',
#             'time_minutes':60,
#             'price':Decimal('4.30'),
#             'ingredients':[{'name':'Cauliflower'},{'name':'salt'}]
#         }
#         res = self.client.post(RECIPES_URL, payload,format='json')
#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)
#         recipes = Recipe.objects.filter(user=self.user)
#         self.assertEqual(recipes.count(),1)
#         recipe = recipes[0]
#         self.assertEqual(recipe.ingredients.count(),2)
#         for ingredient in payload['ingredients']:
#             exists = recipe.ingredients.filter(
#                 name = ingredient['name'],
#                 user = self.user,
#             ).exists()
#             self.assertTrue(exists)

#     def test_create_recipe_with_existing_ingredient(self):
#         """Test creating a new recipe with existing ingredient."""
#         ingredient = Ingredient.objects.create(user=self.user, name='Lemon')
#         payload = {
#             'title': 'Vietnamese Soup',
#             'time_minutes': 25,
#             'price': '2.55',
#             'ingredients': [{'name': 'Lemon'}, {'name': 'Fish Sauce'}],
#         }
#         res = self.client.post(RECIPES_URL, payload, format='json')

#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)
#         recipes = Recipe.objects.filter(user=self.user)
#         self.assertEqual(recipes.count(), 1)
#         recipe = recipes[0]
#         self.assertEqual(recipe.ingredients.count(), 2)
#         self.assertIn(ingredient, recipe.ingredients.all())
#         for ingredient in payload['ingredients']:
#             exists = recipe.ingredients.filter(
#                 name=ingredient['name'],
#                 user=self.user,
#             ).exists()
#             self.assertTrue(exists)

#     def test_create_ingredient_on_update(self):
#         """ Testing creating an ingredient when updating a recipe"""

#         recipe = create_recipe(user=self.user)

#         payload = {'ingredients':[{'name':'Limes'}]}
#         url = detail_url(recipe.id)
#         res = self.client.patch(url,payload,format='json')

#         self.assertEqual(res.status_code,status.HTTP_200_OK)
#         new_ingredient = Ingredient.objects.get(user=self.user,name='Limes')
#         self.assertIn(new_ingredient, recipe.ingredients.all())

#     def test_update_recipe_assign_ingredient(self):
#         """Test assigning an existing ingredient when updating a recipe"""
#         ingredient1 = Ingredient.objects.create(user = self.user, name = "pepper")

#         recipe = create_recipe(user=self.user)
#         recipe.ingredients.add(ingredient1)

#         ingredient2 = Ingredient.objects.create(user = self.user, name = "chili")
#         payload = {'ingredients':[{'name':'chili'}]}
#         url = detail_url(recipe.id)
#         res = self.client.patch(url,payload,format='json')

#         self.assertEqual(res.status_code,status.HTTP_200_OK)
#         self.assertIn(ingredient2, recipe.ingredients.all())
#         self.assertNotIn(ingredient1, recipe.ingredients.all())

#     def test_clear_recipe_ingredients(self):
#         """ Test clearing a recipe's ingredient """
#         ingredient = Ingredient.objects.create(user=self.user, name = "Garlic")
#         recipe = create_recipe(user=self.user)
#         recipe.ingredients.add(ingredient)

#         payload = {'ingredients':[]}
#         url = detail_url(recipe.id)
#         res = self.client.patch(url,payload,format='json')

#         self.assertEqual(res.status_code,status.HTTP_200_OK)
#         self.assertEqual(recipe.ingredients.count(),0)


# class ImageUploadTests(TestCase):
#     """ Tests for image upload API """

#     def setUp(self):
#         self.client = APIClient()
#         self.user = get_user_model().objects.create_user(
#             'user@example.com',
#             'password123',
#         )
#         self.client.force_authenticate(self.user)
#         self.recipe = create_recipe(user=self.user)

#     def tearDown(self):
#         self.recipe.image.delete()

#         """ tear down is similar to set up, but set up executes BEFORE tests, tear down executes AFTER tests"""

#     def test_upload_image(self):
#         """ Test uploading an image to a recipe """
#         url = image_upload_url(self.recipe.id)
#         with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
#             img = Image.new('RGB', (10, 10))
#             """ img mimicks a user upload"""
#             img.save(image_file, format = 'JPEG')
#             """ save img to "image_file" which is the temp file we created """
#             image_file.seek(0)
#             payload = {'image': image_file}
#             res = self.client.post(url,payload,format='multipart')
#             """ multipart form, upload is multipart as it has text and binary data """

#         """ NamedTemporaryFile is a python helper module which allows you to create temp files when working with python code.  """
#         """ It will create a temp file whilst we're in the context manager (the block with "with") """
#         """ As soon as with block ends, temp file is cleaned up"""

#         self.recipe.refresh_from_db()
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertIn('image',res.data)
#         self.assertTrue(os.path.exists(self.recipe.image.path))

#     def test_upload_image_bad_request(self):
#         """Test uploading invalid image """
#         url = image_upload_url(self.recipe.id)
#         payload = {'image': "notanimage"}
#         """pass a string (i.e not an image) to the payload """
#         res = self.client.post(url,payload,format='multipart')

#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)























