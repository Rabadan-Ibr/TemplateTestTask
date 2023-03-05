from django.db import models
from django.urls import reverse, NoReverseMatch


class Menu(models.Model):
    name = models.CharField(verbose_name='Name', max_length=50)
    url = models.CharField(
        verbose_name='URL',
        max_length=200,
        blank=True,
        null=True,
    )
    named_url = models.CharField(
        verbose_name='Named URL',
        max_length=200,
        blank=True,
        null=True,
    )
    parent = models.ForeignKey(
        'Menu',
        on_delete=models.CASCADE,
        related_name='childes',
        blank=True,
        null=True,
    )
    menu_title = models.ForeignKey(
        'HeadMenu',
        on_delete=models.PROTECT,
        related_name='menus',
    )

    class Meta:
        verbose_name = 'Menu'
        ordering = 'name',

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
    ):
        if self.named_url is not None:
            try:
                self.url = reverse(self.named_url)
            except NoReverseMatch:
                self.url = '/404/'
        elif self.url is None:
            self.url = '/404/'
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

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
