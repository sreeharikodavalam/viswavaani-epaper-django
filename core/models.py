import uuid
from django.db import models
from django.urls import reverse

from epaper.models import PaperPage
from viswavaani.settings import BASE_URL


class PaperCut(models.Model):
    """News paper page cut"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_main = models.BooleanField(default=False)
    date = models.DateField(unique=False, auto_now_add=True)
    page = models.ForeignKey(PaperPage, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=512)

    class Meta:
        verbose_name = 'PaperCut'
        verbose_name_plural = 'PaperCuts'
        db_table = 'paper_cut'

    def __str__(self):
        return f"{self.date} - {self.id}"

    def share_url(self):
        return f"{BASE_URL}{reverse('share-paper-cut', args=[str(self.id)])}"
