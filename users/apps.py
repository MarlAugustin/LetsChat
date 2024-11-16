from django.apps import AppConfig

class UsersConfig(AppConfig):
    #THis is the configuration class for the users app where we can create user profile and save any changes
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        import users.signals
        