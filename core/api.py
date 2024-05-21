import json

from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from datetime import datetime
from edition.models import Edition
from epaper.models import Paper, PaperPage
from epaper.utils.pdf_utils import PDFProcessor
from django.db.models import Max
from core.utils.json_utils import validate_json_string_data
from core.utils.date_utils import validate_date_string
from django.core.paginator import Paginator


def subscribe_epaper(request):
    return JsonResponse({'result': True, 'message': 'an verification email send to you email id'})
    # paper_id = request.POST.get('paper_id')
    # page_id = request.POST.get('page_id')
    # if all([page_id, paper_id]):
    #     if page := PaperPage.objects.filter(id=page_id, paper_id=paper_id):
    #         page.delete()
    #         return JsonResponse({'result': True, 'message': 'Page has been deleted success fully'})
    #     else:
    #         return JsonResponse({'result': False, 'message': 'unable to find page you looking for'})
    # return JsonResponse({'result': False, 'message': 'Something went wrong please try again later'})