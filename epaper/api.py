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


def delete_epaper_page(request):
    paper_id = request.POST.get('paper_id')
    page_id = request.POST.get('page_id')
    if all([page_id, paper_id]):
        if page := PaperPage.objects.filter(id=page_id, paper_id=paper_id):
            page.delete()
            return JsonResponse({'result': True, 'message': 'Page has been deleted success fully'})
        else:
            return JsonResponse({'result': False, 'message': 'unable to find page you looking for'})
    return JsonResponse({'result': False, 'message': 'Something went wrong please try again later'})


def add_additional_paper(request):
    paper_id = request.POST.get('paper_id')
    uploaded_files = request.FILES.getlist('epaper')
    paper = get_object_or_404(Paper, pk=paper_id)
    if uploaded_files is not None:
        pdf_processor = PDFProcessor(uploaded_files, paper.date)
        result = pdf_processor.process_files()
        print(result)
        if result:
            highest_page_number = PaperPage.objects.filter(paper_id=paper_id).aggregate(Max('page_number'))['page_number__max'] or 0
            for page_number, page_data in enumerate(result, start=1):
                PaperPage.objects.create(
                    paper=paper,
                    pdf_url=page_data['pdf_url'],
                    gif_url=page_data['gif_url'],
                    thumbnail_url=page_data['thumbnail_url'],
                    page_number=highest_page_number + page_number
                )
            return JsonResponse({'result': True, 'message': 'New pages are added successfully'})
        else:
            return JsonResponse({'result': False, 'message': 'Please upload valid file'})

    return JsonResponse({'result': False, 'message': 'Something went wrong please try again later'})


def add_new_paper(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        edition_id = request.POST.get('edition_id')
        uploaded_files = request.FILES.getlist('epaper[]')
        if date is not None and edition_id is not None:
            edition = get_object_or_404(Edition, pk=edition_id)
            try:
                return _add_new_paper_do(date, edition, uploaded_files)
            except ValueError:
                return JsonResponse(
                    {'result': False, 'message': 'Invalid date format. It must be in DD/MM/YYYY format.'})

    return JsonResponse({'result': False, 'message': 'Something went wrong please try again later'})


# validate ePaper date for edition
# Upload ePaper Pdfs
def _add_new_paper_do(date, edition, uploaded_files):
    date_obj = datetime.strptime(date, '%d/%m/%Y')
    formatted_date = date_obj.strftime('%Y-%m-%d')
    if Paper.objects.filter(date=formatted_date, edition=edition).exists():
        return JsonResponse({'result': False, 'message': 'ePaper has been already created, Goto manage ePaper section'})
    e_paper = Paper.objects.create(date=formatted_date, edition=edition)
    if uploaded_files:
        pdf_processor = PDFProcessor(uploaded_files, date_obj)
        if result := pdf_processor.process_files():
            for page_number, page_data in enumerate(result, start=1):
                PaperPage.objects.create(
                    paper=e_paper,
                    pdf_url=page_data['pdf_url'],
                    gif_url=page_data['gif_url'],
                    thumbnail_url=page_data['thumbnail_url'],
                    page_number=page_number
                )
    return JsonResponse({'result': True, 'message': 'Edition status has been updated success fully'})


def update_paper_status(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        print(f"got status id {status}")
        paper_id = request.POST.get('paper_id')
        if status is not None and paper_id is not None:
            paper = Paper.objects.get(id=paper_id)
            paper.is_active = str(status) == '1'
            paper.save()
            return JsonResponse({'result': True, 'message': 'ePaper status has been updated success fully'})
    return JsonResponse({'result': False, 'message': 'Something went wrong please try again later'})


def reorder_pages(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        paper = get_object_or_404(Paper, pk=str(data['paper_id']))
        if data['page_order'] is not None:
            for index, page_id in enumerate(data['page_order']):
                if page := PaperPage.objects.filter(id=page_id, paper=paper).first():
                    page.page_number = index
                    page.save()
            return JsonResponse({'result': True, 'message': 'New page order has been saved success fully'})
    return JsonResponse({'result': False, 'message': 'Something went wrong please try again later'})


def find_main_editions_paper(request):
    if request.method == 'POST':
        if data := validate_json_string_data(request.body, ['main_edition', 'sub_edition', 'date']):
            if date := validate_date_string(data['date']):
                if edition := Edition.objects.filter(id=data['main_edition']).first():
                    if sub_edition := Edition.objects.filter(id=data['sub_edition'], parent=edition).first():
                        if paper := Paper.objects.filter(edition=edition, date=date).first():
                            edition_papers_json = _get_paper_pages(paper, sub_edition)
                            return JsonResponse({'result': True, 'message': 'Found an ePaper on this date, now you can create variants',
                                                 'data': {'paper_id': paper.id, 'sub_edition_id': sub_edition.id, 'paper_pages': edition_papers_json}})
            return JsonResponse({'result': False, 'message': 'Please publish main edition, before looking into its variants'})
    return JsonResponse({'result': False, 'message': 'Something went wrong please try again later'})


def _get_paper_pages(paper, sub_edition):
    main_edition_papers = PaperPage.objects.filter(paper=paper, is_variant=False)
    edition_papers_json = []
    for paper_page in main_edition_papers:
        variant_paper = PaperPage.objects.filter(parent_page=paper_page, sub_edition=sub_edition).first()
        variant_data = {
            'id': paper_page.id,
            'gif_url': paper_page.gif_url,
            'thumbnail_url': paper_page.thumbnail_url,
            'has_variant': variant_paper is not None,
        }
        if variant_paper:
            variant_data.update({
                'variant_gif_url': variant_paper.gif_url,
                'variant_thumbnail_url': variant_paper.thumbnail_url,
                'variant_id': variant_paper.id,
            })
        edition_papers_json.append(variant_data)
    return edition_papers_json


def _get_paper_pages_for_home(paper, sub_edition):
    main_edition_papers = PaperPage.objects.filter(paper=paper, is_variant=False)
    edition_papers_json = []
    for counter, paper_page in enumerate(main_edition_papers, start=1):
        if variant_paper := PaperPage.objects.filter(parent_page=paper_page, sub_edition=sub_edition).first():
            variant_data = {
                'id': counter,
                'page_id': variant_paper.id,
                'pdf_url': variant_paper.pdf_url,
                'gif_url': variant_paper.gif_url,
                'thumbnail_url': variant_paper.thumbnail_url,
            }
        else:
            variant_data = {
                'id': counter,
                'page_id': paper_page.id,
                'pdf_url': paper_page.pdf_url,
                'gif_url': paper_page.gif_url,
                'thumbnail_url': paper_page.thumbnail_url,
            }
        edition_papers_json.append(variant_data)
    return edition_papers_json


def upload_sub_edition_variant(request):
    if request.method == 'POST':
        page_id = request.POST.get('page_id')
        edition_id = request.POST.get('edition_id')
        if not all([page_id, edition_id]):
            return JsonResponse({'result': False, 'message': 'Invalid request data'})
        if edition := Edition.objects.filter(id=edition_id).first():
            if page := PaperPage.objects.filter(id=page_id).first():
                if uploaded_files := request.FILES.getlist('epaper[]'):
                    pdf_processor = PDFProcessor(uploaded_files, page.paper.date)
                    if result := pdf_processor.process_files(only_first=True):
                        new_variant = PaperPage.objects.create(
                            paper=page.paper,
                            pdf_url=result[0]['pdf_url'],
                            gif_url=result[0]['gif_url'],
                            thumbnail_url=result[0]['thumbnail_url'],
                            page_number=page.page_number,
                            is_variant=True,
                            sub_edition=edition,
                            parent_page=page, )
                        if new_variant is not None:
                            output = {
                                'page_id': page_id,
                                'variant_id': new_variant.id,
                                'variant_gif_url': new_variant.gif_url,
                                'variant_thumbnail_url': new_variant.thumbnail_url,
                            }
                            return JsonResponse({'result': True, 'message': 'New variant has been uploaded', 'data': output, })
        return JsonResponse({'result': False, 'message': 'Something went wrong please try again later'})


def epaper_home_data(request):
    if date_string := request.POST.get('date'):
        date = validate_date_string(date_string)
    else:
        dt = datetime.now()
        date = dt.strftime('%Y-%m-%d')
    date_obj = datetime.strptime(date_string, '%Y-%m-%d')
    print(date_string)
    print(date)
    print(request.POST)
    sub_edition_id = request.POST.get('sub_edition', 0)
    sub_edition = Edition.objects.filter(is_main=False, pk=sub_edition_id, is_active=True).first() or Edition.objects.filter(is_main=False, is_active=True).first()
    print(sub_edition)
    if paper := Paper.objects.filter(edition=sub_edition.parent, date=date_obj, is_active=True).first():
        if pages := _get_paper_pages_for_home(paper, sub_edition):
            return JsonResponse({'result': True, 'message': 'OK', 'pages': pages})
    return JsonResponse({'result': False, 'message': 'No paper available.', 'pages': []}, safe=False)
