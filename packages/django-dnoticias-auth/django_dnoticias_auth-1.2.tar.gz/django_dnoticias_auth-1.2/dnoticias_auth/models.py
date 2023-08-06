import requests
import logging
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

logger = logging.getLogger(__name__)

# Create your models here.
class User(AbstractUser):

    @staticmethod
    def get_context(email):
        context = {}
        try:
            response = requests.get(settings.USER_CONTEXT_URL, params={ "email" : email }, timeout=settings.USER_CONTEXT_TIMEOUT)
            response.raise_for_status()
            return response.json()
        except Exception:
            logger.exception("Occured an error getting the context of the user")
        
        return context

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = {}

    def __str__(self):
        return self.email
