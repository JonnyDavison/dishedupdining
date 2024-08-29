from django_summernote.admin import SummernoteModelAdmin
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from .models import Home, Gallery, Review, Feature, FeatureItem

# Custom LogEntry class and admin
class CustomLogEntry(admin.ModelAdmin):
    list_display = ['user', 'content_type', 'object_repr', 'action_flag', 'change_message']
    readonly_fields = ['user', 'content_type', 'object_id', 'object_repr', 'action_flag', 'change_message']
    search_fields = ['user__username', 'object_repr', 'change_message']
    list_filter = ['action_flag', 'content_type']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

# Only register CustomLogEntry if LogEntry is not already registered
if not admin.site.is_registered(LogEntry):
    admin.site.register(LogEntry, CustomLogEntry)

@admin.register(Home)
class HomeAdmin(SummernoteModelAdmin):
    list_display = ('created_on', 'is_active')
    actions = ['make_active']
    summernote_fields = ('main_title', 'sub_title', 'call_to_action',)
    
    def make_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected record is now active")

    make_active.short_description = "Mark selected record as active"


class FeatureItemInline(admin.TabularInline):
    model = FeatureItem
    extra = 1

@admin.register(Feature)
class FeatureAdmin(SummernoteModelAdmin):
    list_display = ('feature_title', 'is_active')
    actions = ['make_active']
    summernote_fields = ('feature_title', 'feature_sub_title')
    inlines = [FeatureItemInline]
    
    def make_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected feature is now active")

    make_active.short_description = "Mark selected feature as active"


@admin.register(Gallery)
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

@admin.register(Review)
class ReviewAdmin(SummernoteModelAdmin):
    """ Organise the Review admin panel """
    list_display = (
        'name',
        'rating',
        'created_at',
        'image',
    )
    ordering = ('name',)
    summernote_fields = ('comment',)
    
