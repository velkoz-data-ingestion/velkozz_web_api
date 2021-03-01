# Importing native django storage methods:
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models

# Import 3rd party packages:
import os

class OHLCOverwriteStorage(FileSystemStorage):
    """A basic FileSystemStorage object that overwrites existing instances
    of a static file. 
    
    Used in the SecurityPriceOHLC data model to 'update' historical price 
    csv files.

    """
    def get_available_name(self, name, max_length):
        
        if self.exists(name):
            os.remove(os.path.join(self.location, name))

        return super(OHLCOverwriteStorage, self).get_available_name(name, max_length)