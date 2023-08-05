from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


# Create your models here.
class OauthUser(AbstractBaseUser, PermissionsMixin):
	identifier = models.CharField(max_length=40, unique=True)
	
	email = None
	is_staff = None
	is_active = None
	is_superuser = None
	is_anonymous = True
	
	USERNAME_FIELD = 'identifier'

	def __str__(self):
		return self.identifier
