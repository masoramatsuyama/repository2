from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin,UserManager
from django.contrib.auth.base_user import AbstractBaseUser,BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.validators import UnicodeUsernameValidator

# Create your models here.


class Artist(models.Model):
    artistname = models.CharField(max_length=20)
    fromm = models.CharField(max_length=128)
    artistimage = models.FileField(upload_to='media')
    video = models.FileField(upload_to='media', null=True, blank=True)
    def __str__(self):
     return self.artistname


class Art(models.Model):
    artist = models.ForeignKey('Artist',on_delete=models.CASCADE)
    artname = models.CharField(max_length=128)
    artbirth = models.DateField()
    artimage = models.ImageField(upload_to='media')
    def __str__(self):
     return self.artname

class Return(models.Model):
    artist = models.ForeignKey('Artist',on_delete=models.CASCADE)
    lank = models.ForeignKey('Price',on_delete=models.CASCADE)
    returnname = models.CharField(max_length=20)
    returnimage = models.ImageField(upload_to='media')
    returnex = models.CharField(max_length=100)
    def __str__(self):
     return self.returnname

class Price(models.Model):
    lank = models.CharField(max_length=20)
    price = models.PositiveIntegerField(verbose_name='価格')
    def __str__(self):
     return self.lank

   
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

"""お気に入り機能追加済みユーザー"""
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True)

    favorite_place = models.ManyToManyField(Art, blank=True)
    favorite_people = models.ManyToManyField(Artist, blank=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

class Order(models.Model):
    # customer = models.ForeignKey(User, on_delete=models.SET_NULL,  null=True)
    product = models.ForeignKey(Return, on_delete=models.SET_NULL, null=True)
    price = models.PositiveIntegerField(verbose_name='価格')
    timestamp = models.DateTimeField(verbose_name='発注日', auto_now_add=True)
    stripe = models.CharField(verbose_name='Stripe Session', max_length=100)