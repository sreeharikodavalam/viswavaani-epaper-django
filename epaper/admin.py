from django.contrib import admin
from epaper.models import Paper, PaperPage
admin.site.register(PaperPage)
admin.site.register(Paper)