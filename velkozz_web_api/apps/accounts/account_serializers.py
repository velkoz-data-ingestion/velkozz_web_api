# Importing seralizer methods: 
from rest_framework import serializers

# Importing 3rd party Request log method:
from request.models import Request

# Generic Request Seralizer:
class RequestSerializer(serializers.Serializer):
    
    # Manually adding fields because setting Meta fields and model appear broken for 3rd party objects?
    time = serializers.DateTimeField()
    response = serializers.IntegerField()
    method = serializers.CharField()
    path = serializers.CharField()
    is_secure = serializers.BooleanField()
    is_ajax = serializers.BooleanField()
    ip = serializers.IPAddressField()
    user = serializers.CharField()
    referer = serializers.CharField()
    user_agent = serializers.CharField()
    language = serializers.CharField()
    
    class Meta:
        fields = "__all__"
        model = Request


class SettingsSerializer(serializers.Serializer):

    # Adding the relevant settings fields that should be seralized for diagnostic purposes:
    DEBUG = serializers.BooleanField()
    BASE_DIR = serializers.CharField()
    ALLOWED_HOSTS = serializers.ListField()
    LOGIN_REDIRECT_URL = serializers.CharField()
    INSTALLED_APPS = serializers.ListField()
    MIDDLEWARE = serializers.ListField()
    TEMPLATES = serializers.ListField()
    WSGI_APPLICATION = serializers.CharField()
    DATABASES = serializers.ListField()
    AUTH_PASSWORD_VALIDATORS = serializers.ListField()
    REST_FRAMEWORK = serializers.ListField()
    LANGUAGE_CODE = serializers.CharField()
    TIME_ZONE = serializers.CharField()
    USE_I18N = serializers.BooleanField()
    USE_L10N = serializers.BooleanField()
    USE_TZ = serializers.BooleanField()

    STATIC_URL = serializers.CharField()
    STATIC_ROOT = serializers.CharField()
    STATICFILES_DIRS = serializers.ListField()
    MEDIA_ROOT = serializers.CharField()
    AUTH_USER_MODEL = serializers.CharField()
    DATA_UPLOAD_MAX_MEMORY_SIZE = serializers.IntegerField() 