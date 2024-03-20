from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class Categories(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class SizeCatalog(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class MaterialType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Product(models.Model):
    CONDITION = (('New', 'New'),('Old', 'Old'))

    unique_id = models.CharField(unique=True, max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='application/static/img/product')
    name = models.CharField(max_length=200)
    saleprice = models.IntegerField("Цена До:", default=0)
    price = models.IntegerField("Цена После:", default=0)
    condition = models.CharField(choices=CONDITION, max_length=100)
    short_description = models.TextField()
    description = models.TextField()
    сare_instructions = models.TextField(default='')
    created_date = models.DateTimeField(default=timezone.now)
    views = models.IntegerField(default=0)

    Categories = models.ForeignKey(Categories, on_delete=models.CASCADE)
    Color = models.ForeignKey(Color, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.unique_id is None and self.created_date and self.id:
            self.unique_id = self.created_date.strftime('75%Y%m%d23') + str(self.id)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
class Stuff(models.Model):
    name = models.ForeignKey(MaterialType, on_delete=models.CASCADE)
    percent = models.CharField(max_length=200, default='')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
class Sizes(models.Model):
    name = models.ForeignKey(SizeCatalog, on_delete=models.CASCADE)
    url = models.CharField(max_length=200, default='')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
class Images(models.Model):
    image = models.ImageField(upload_to='application/static/img/product')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Tag(models.Model):
    name = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

### КЛАСС ПОСТОВ ###
    
class WebThemePost(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class WebSubThemePost(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class WebPost(models.Model):
    name = models.CharField(max_length=200, default='')

    unique_id = models.CharField(unique=True, max_length=200, null=True, blank=True)
    short_description = models.TextField(default='')
    photo_create = models.CharField(max_length=200, default='')
    views = models.IntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='application/static/img/post', default='')
    content = RichTextUploadingField(default='')

    theme = models.ForeignKey(WebThemePost, on_delete=models.CASCADE, default=1)
    subtheme = models.ForeignKey(WebSubThemePost, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name
    
class WebPostType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class WebPostCategories(models.Model):
    name = models.ForeignKey(WebPostType, on_delete=models.CASCADE)
    post = models.ForeignKey(WebPost, on_delete=models.CASCADE, default=1)
    

    


