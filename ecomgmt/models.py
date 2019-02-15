from django.db import models


class Supplier(models.Model):
    name=models.CharField(max_length=128)
    logo=models.ImageField(upload_to='upload/ecologo', blank=True, null=True)
    website=models.URLField()

    def __unicode__(self):
        return self.name


class ProductType(models.Model):
    name=models.CharField(max_length=128)
    pseudo_name = models.CharField(max_length=64, unique=True)
    description=models.CharField(max_length=1024)
    scene=models.CharField(max_length=256, blank=True, null=True)
    sort_no=models.IntegerField(default=100)

    def __unicode__(self):
        return self.name


class Product(models.Model):
    name=models.CharField(max_length=128)
    type=models.ForeignKey(ProductType, blank=True, null=True, related_name='type_products')
    supplier=models.ForeignKey(Supplier, blank=True, null=True, related_name='supplier_products')
    description=models.CharField(max_length=1024, blank=True, null=True)
    keywords=models.CharField(max_length=256, blank=True, null=True)
    logo=models.ImageField(upload_to='upload/ecologo', blank=True, null=True)
    website=models.URLField(blank=True, null=True)
    sort_no=models.IntegerField(default=100)

    def __unicode__(self):
        return self.name

    def get_website(self):
        return self.website or self.supplier.website
