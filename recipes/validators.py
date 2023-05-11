from django.core.exceptions import ValidationError
from pint.errors import UndefinedUnitError
import pint


def check_valid_value(value):
    registry = pint.UnitRegistry()
    try:
        registry[value]
    except UndefinedUnitError:
        raise ValidationError(f'{value} is not valid')
    except:
        raise ValidationError(f'{value} unknown error')

# list_value = ['kg', 'pound', 'pkg', 'mg']
# def check_valid_value(value):
#     if value not in list_value:
#         raise ValidationError(f'{value} is not valid')
