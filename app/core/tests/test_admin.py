""" Tests for django admin mods """

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTets(TestCase):

    """ Tests for Django admin """

    def setUp(self):

        self.client = Client()
        """ Allows us to make http requests """
        self.admin_user = get_user_model().objects.create_superuser(
            email = 'admin@example.com',
            password = 'test',
        )

        self.client.force_login(self.admin_user)
        """ force login so test forces past authentication """

        self.user = get_user_model().objects.create_user(
            email = 'user@example.com',
            password = 'test123',
            name = 'Test User',
        )

        """This is just so when we run tests we have users to test with """


    def test_users_list(self):
        """ Test that users are listed on page """
        url = reverse('admin:core_user_changelist')
        """ Determines which url we are going to pull from django admin, all defined in d-admin docs. This gets the page of list of users"""
        res = self.client.get(url)
        """Makes a http get request, and makes request from user we forced to login (super user above)"""
        self.assertContains(res,self.user.name)
        """" Does the page contain the name of the user ?"""
        self.assertContains(res,self.user.email)
        """ Does the page contain the email of the user? """

    def test_edit_user_page(self):
        """Test edit user page works"""
        url = reverse('admin:core_user_change',args=[self.user.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code,200)

    def test_create_user_page(self):
        """ Test the create user page works - this is when you press "create user" in django admin """
        url = reverse('admin:core_user_add')
        res = self.client.get(url)
        self.assertEqual(res.status_code,200)


