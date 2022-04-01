from django.contrib import admin
from  .models import Category, Product, Gallery
# Register your models here.
from django.utils.safestring import mark_safe


class GalleryInline(admin.TabularInline):
    fk_name = 'product'
    model = Gallery
    extra = 1



class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'category', 'quantity', 'price', 'created_at', 'get_photo', 'get_photo_count')
    list_editable = ('price', 'quantity')
    list_display_links = ('title', )
    inlines = [GalleryInline]
    list_filter = ('title', 'price')

    def get_photo(self, obj):
        if obj.images:
            return mark_safe(f'<img src="{obj.images.all()[0].image.url}" width="75">')
        else:
            return '-'
    get_photo.short_description = 'Главное фото'

    def get_photo_count(self, obj):
        if obj.images:
            return str(len(obj.images.all()))
        else:
            return '0'
    get_photo_count.short_description = 'Количество изображений'






admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
