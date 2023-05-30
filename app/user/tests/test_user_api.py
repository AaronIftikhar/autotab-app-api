""" Tests for the user API """

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')
""" Me url sets the url to test"""


def create_user(**params):
    """ Create and return a new user """
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """ Test the public features of the user API """

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """ Test creating a user is succesful """
        payload = {
            'email':'test@example.com',
            'password':'testpass123',
            'name':'Test Name',
            }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))

        self.assertNotIn('password',res.data)


    def test_user_with_email_exists_error(self):
        """ Tes error returned if user with email exists """

        payload = {
            'email':'test@example.com',
            'password':'testpass123',
            'name':'Test Name',
            }

        """ Above is same email as the email of the user we already created, so should return an error """

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL,payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """ Test an error is returned if password less than 5 chars"""
        payload = {
            'email':'test@example.com',
            'password':'pw',
            'name':'Test Name',
            }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email = payload['email']
        ).exists()
        self.assertFalse(user_exists)
        """ USer should not exist as it should not have been created (pw too short)"""

    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""
        user_details = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'test-user-password123',
        }
        get_user_model().objects.create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_create_token_bad_credentials(self):
        """ Test returns error if creds invalid """
        create_user(email='test@example.com', password = 'goodpass')

        payload = {'email':'test@example.com','password':'badpass'}

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token',res.data)
        """ There should not be a token in the data, as the pass words are incorrect"""

        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """ Test posting a blank password returnd an error """
        payload = {'email':'test@example.com','password':''}

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token',res.data)
        """ There should not be a token in the data, as the pass words are incorrect"""

        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """ Check that authentication is required and enforced for ME url endpoint """

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        """The base class is public user api test (see above) - we don't do any authentication here, so we're making an unauthorized reuqest, hence expect a unauth response """

""" These are for test cases that require authentication """
class PrivateUserApiTests(TestCase):
    """Set up method is called automatically before each test, so we'll set authentication there"""

    def setUp(self):
        self.user = create_user(
            email = 'test@email.com',
            password = 'testpass123',
            name = 'Test Name',
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        """ Force the user to login, so we can do unit tests for authenticated users. All requests from this client will be authentciated """

    def test_retrieve_profile_success(self):
        """ Test retrieveing profile for logged in user """
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data,{
            'name':self.user.name,
            'email':self.user.email,
        })

    def test_post_me_not_allowed(self):
        """ Test post is not allowed for me endpoint """

        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        """ Here we're checking that post method is not allowed for me endpoint, only put and patch should be allowed """

    def test_update_user_profile(self):
        """ Test updating user profile for the authenticated user"""

        payload = {'name':'Updated name', 'password':'newpassword123'}

        res = self.client.patch(ME_URL, payload)
        """ This is making the patch request to update"""

        self.user.refresh_from_db()
        """ This refreshed the user details in db"""
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)