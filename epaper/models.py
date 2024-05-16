from django.db import models
from edition.models import Edition


class Paper(models.Model):
    """ePaper Model"""
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE)
    date = models.DateField(unique=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Paper'
        verbose_name_plural = 'Papers'
        db_table = 'paper'

    def __str__(self):
        return f"{self.date} - {self.edition.name}"

    @property
    def main_edition_page_count(self):
        # Count the number of pages in the main edition for this paper
        return self.paperpage_set.filter(paper__edition__is_main=True).count()

    @property
    def first_page(self):
        # Retrieve first page of this paper
        return self.paperpage_set.order_by('page_number').first()


class PaperPage(models.Model):
    """Model definition for Paper Page"""
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    pdf_url = models.CharField(max_length=1024, default='')
    gif_url = models.CharField(max_length=1024, default='')
    thumbnail_url = models.CharField(max_length=1024, default='')
    page_number = models.IntegerField(default=999)
    is_active = models.BooleanField(default=True)
    is_variant = models.BooleanField(default=False)
    parent_page = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    sub_edition = models.ForeignKey(Edition, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'
        db_table = 'paper_page'

    def __str__(self):
        return f"Page {self.page_number}"
