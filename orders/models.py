from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_rest_passwordreset.tokens import get_token_generator

STATE_CHOICES = (
    ('basket', 'Статус корзины'),
    ('new', 'Новый'),
    ('confirmed', 'Подтвержден'),
    ('assembled', 'Собран'),
    ('sent', 'Отправлен'),
    ('delivered', 'Доставлен'),
    ('canceled', 'Отменен'),
)

class Category(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = "Список категорий"
        ordering = ('-name',)

    def __str__(self):
        return self.name

class Parameter(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название')
    descriptions = models.CharField(max_length=40, verbose_name='Описание')

    class Meta:
        verbose_name = 'Имя параметра'
        verbose_name_plural = "Список имен параметров"
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Product(models.Model):
    model = models.CharField(max_length=80, verbose_name='Модель', blank=True)
    external_id = models.PositiveIntegerField(verbose_name='Внешний ИД')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price = models.PositiveIntegerField(verbose_name='Цена')
    price_rrc = models.PositiveIntegerField(verbose_name='Рекомендуемая розничная цена')
    category_id= models.ForeignKey(Category, verbose_name='Категория', related_name='category_info', blank=True,
                                on_delete=models.CASCADE)
    parametr_id = models.ForeignKey(Parameter, verbose_name='Параметр', related_name='parametr_info', blank=True,
                                on_delete=models.CASCADE)

    provider_id = models.ForeignKey(User, verbose_name='Поставщик', related_name='provider_info', blank=True,
                                on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Информация о продукте'
        verbose_name_plural = "Информационный список о продуктах"

    def __str__(self):
        return self.name



class Contact(models.Model):
    user = models.ForeignKey(User, related_name='user_info', on_delete=models.CASCADE)
    organization = models.CharField(max_length=100, verbose_name='Название организации пользователя')
    city = models.CharField(max_length=50, verbose_name='Город', null=True, default=None)
    street = models.CharField(max_length=100, verbose_name='Улица', null=True, default=None)
    house = models.CharField(max_length=15, verbose_name='Дом', null=True, default=None)
    structure = models.CharField(max_length=15, verbose_name='Корпус', null=True, default=None)
    apartment = models.CharField(max_length=15, verbose_name='Квартира', null=True, default=None)
    phone = models.CharField(max_length=20, verbose_name='Телефон', null=True, default=None)
    provider = models.BooleanField(verbose_name='Поставщик', default=True)


    class Meta:
        verbose_name = 'Контакты представителя организации'
        verbose_name_plural = "Список контактов представителей огранизаций"

    def __str__(self):
        return f'{self.organization} {self.city} {self.street} {self.house}'


class Shop(models.Model):
    name = models.ForeignKey(Contact, verbose_name='Название магазина',
                             related_name='contact_info', blank=True,
                             on_delete=models.CASCADE)
    state = models.BooleanField(verbose_name='статус получения заказов', default=True)

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = "Список магазинов"
        ordering = ('-name',)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь',
                             related_name='orders', blank=True,
                             on_delete=models.CASCADE)
    dt = models.DateTimeField(auto_now_add=True)
    state = models.CharField(verbose_name='Статус', choices=STATE_CHOICES, max_length=15)


    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = "Список заказ"
        ordering = ('-dt',)

    def __str__(self):
        return str(self.dt)



class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ', related_name='ordered_items', blank=True,
                              on_delete=models.CASCADE)

    product_info = models.ForeignKey(Product, verbose_name='Информация о продукте', related_name='ordered_items',
                                     blank=True,
                                     on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Заказанная позиция'
        verbose_name_plural = "Список заказанных позиций"



# STATE_CHOICES = (
#     ('basket', 'Статус корзины'),
#     ('new', 'Новый'),
#     ('confirmed', 'Подтвержден'),
#     ('assembled', 'Собран'),
#     ('sent', 'Отправлен'),
#     ('delivered', 'Доставлен'),
#     ('canceled', 'Отменен'),
# )
#
# USER_TYPE_CHOICES = (
#     ('shop', 'Магазин'),
#     ('buyer', 'Покупатель'),
#
# )
#
#
#
# class Shop(models.Model):
#     name = models.CharField(max_length=50, verbose_name='Название')
#     url = models.URLField(verbose_name='Ссылка', null=True, blank=True)
#     user = models.OneToOneField(User, verbose_name='Пользователь',
#                                 blank=True, null=True,
#                                 on_delete=models.CASCADE)
#     state = models.BooleanField(verbose_name='статус получения заказов', default=True)
#
#     class Meta:
#         verbose_name = 'Магазин'
#         verbose_name_plural = "Список магазинов"
#         ordering = ('-name',)
#
#     def __str__(self):
#         return self.name
#
#
# class Category(models.Model):
#     name = models.CharField(max_length=40, verbose_name='Название')
#     shops = models.ManyToManyField(Shop, verbose_name='Магазины', related_name='categories', blank=True)
#
#     class Meta:
#         verbose_name = 'Категория'
#         verbose_name_plural = "Список категорий"
#         ordering = ('-name',)
#
#     def __str__(self):
#         return self.name
#
#
# class Product(models.Model):
#     name = models.CharField(max_length=80, verbose_name='Название')
#     category = models.ForeignKey(Category, verbose_name='Категория', related_name='products', blank=True,
#                                  on_delete=models.CASCADE)
#
#     class Meta:
#         verbose_name = 'Продукт'
#         verbose_name_plural = "Список продуктов"
#         ordering = ('-name',)
#
#     def __str__(self):
#         return self.name
#
#
# class ProductInfo(models.Model):
#     model = models.CharField(max_length=80, verbose_name='Модель', blank=True)
#     external_id = models.PositiveIntegerField(verbose_name='Внешний ИД')
#     product = models.ForeignKey(Product, verbose_name='Продукт', related_name='product_infos', blank=True,
#                                 on_delete=models.CASCADE)
#     shop = models.ForeignKey(Shop, verbose_name='Магазин', related_name='product_infos', blank=True,
#                              on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(verbose_name='Количество')
#     price = models.PositiveIntegerField(verbose_name='Цена')
#     price_rrc = models.PositiveIntegerField(verbose_name='Рекомендуемая розничная цена')
#
#     class Meta:
#         verbose_name = 'Информация о продукте'
#         verbose_name_plural = "Информационный список о продуктах"
#         constraints = [
#             models.UniqueConstraint(fields=['product', 'shop', 'external_id'], name='unique_product_info'),
#         ]
#
#
# class Parameter(models.Model):
#     name = models.CharField(max_length=40, verbose_name='Название')
#
#     class Meta:
#         verbose_name = 'Имя параметра'
#         verbose_name_plural = "Список имен параметров"
#         ordering = ('-name',)
#
#     def __str__(self):
#         return self.name
#
#
# class ProductParameter(models.Model):
#     product_info = models.ForeignKey(ProductInfo, verbose_name='Информация о продукте',
#                                      related_name='product_parameters', blank=True,
#                                      on_delete=models.CASCADE)
#     parameter = models.ForeignKey(Parameter, verbose_name='Параметр', related_name='product_parameters', blank=True,
#                                   on_delete=models.CASCADE)
#     value = models.CharField(verbose_name='Значение', max_length=100)
#
#     class Meta:
#         verbose_name = 'Параметр'
#         verbose_name_plural = "Список параметров"
#         constraints = [
#             models.UniqueConstraint(fields=['product_info', 'parameter'], name='unique_product_parameter'),
#         ]
#
#
# class Contact(models.Model):
#     user = models.ForeignKey(User, verbose_name='Пользователь',
#                              related_name='contacts', blank=True,
#                              on_delete=models.CASCADE)
#
#     city = models.CharField(max_length=50, verbose_name='Город')
#     street = models.CharField(max_length=100, verbose_name='Улица')
#     house = models.CharField(max_length=15, verbose_name='Дом', blank=True)
#     structure = models.CharField(max_length=15, verbose_name='Корпус', blank=True)
#     building = models.CharField(max_length=15, verbose_name='Строение', blank=True)
#     apartment = models.CharField(max_length=15, verbose_name='Квартира', blank=True)
#     phone = models.CharField(max_length=20, verbose_name='Телефон')
#
#     class Meta:
#         verbose_name = 'Контакты пользователя'
#         verbose_name_plural = "Список контактов пользователя"
#
#     def __str__(self):
#         return f'{self.city} {self.street} {self.house}'
#
#
# class Order(models.Model):
#     user = models.ForeignKey(User, verbose_name='Пользователь',
#                              related_name='orders', blank=True,
#                              on_delete=models.CASCADE)
#     dt = models.DateTimeField(auto_now_add=True)
#     state = models.CharField(verbose_name='Статус', choices=STATE_CHOICES, max_length=15)
#     contact = models.ForeignKey(Contact, verbose_name='Контакт',
#                                 blank=True, null=True,
#                                 on_delete=models.CASCADE)
#
#     class Meta:
#         verbose_name = 'Заказ'
#         verbose_name_plural = "Список заказ"
#         ordering = ('-dt',)
#
#     def __str__(self):
#         return str(self.dt)
#
#     # @property
#     # def sum(self):
#     #     return self.ordered_items.aggregate(total=Sum("quantity"))["total"]
#
#
# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, verbose_name='Заказ', related_name='ordered_items', blank=True,
#                               on_delete=models.CASCADE)
#
#     product_info = models.ForeignKey(ProductInfo, verbose_name='Информация о продукте', related_name='ordered_items',
#                                      blank=True,
#                                      on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(verbose_name='Количество')
#
#     class Meta:
#         verbose_name = 'Заказанная позиция'
#         verbose_name_plural = "Список заказанных позиций"
#         constraints = [
#             models.UniqueConstraint(fields=['order_id', 'product_info'], name='unique_order_item'),
#         ]
#