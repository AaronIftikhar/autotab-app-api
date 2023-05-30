""" Tests for models """
from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from core.models import Project

def create_user(email='user@example.com',password='testpass123'):
    """ Create and return new user, helper function to use for testing """
    return get_user_model().objects.create_user(email,password)


# def create_project(user):
#     project = Project.objects.create(user = user)
#     return project

class ModelTests(TestCase):
    """ Test models"""

    def test_create_user_with_email_successful(self):

        """ Test creating a user with email is successful"""

        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email = email,
            password = password
        )

        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))
        """ check_password as we'll used a hashed password """

    def test_new_user_email_normalised(self):
        """ Test email is normalised for new users """

        sample_emails = [
            ['test1@EXAMPLE.com','test1@example.com'],
            ['Test2@Example.com','Test2@example.com'],
            ['TEST3@EXAMPLE.com','TEST3@example.com'],
            ['test4@Example.COM','test4@example.com'],
        ]

        for email, expected in sample_emails:
            """ syntax to loop through list with two variables in python"""
            user = get_user_model().objects.create_user(email,"sample123")

            self.assertEqual(user.email, expected)


    def test_new_user_without_email_raises_error(self):
        """ Creating a user without an email raised an error """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('','test123')

    def test_create_superuser(self):
        """ Test creating a super user"""

        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    """ Testing adding the company field """



    def test_creating_a_company_dynamically_from_user(self):

        self.user = create_user(email='peter@bostonUni.com', password = 'testpass123')

        company_name = self.user.company_name

        company_str_1 = (str(self.user.email)).split("@",1)[1]
        company_str_2 = company_str_1.split('.')[0]

        self.assertEqual(company_name,company_str_2)









    # """ Client tests below """

    # def test_create_client(self):
    #     """ Test creating a client successful """
    #     user = get_user_model().objects.create_user(
    #         'test@example.com',
    #         'testpass123',
    #     )

    #     client = models.Client.objects.create(
    #         user = user,
    #         company = user.company,
    #         title = "Test client 1",
    #     )

    #     company_str_1 = (str(user.email)).split("@",1)[1]
    #     company_str_2 = company_str_1.split('.')[0]

    #     self.assertEqual(str(client), client.title)
    #     self.assertEqual(client.company, company_str_2)

    # def test_create_tag(self):
    #     """ Test creating a tag is successful """
    #     user = create_user()
    #     tag = models.Tag.objects.create(user=user,name="Tag1")

    #     self.assertEqual(str(tag),tag.name)

    # def test_create_ingridient(self):
    #     """Test creating an ingridient successful"""
    #     user = create_user()
    #     ingredient = models.Ingredient.objects.create(
    #         user = user,
    #         name = "Ingredient 1",
    #     )

    #     self.assertEqual(str(ingredient),ingredient.name)

    # @patch('core.models.uuid.uuid4')
    # def test_recipe_file_name_uuid(self,mock_uuid):
    #     """ Test generating image path, uuid = unique name for file """
    #     uuid = 'test-uuid'
    #     """ This is the mocked response, uuid is usually a difficult and long unique id, which would"""
    #     """ be annoying when developing"""
    #     mock_uuid.return_value = uuid
    #     file_path = models.recipe_image_file_path(None, 'example.jpg')

    #     self.assertEqual(file_path,f'uploads/recipe/{uuid}.jpg')

    # """ The patch is used to mimick the uuid function """



