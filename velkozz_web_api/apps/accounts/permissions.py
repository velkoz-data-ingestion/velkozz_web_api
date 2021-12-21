# Importing local packages:
import copy

# Importing Django Permissions Objects:
from rest_framework.permissions import DjangoModelPermissions

class HasAPIAccess(DjangoModelPermissions):
    """
    An object that extends the base DjangoModelPermissions class to
    add the necessary additional permission functionality for each
    API data models.

    This is the permissions class that is added to the 'permission_classes'
    list in API ModelViewSets that maps the native Django database model
    permissions to requests made to the APIs.

    The database permissions that are mapped to HTTP requests at the ModelView
    level are:

    - POST --> add 
    - PUT & POST --> change
    - DELETE --> delete
    - GET --> view 

    """
    def __init__(self):
        # Copying over the perms_map dict's contents to be extended:
        self.perms_map = copy.deepcopy(self.perms_map)

        # Adding a key to perms_map dict adding GET request permission for
        # viewing a django model:
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']

# Method that ensures that only uses with staff status have access to a specific view:
def staff_check(user):
    """A method that checks if a user is a memeber of staff and returns true.
    It is used by the @user_passes_test() decorator to lock away views that should
    only be accessed by staff memebers.

    Returns: 
        Bool: The boolean indicating if a user is a staff memeber or not.

    """
    return user.is_staff
    