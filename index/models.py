from django.db import models


class Home(models.Model):
    """ Homepage Hero Section Model """

    class Meta:
        verbose_name_plural = 'Home'

    logo = models.ImageField(null=True, blank=True)
    main_title = models.TextField()
    sub_title = models.TextField()
    call_to_action = models.TextField()
    hero_image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.main_title


class Gallery(models.Model):
    """ Gallery model """

    class Meta:
        verbose_name_plural = 'Gallery'

    name = models.CharField(max_length=254)
    description = models.TextField()
    image1 = models.ImageField(null=True, blank=True)
    image2 = models.ImageField(null=True, blank=True)
    image3 = models.ImageField(null=True, blank=True)
    image4 = models.ImageField(null=True, blank=True)
    image5 = models.ImageField(null=True, blank=True)
    image6 = models.ImageField(null=True, blank=True)
    image7 = models.ImageField(null=True, blank=True)
    image8 = models.ImageField(null=True, blank=True)
    image9 = models.ImageField(null=True, blank=True)
    image10 = models.ImageField(null=True, blank=True)

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

    def __str__(self):
        return self.name
