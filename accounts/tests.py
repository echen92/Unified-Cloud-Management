from django.test import TestCase
from django.test.client import Client
from accounts.views import *


class AccountsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.demo_user = User.objects.create_user(username='demo_user', email='demo@user.com',
                                                  password='qwerty123', first_name='', last_name='')
        self.demo_user.save()
        self.user_profile = UserProfile(user=self.demo_user)
        self.user_profile.save()

    def test_valid_email(self):
        email1 = 'testmail.cu'
        email2 = 'testmail%$#.com'
        email3 = 'test@#.com'
        email4 = 'test@mail.com'
        email5 = ''

        self.assertFalse(valid_email_address(email1))
        self.assertFalse(valid_email_address(email2))
        self.assertFalse(valid_email_address(email3))
        self.assertFalse(valid_email_address(email5))
        self.assertTrue(valid_email_address(email4))

    def test_valid_password(self):
        tooshort = 'short'
        blank = ''
        valid = 'qwerty123'

        short = check_valid_password(tooshort, tooshort)
        none = check_valid_password(blank, blank)
        notmatching1 = check_valid_password(tooshort, 'blah')
        notmatching2 = check_valid_password(blank, 'asdf')
        validpw = check_valid_password(valid, valid)

        self.assertFalse(short)
        self.assertFalse(none)
        self.assertFalse(notmatching1)
        self.assertFalse(notmatching2)
        self.assertTrue(validpw)

    def test_unique_user(self):
        email1 = 'test1@xyz.com'
        email2 = 'test2@xyz.com'
        password = 'qwerty123'

        # Create the user object in the DB
        User.objects.create_user(username_md5(email1), email1, password, first_name="", last_name="")

        # email1 already exists in DB, thus it should return false
        user1_not_unique = unique_user(email1)
        self.assertFalse(user1_not_unique)

        user2_unique = unique_user(email2)
        self.assertTrue(user2_unique)