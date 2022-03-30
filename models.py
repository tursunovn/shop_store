from django.db import models

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_lenght=50, verbose_name = 'Категория')

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'Category(pk={self.pk}, title{self.title})'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категрии'
        ordering = ['title']


class Product(models.Model):
    title = models.CharField(max_lenght=255, verbose_name='Наименование продукта')
    price = models.FloatField(verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    quantity = models.IntegerField(default=0, verbose_name='Кодичество на складе')
    description = models.TextField(default='Здесь будет описание', verbose_name='Описание')
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 verbose_name='Категория',
                                 related_name='products')

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
    side = models.CharField(max_lengh=255, default='Фронтальная', verbose_name='Описание картинки')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Галерея товаров'

