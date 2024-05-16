import json
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from core.models import PaperCut
from edition.models import Edition
from epaper.models import Paper, PaperPage
from django.core.serializers import serialize


@login_required
def home(request):
    paper_list = Paper.objects.order_by('-date').all()
    paginator = Paginator(paper_list, 10)
    page_number = request.GET.get("page")
    papers = paginator.get_page(page_number)
    return render(request, 'epaper/list_papers.html', {'papers': papers})


@login_required
def manage(request, paper_id):
    paper = get_object_or_404(Paper, pk=paper_id)
    pages = PaperPage.objects.filter(paper=paper).order_by('page_number')
    return render(request, 'epaper/manage_paper.html',
                  {'paper': paper, 'pages': pages, 'pages_json': json.dumps(serialize('json', pages), indent=4)})


@login_required
def add_new_paper(request):
    recent_paper = Paper.objects.order_by('-date').first()
    editions = Edition.objects.filter(is_main=True)
    return render(request, 'epaper/add_new_paper.html', {'editions': editions, 'recent_paper': recent_paper})


@login_required
def variants(request):
    main_editions = Edition.get_main_editions()
    data = {'main_editions': main_editions}
    return render(request, 'epaper/edition_variants.html', data)


def epaper_home(request):
    if main_editions := Edition.objects.filter(is_main=True, is_active=True):
        if sub_editions := Edition.get_sub_editions(main_editions.first().id):
            data = {'main_editions': main_editions, 'sub_editions': sub_editions}
            return render(request, 'epaper/view_paper.html', data)
    return render(request, 'epaper/view_paper.html', {'main_editions': [], 'sub_editions': []})


def share_paper_cut(request, share_id):
    paper_cut = get_object_or_404(PaperCut, id=share_id)
    return render(request, 'epaper/share_paper_cut.html', {'share' : paper_cut})
