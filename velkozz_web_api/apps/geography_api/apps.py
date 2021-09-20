from django.apps import AppConfig


class GeographyApiConfig(AppConfig):
    name = 'geography_api'
    verbose_name = 'Geography Data API'
    app_description = "Lorem, ipsum dolor sit amet consectetur adipisicing elit. Repellat nemo ipsum aut fuga quasi eum distinctio odio earum veritatis esse, consequatur quo iure nulla maiores, quos neque id inventore, eaque eveniet eligendi repudiandae. Aperiam impedit eaque fugiat officiis ipsum doloremque, quibusdam tempore provident quasi cupiditate vitae nulla blanditiis officia omnis."

    def ready(self):
        """Upon startup writes MetaData about the Geography Data API
         to the APIApplication database table.
        """
        # Importing the API Applications data model:
        from accounts.models import APIApplication

        # Try Catch to aviod pre-migration crash:
        try:
            APIApplication.objects.update_or_create(
                module_name=self.name,
                defaults = {
                    'app_name' : self.verbose_name,
                    'app_description' : self.app_description
                }
            )
        except:
            pass