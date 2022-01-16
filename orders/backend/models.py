from asyncio.windows_events import NULL

import re

# from unicodedata import category
from django.conf import settings
from django.core import validators
from datetime import datetime, timedelta
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser 
from django.contrib.auth.validators import UnicodeUsernameValidator

from django.utils.translation import gettext_lazy as _ 
from django_rest_passwordreset.tokens import get_token_generator
import jwt

from datetime import datetime, timedelta

from rest_framework.authtoken.models import Token

USER_TYPE_CHOICES = (
    ('shop', 'Магазин'),
    ('buyer', 'Покупатель'),
)

ORDER_STATUS_CHOICES = (
    ('not paid', 'Не оплачен'),
    ('new', 'Новый'),
    ('confirmed', 'Подтвержден'),
    ('assembled', 'Собран'),
    ('sent', 'Отправлен'),
    ('delivered', 'Доставлен'),
    ('canceled', 'Отменен'),
)

# CONTACT_TYPE_CHOICES = (
#     ('adress', 'Адрес'),
#     ('phone', 'Телефон'),
# )

# tpl = '/^[A-Z0-9._%+-]+@[A-Z0-9-]+.+.[A-Z]{2,4}$/i'
# if re.match(tpl, work_email) is not None:
#     pass


class UserManager(BaseUserManager):
    """
    Миксин для управления пользователями
    """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Стандартная модель пользователей
    """
    REQUIRED_FIELDS = []
    objects = UserManager()
    USERNAME_FIELD = 'email'
    email = models.EmailField(_('email address'), unique=True)
    company = models.CharField(verbose_name='Компания', max_length=40, blank=True)
    position = models.CharField(verbose_name='Должность', max_length=40, blank=True)
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
        "unique" : _("A user with that username already exists."),
        },
    )
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        )
    )
    type = models.CharField(verbose_name='Группа пользователя', choices=USER_TYPE_CHOICES, max_length=5, default='buyer')


    def __str__(self):
        """Возвращает строковое представление этого `User`."""
        return self.email


    @property
    def token(self):
        """Позволяет нам получить токен пользователя, 
        вызвав `user.token` вместо `user.generate_jwt_token()."""
        return self._generate_jwt_token()


    """
    Следующие 2 метода требуется Django для таких вещей,
    как обработка электронной почты.
    Обычно это имя и фамилия пользователя.
    Поскольку мы не храним настоящее имя пользователя,
    мы возвращаем его имя пользователя.
    """
    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username


    def _generate_jwt_token(self):
        """
        Создает веб-токен JSON, в котором хранится идентификатор
        этого пользователя и срок его действия
        составляет 60 дней в будущем.
        """
        date = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            # 'exp': dt.strftime('%s')
            'exp': date.utcfromtimestamp(date.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

    class Meta:

        verbose_name = 'Пользователь'
        verbose_name_plural = "Список пользователей"
        ordering = ('email',)


class Shop(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30, blank=True)
    work_email = models.CharField(max_length=30, blank=True)
       
    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Список магазинов'     
        
    def __str__(self):
        return self.name 
       

class Parameter(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40, blank=True)
       
    class Meta:
        verbose_name = 'Название параметра'
        verbose_name_plural = 'Список названий параметров'   
        
    def __str__(self):
        return self.name     
       

class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30, blank=True)
       
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Список товаров'   
        
    def __str__(self):
        return self.name  


class ProductParameter(models.Model):
    product_id = ForeignKey(Product, related_name='product_id', on_delete=models.CASCADE, blank=True)
    parameter_id = ForeignKey(Parameter, related_name='parameter_id', on_delete=models.CASCADE, blank=True)    
    value = models.CharField(max_length=30, blank=True)

    class Meta:
        unique_together = ('product_id', 'parameter_id'),
        verbose_name = 'Параметр',
        verbose_name_plural = 'Список параметров'
        

class Catalog(models.Model):
    category = models.CharField(max_length=20, blank=True)
    product_id = ForeignKey(Product, on_delete=models.CASCADE, blank=True)
    shop_id = ForeignKey(Shop, on_delete=models.CASCADE, blank=True)
    price = models.CharField(max_length=10, blank=True)
    qty = models.PositiveIntegerField(blank=True)
    on_sale = models.BooleanField(blank=True)
    foreign_together = ForeignKey('Orderlist', related_name='foreign_together', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('product_id', 'shop_id')  
        verbose_name = 'Список товаров'
        verbose_name_plural = 'Каталог товаров'   
        

class Orderlist(models.Model):
    order_id = ForeignKey('Order', related_name='order_id', on_delete=models.CASCADE, blank=True)
    product_id = ForeignKey(Product, on_delete=models.CASCADE, blank=True)
    shop_id = ForeignKey(Shop, on_delete=models.CASCADE, blank=True)
    current_price = models.PositiveIntegerField(blank=True)
    qty = models.PositiveIntegerField(blank=True)
    coast = models.PositiveIntegerField(blank=True)

    class Meta:
        unique_together = ('product_id', 'shop_id')
        # , primary_key=True
        verbose_name = 'Заказанный товар'
        verbose_name_plural = 'Заказанные товары'

    @property
    def calculate_coast(self):
        self.coast = self.current_price * self.qty
        return self.coast


class Order(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = ForeignKey('User', related_name='user_id', on_delete=models.CASCADE, blank=True)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(verbose_name='Статус', choices=ORDER_STATUS_CHOICES, max_length=15)
    total_cost = models.PositiveIntegerField(blank=True)

    @property
    def calculate_total_coast(self):
        order_items = Orderlist.objects.filter(Orderlist.order_id == self.id).all()
        for item in order_items:
            self.total_coast += item.calculate_coast
        return self.total_coast

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Список заказов' 
        ordering = ('-date',)

    def __str__(self):
        return str(self.date)

    

class Contact(models.Model):
    user_id = ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(verbose_name='ФИО', max_length=60)
    phone_number = models.CharField(verbose_name='Телефон', max_length=20)
    address = models.CharField(verbose_name='Адрес', max_length=150)
    class Meta:
        verbose_name = 'Контакты заказчика'
        verbose_name_plural = 'Список контактов'


class ConfirmEmailToken(models.Model):
    class Meta:
        verbose_name = 'Токен подтверждения Email'
        verbose_name_plural = 'Токены подтверждения Email'

    @staticmethod
    def generate_key():
        """ generates a pseudo random code using os.urandom and binascii.hexlify """
        return get_token_generator().generate_token()

    user = models.ForeignKey(
        User,
        related_name = 'confirm_email_tokens',
        on_delete = models.CASCADE,
        verbose_name =_("The User which is associated to this password reset token")
        )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("When was this token generated")
        )

    # Key field, though it is not the primary key of the model
    key = models.CharField(
        _("Key"),
        max_length=64,
        db_index=True,
        unique=True
    )

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(ConfirmEmailToken, self).save(*args, **kwargs)

    def __str__(self):
        return "Password reset token for user {user}".format(user=self.user)
