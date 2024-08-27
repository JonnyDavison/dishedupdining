from django.contrib import admin
from .models import Home, Gallery, Review


class HomeAdmin(admin.ModelAdmin):
    """ Organise the Home page admin panel """
    list_display = (
        'logo',
        'main_title',
        'sub_title',
        'call_to_action',
        'hero_image',
    )

    ordering = ('main_title',)

class GalleryAdmin(admin.ModelAdmin):
    """ Organise the Gallery admin panel """
    list_display = (
        'name',
        'description',
        'image1',
        'image2',
        'image3',
        'image4',
        'image5',
        'image6',
        'image7',
        'image8',
        'image9',
        'image10',
    )
    ordering = ('name',)


class ReviewAdmin(admin.ModelAdmin):
    """ Organise the Gallery admin panel """
    list_display = (
        'name',
        'rating',
        'created_at',
        'image',
    )
    ordering = ('name',)


admin.site.register(Home, HomeAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Review, ReviewAdmin)
