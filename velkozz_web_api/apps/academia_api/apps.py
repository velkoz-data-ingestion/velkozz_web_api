from django.apps import AppConfig


class AcademiaApiConfig(AppConfig):
    name = 'academia_api'
    verbose_name = "Academia Data API"
    app_description = "Lorem, ipsum dolor sit amet consectetur adipisicing elit. Repellat nemo ipsum aut fuga quasi eum distinctio odio earum veritatis esse, consequatur quo iure nulla maiores, quos neque id inventore, eaque eveniet eligendi repudiandae. Aperiam impedit eaque fugiat officiis ipsum doloremque, quibusdam tempore provident quasi cupiditate vitae nulla blanditiis officia omnis."

    def ready(self):
        """Upon startup writes MetaData about the Academia Data API
         to the APIApplication database table.
        """
        # Importing the API Application data model:
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
