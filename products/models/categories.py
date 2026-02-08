from django.db import models
from slugify import slugify


class Category(models.Model):
    name = models.CharField(max_length=190)
    slug = models.SlugField(max_length=210, unique=True, blank=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
