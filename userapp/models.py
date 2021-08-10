from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount


class AccountManager(BaseUserManager):

    # create new user
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError('Users must have a username.')
        if not email:
            raise ValueError('Users must have an email address.')
        
        user = self.create(
            email = self.normalize_email(email),
            username = username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # create new superuser
    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username, 
            email=email, 
            password=password
        )

        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


def profile_image_path(self, fiename):
    return f'profile_images/{self.pk}/{"profile_image.png"}'


class Account(AbstractBaseUser):

    first_name                   = models.CharField(max_length=50, blank=True, null=True)
    last_name                    = models.CharField(max_length=50, blank=True, null=True)
    email                        = models.EmailField(unique=True, primary_key=False)
    profile_image                = models.ImageField(upload_to=profile_image_path, null=True, blank=True)
    profile_image_link           = models.URLField(null=True, blank=True)
    username                     = models.CharField(max_length=10, unique=True, primary_key=True)
    date_joined                  = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login                   = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin                     = models.BooleanField(default=False)
    is_active                    = models.BooleanField(default=True)
    is_staff                     = models.BooleanField(default=False)
    is_customer                  = models.BooleanField(default=False)
    is_authority                 = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    def get_username(self):
        return self.username
    
    @property
    def admin(self):
        return self.is_admin
    
    @property
    def staff(self):
        return self.is_staff

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
        ordering = ['-date_joined',]

@receiver(post_save, sender=Account)
def save_profile_image(sender, instance, **kwargs):
    user = None
    try:
        user = SocialAccount.objects.get(user=instance)
    except:
        pass
    if user is not None:
        instance.profile_image_link = user.extra_data['picture']
        instance.is_customer = True
        instance.save()


