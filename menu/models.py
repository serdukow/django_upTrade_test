from django.db import models
from django.utils.translation import gettext_lazy as _


class Parent(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Menu name'))

    def __str__(self):
        return self.name


class Child(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('Title'))
    parent = models.ForeignKey('Parent', on_delete=models.CASCADE,
                               blank=True, null=True, verbose_name=_('Parent'))
    href = models.CharField(max_length=200, blank=True, null=True,
                            verbose_name=_('Link'))
    named_url = models.CharField(max_length=50, blank=True, null=True,
                                 verbose_name=_('Named URL'))
    menu = models.ForeignKey('Parent', on_delete=models.CASCADE,
                             null=True, related_name='children', verbose_name=_('Related menu'))

    class Meta:
        ordering = ['menu', 'id']

    def __str__(self):
        return self.title
