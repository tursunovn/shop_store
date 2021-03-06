from django.contrib import admin
from .models import Category, Product, Gallery, Sizes, Colours, Review
# Register your models here.
from django.utils.safestring import mark_safe


class GalleryInline(admin.TabularInline):
    fk_name = 'product'
    model = Gallery
    extra = 1

class ColoursInline(admin.TabularInline):
    fk_name = 'product'
    model = Gallery
    extra = 1

class SizesInline(admin.TabularInline):
    fk_name = 'product'
    model = Colours
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title',
                    'category', 'quantity',
                    'price', 'created_at',
                    'get_photo', 'get_photo_count',
                    'size', 'colour')
    list_editable = ('price', 'quantity', 'size', 'colour')
    list_display_links = ('title',)
    inlines = [GalleryInline, ColoursInline, SizesInline]
    list_filter = ('title', 'price')
    prepopulated_fields = {'slug': ('title',)}

    def get_photo(self, obj):
        if obj.images:
            try:
                return mark_safe(f'<img src="{obj.images.all()[0].image.url}" width="75">')
            except:
                return '-'
        else:
            return '-'

    get_photo.short_description = 'Главное фото'

    def get_photo_count(self, obj):
        if obj.images:
            return str(len(obj.images.all()))
        else:
            return '0'

    get_photo_count.short_description = 'Количество изображений'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_products_count')
    prepopulated_fields = {'slug': ('title',)}


    def get_products_count(self, obj):
        if obj.products:
            return str(len(obj.products.all()))
        else:
            return '0'

    get_products_count.short_description = 'Количество товаров'

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'text', 'created_at')
    list_display_links = ('pk',)
    readonly_fields = ('author', 'product', 'text', 'created_at')



admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
