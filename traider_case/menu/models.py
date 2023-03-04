from django.db import models


class Menu(models.Model):
    name = models.CharField(verbose_name='Name', max_length=50)
    url = models.CharField(verbose_name='URL', max_length=200, unique=True)
    parent = models.ForeignKey(
        'Menu',
        on_delete=models.CASCADE,
        related_name='childes',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Menu'

    def __str__(self):
        return self.name


class HeadMenu(models.Model):
    menu = models.OneToOneField(
        Menu,
        on_delete=models.CASCADE,
        related_name='head',
        primary_key=True,
    )
    title = models.SlugField(verbose_name='Title')

    def __str__(self):
        return self.title
