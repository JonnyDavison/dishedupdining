from django.db import models


class Home(models.Model):
    """ Homepage Model """
    main_title = models.TextField()
    sub_title = models.TextField()
    call_to_action = models.TextField()

    def __str__(self):
        return self.main_title


class Gallery(models.Model):
    """ Gallery model """
    name = models.CharField(max_length=254)
    description = models.TextField()
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    """ Review Model"""
    name = models.CharField(max_length=254)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
