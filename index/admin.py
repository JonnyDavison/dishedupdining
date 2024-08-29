from django_summernote.admin import SummernoteModelAdmin
from django.contrib import admin
from .models import Home, Gallery, Review


@admin.register(Home)
class HomeAdmin(SummernoteModelAdmin):
    list_display = ('main_title', 'is_active')
    actions = ['make_active']
    summernote_fields = '__all__'
    
    def make_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected record is now active")

    make_active.short_description = "Mark selected record as active"


class GalleryAdmin(SummernoteModelAdmin):
    """ Organise the Gallery admin panel """
    list_display = (
        'name',
        'description',
        'gallery_image1',
        'gallery_image2',
        'gallery_image3',
        'gallery_image4',
        'gallery_image5',
        'gallery_image6',
        'gallery_image7',
        'gallery_image8',
        'gallery_image9',
        'gallery_image10',
        'gallery_image11',
        'gallery_image12',
    )
    ordering = ('name',)
    summernote_fields = ('description',)



class ReviewAdmin(SummernoteModelAdmin):
    """ Organise the Gallery admin panel """
    list_display = (
        'name',
        'rating',
        'created_at',
        'image',
    )
    ordering = ('name',)
    summernote_fields = ('comment',)


# admin.site.register(Home, HomeAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Review, ReviewAdmin)
