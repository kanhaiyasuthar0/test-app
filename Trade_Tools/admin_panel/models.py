from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/' ,default="")
    zipfile = models.FileField(upload_to='zipfiles/')

    def __str__(self):
        return self.title


class VisitorCount(models.Model):
    count = models.IntegerField(default=0)
