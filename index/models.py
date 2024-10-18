from django.db import models
from django_summernote.fields import SummernoteTextField


class Home(models.Model):
    """ Homepage Hero Section Model """

    class Meta:
        verbose_name_plural = 'Home'
        
    created_on = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    logo = models.ImageField(null=True, blank=True)
    main_title = models.TextField(null=True, blank=True)
    sub_title = models.TextField(null=True, blank=True)
    call_to_action = models.TextField(null=True, blank=True)
    hero_image = models.ImageField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.main_title

    def save(self, *args, **kwargs):
        if self.is_active:
            # Set all other instances to inactive
            Home.objects.filter(is_active=True).update(is_active=False)
        super(Home, self).save(*args, **kwargs)

 
class Feature(models.Model):
    feature_image = models.ImageField(null=True, blank=True)
    feature_title = models.TextField()
    feature_sub_title = models.TextField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.feature_title

    def save(self, *args, **kwargs):
        if self.is_active:
            Feature.objects.filter(is_active=True).update(is_active=False)
        super(Feature, self).save(*args, **kwargs)
        
        
class FeatureItem(models.Model):
    feature = models.ForeignKey(Feature, related_name='items', on_delete=models.CASCADE)
    icon = models.CharField(max_length=50)  # max_length to accommodate Font Awesome classes
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title


class Gallery(models.Model):
    """ Gallery model """

    class Meta:
        verbose_name_plural = 'Gallery'

    name = models.CharField(max_length=254)
    description = models.TextField()
    is_active = models.BooleanField(default=False)
    gallery_image1 = models.ImageField(null=True, blank=True)
    gallery_image2 = models.ImageField(null=True, blank=True)
    gallery_image3 = models.ImageField(null=True, blank=True)
    gallery_image4 = models.ImageField(null=True, blank=True)
    gallery_image5 = models.ImageField(null=True, blank=True)
    gallery_image6 = models.ImageField(null=True, blank=True)
    gallery_image7 = models.ImageField(null=True, blank=True)
    gallery_image8 = models.ImageField(null=True, blank=True)
    gallery_image9 = models.ImageField(null=True, blank=True)
    gallery_image10 = models.ImageField(null=True, blank=True)
    gallery_image11 = models.ImageField(null=True, blank=True)
    gallery_image12 = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    """ Review Model"""

    class Meta:
        verbose_name_plural = 'Reviews'

    name = models.CharField(max_length=254)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Review by {self.author}"


class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.subject}"
    

class About(models.Model):
    title = models.CharField(max_length=200)
    sub_title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='about/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "About"


class Service(models.Model):
    name = models.CharField(max_length=200)
    sub_title = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Services'