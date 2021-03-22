# Importing Django packages:
from django.apps import AppConfig, apps
from django.contrib.auth.management import create_permissions

class SocialMediaAPIConfig(AppConfig):
    name = 'social_media_api'
    verbose_name = "Social Media Data API" 
    app_description = "Lorem, ipsum dolor sit amet consectetur adipisicing elit. Repellat nemo ipsum aut fuga quasi eum distinctio odio earum veritatis esse, consequatur quo iure nulla maiores, quos neque id inventore, eaque eveniet eligendi repudiandae. Aperiam impedit eaque fugiat officiis ipsum doloremque, quibusdam tempore provident quasi cupiditate vitae nulla blanditiis officia omnis."

    def ready(self):
        """Upon startup writes MetaData about the Social Media API
         to the APIApplication database table.
        """
        # Importing API Applications Database Model:
        from accounts.models import APIApplication
        
        APIApplication.objects.update_or_create(
            module_name= self.name,
            defaults = {
                'app_name' : self.verbose_name,
                'app_description' : self.app_description
            }
        )



