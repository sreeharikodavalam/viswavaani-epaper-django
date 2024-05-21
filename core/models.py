import uuid
from django.db import models
from django.urls import reverse
from urllib.parse import urljoin
from epaper.models import PaperPage
from viswavaani.settings import BASE_URL


class PaperCut(models.Model):
    """ePaper page cut"""
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
        sub_url = reverse('share-paper-cut', args=[str(self.id)])
        return urljoin(BASE_URL, sub_url)


class Subscriber(models.Model):
    """ePaper Subscribers"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(default=False)
    date = models.DateField(unique=False, auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Subscriber'
        verbose_name_plural = 'Subscribers'
        db_table = 'paper_subscriber'

    def __str__(self):
        return self.email
