import os
from django.contrib.auth.password_validation import validate_password

from django.test import TestCase


class EnvironVariableTest(TestCase):
    def test_secret_key(self):
        secret_key = os.environ.get('SECRET_KEY')
        try:
            validate_password(secret_key)
        except AssertionError as e:
            self.fail(e)
        self.assertEqual(secret_key, 'g@i(ljz%@p3)ymt0h)o6@3ywm8y-2ahkpmt+7pav6e4zf+u%51')


# class MyTestCase(TestCase):
#     def test_my_function_raises_exception(self):
#         def my_function(x):
#             return 2 / x
#
#         with self.assertRaises(ZeroDivisionError, msg='Raise exception only share by zero ') as cm:
#             my_function(2)
# the_exception = cm.exception
# self.assertEqual(str(the_exception), 'division by zero')
