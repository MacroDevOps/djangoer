from django.db import models


from django.db import models
from mdeditor.fields import MDTextField


class ExampleModel(models.Model):
    name = models.CharField(max_length=10)
    content = MDTextField()

    class Meta:
        verbose_name = "文档"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
