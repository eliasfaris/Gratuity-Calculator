from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password = None, ismanager=None):
        """
        Creates and saves a User with the given email and password
        """
        if not email:
            raise ValueError('Users must have email address')
        user = self.model(email = self.normalize_email(email))
        user.set_password(password)
        user.set_manager(ismanager)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.admin = True
        user.staff = True
        user.manager = False
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique= True, verbose_name = 'email address', null = False, blank = False)
    manager = models.BooleanField(default=False, null=True)

    def set_manager(self, ismanager):
        self.manager = ismanager
    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return True

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return True


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= []

    objects = UserManager()