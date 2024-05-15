from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.


# Модель категорий
class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Названия категории')
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name='Картинка')
    slug = models.SlugField(unique=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True,
                               related_name='subcategories', verbose_name='Категория')

    # Умная ссылка
    def get_absolute_url(self):
        return reverse('category_page', kwargs={'slug': self.slug})

    # Получения картинки
    def get_image_category(self):
        if self.image:
            return self.image.url
        else:
            return '-'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


# Модель бренда
class Brand(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название брэнда')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='brand', verbose_name='Категория',
                                 blank=True, null=True)

    def __str__(self):
        return f'{self.title}: {self.category}'

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'


# Модель товара
class Product(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название товара')
    description = models.TextField(blank=True, null=True, verbose_name='Описание к товару')
    price = models.FloatField(verbose_name='Цена товара')
    quantity = models.IntegerField(verbose_name='На складе')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    production = models.CharField(max_length=70, verbose_name='Страна производства')
    slug = models.SlugField(unique=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products',
                                 verbose_name='Категория')
    taste = models.CharField(max_length=100, blank=True, null=True, verbose_name='Вкус')
    brand = models.ForeignKey(Brand, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Бренд')
    model_product = models.CharField(max_length=50, blank=True, null=True, verbose_name='Модель')

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    # Получения картинки
    def get_image_product(self):
        if self.images:
            try:
                return self.images.first().image.url
            except:
                return '-'
        else:
            return '-'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


# Модель галлереи
class Gallery(models.Model):
    image = models.ImageField(upload_to='products/', verbose_name='Картинка товара')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='Товар')

    class Meta:
        verbose_name = 'Картинка товара'
        verbose_name_plural = 'Картинки товара'


# ----------------------------------------------------------------------------------------------------------------------

# Модель слайдера "постер"
class Slider(models.Model):
    title = models.CharField(max_length=400, verbose_name='Краткоео описание к слайдеру')
    description = models.CharField(max_length=400, verbose_name='Под описание')
    image = models.ImageField(upload_to='images_slider/', verbose_name='Картинка для слайдера', blank=True, null=True)

    def get_image_product(self):
        if self.image:
            try:
                return self.image.url
            except:
                return '-'
        else:
            return '-'

    class Meta:
        verbose_name = 'Слайдер'
        verbose_name_plural = 'Слайдер'


# ----------------------------------------------------------------------------------------------------------------------

# Избранное
class FavoriteProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользолватель')

    def __str__(self):
        return f'Товар: {self.product} пользователя: {self.user.username}'

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные товары'


# ----------------------------------------------------------------------------------------------------------------------

# Корзина
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
    first_name = models.CharField(max_length=200, default='', verbose_name='Имя покупателя')
    last_name = models.CharField(max_length=200, default='', verbose_name='Фамилия покупателя')
    email = models.EmailField(verbose_name='Почта покупателя', blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


# Заказ
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    is_completed = models.BooleanField(default=False, verbose_name='Выполнен ли заказ')
    shipping = models.BooleanField(default=True, verbose_name='Доставка')

    def __str__(self):
        return f'Заказ №: {self.pk}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    # метода подсчета суммы заказа
    @property
    def get_cart_total_price(self):
        order_products = self.orderproduct_set.all()
        total_price = sum([product.get_total_price for product in order_products])
        return total_price

    @property
    def get_cart_total_quantity(self):
        order_products = self.orderproduct_set.all()
        total_quantity = sum([product.quantity for product in order_products])
        return total_quantity


# Заказанные товары
class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, verbose_name='Номер заказа')
    quantity = models.IntegerField(default=0, blank=True, null=True, verbose_name='Количество')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления в корзину')

    def __str__(self):
        return f'Продукт {self.product.title} {self.order}'

    class Meta:
        verbose_name = 'Заказанный товар'
        verbose_name_plural = 'Заказанные товары'

    # Получение стоимости количества товара
    @property
    def get_total_price(self):
        total_price = self.product.price * self.quantity
        return total_price


# Доставка
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, verbose_name='Покупатель')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, verbose_name='Заказ')
    address = models.CharField(max_length=200, verbose_name='Адрес улица/дом/квартира')
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город доставки')
    region = models.CharField(max_length=200, verbose_name='Регион/Область')
    phone = models.CharField(max_length=100, verbose_name='Номер телефона')
    comment = models.CharField(max_length=300, verbose_name='Комментарий к заказу')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата доставки')

    def __str__(self):
        return f'Получатель {self.customer} по адресу: {self.address}'

    class Meta:
        verbose_name = 'Адрес доставки'
        verbose_name_plural = 'Адреса доставок'


# Город
class City(models.Model):
    city_name = models.CharField(max_length=100, verbose_name='Название города')

    def __str__(self):
        return self.city_name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


# Профиль
# Профиль
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    first_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Имя')
    last_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Фамилия')
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Город')
    street = models.CharField(max_length=100, blank=True, null=True, verbose_name='Улица')
    house = models.CharField(max_length=100, blank=True, null=True, verbose_name='Дом/Корпус')
    flat = models.CharField(max_length=100, blank=True, null=True, verbose_name='Квартира')
    email = models.EmailField(blank=True, null=True, verbose_name='Почта')
    phone = models.CharField(max_length=50, blank=True, null=True, verbose_name='Номер телефона')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профиля'









