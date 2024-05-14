from django.db import models


class Edition(models.Model):
    """News paper edition details"""
    name = models.CharField(max_length=32, default='')
    is_main = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        """Meta definition for Edition."""

        verbose_name = 'Edition'
        verbose_name_plural = 'Editions'
        db_table = 'paper_edition'

    def __str__(self):
        return self.name

    @staticmethod
    def get_main_editions():
        return Edition.objects.filter(parent__isnull=True)

    @staticmethod
    def get_sub_editions(parent_id):
        return Edition.objects.filter(parent__id=parent_id, parent__isnull=False)
