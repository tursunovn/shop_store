from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name='Категория')
    image = models.ImageField(upload_to='categories/', null=True, blank=True, verbose_name='Изображение')
    slug = models.SlugField(unique=True, null=True)

    def get_absolute_url(self):
        return(reverse('product_list_by_category', kwargs={'slug':self.slug}))


    def __str__(self):
        return self.title

    def __repr__(self):
        return f'Category(pk={self.pk}, title{self.title})'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='Наименование продукта')
    price = models.FloatField(verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    quantity = models.IntegerField(default=0, verbose_name='Количество на складе')
    description = models.TextField(default='Здесь будет описание', verbose_name='Описание')
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 verbose_name='Категория',
                                 related_name='products')
    slug = models.SlugField(unique=True, null=True)
    size = models.IntegerField(default=30, verbose_name='Размеры в мм')
    colour = models.CharField(max_length=30, default='Сталь', verbose_name='Цвет')

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def get_first_photo(self):
        if self.images:
            try:
                return self.images.all()[0].image.url
            except:
                return 'https://экологиякрыма.рф/img/19893719.jpg'
        else:
            return 'https://экологиякрыма.рф/img/19893719.jpg'

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'Product(pk={self.pk}, title={self.title})'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at', 'category']


class Gallery(models.Model):
    image = models.ImageField(upload_to='product/', verbose_name='Изображение')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    side = models.CharField(max_length=255, default='Фронтальная', verbose_name='Описание картинки')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Галерея товаров'

class Colours(models.Model):
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE, related_name='colours')
    colour = models.CharField(max_length=100, verbose_name='Название цвета')

    def __str__(self):
        return self.colour

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Варианты цветов'

class Sizes(models.Model):
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE, related_name='sizes')
    size = models.IntegerField(verbose_name='Размер в мм', default=0)

    def __str__(self):
        return str(self.size)

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Варианты размеров'


class Review(models.Model):
    text = models.TextField(verbose_name='Текст комметария')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,verbose_name='Товар')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Mail(models.Model):
    mail = models.EmailField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.mail