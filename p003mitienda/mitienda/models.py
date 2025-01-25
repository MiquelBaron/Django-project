from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)

    class Meta:
        ordering=['name']
        indexes = [
            models.Index(fields=['name'])
        ]


    def __str__(self):
        return self.name


class Products(models.Model):
    category = models.ForeignKey(Category,
                                related_name='products',
                                on_delete=models.CASCADE) #Al eliminar la categoria se eliminaran sus productos tambien (cascada)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    available=models.BooleanField(default=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering=['name']

    def __str__(self):
        return self.name
    

    