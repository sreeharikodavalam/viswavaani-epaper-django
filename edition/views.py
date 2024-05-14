from django.shortcuts import get_object_or_404, render
from edition.models import Edition


def home(request):
    edition = Edition.objects.filter(is_main=True).order_by('id')
    return render(request, 'edition/list_edition.html', {'editions': edition})


def sub_editions_list(request):
    main_editions = Edition.objects.filter(is_main=True).order_by('id')
    edition_id = request.GET.get("id")
    if edition_id is not None:
        sub_editions = Edition.objects.filter(parent_id=edition_id).order_by('id')
    else:
        edition_id = main_editions[0].pk
        sub_editions = Edition.objects.filter(parent=edition_id).order_by('id')

    return render(request, 'edition/list_sub_edition.html',
                  {'main_editions': main_editions, 'sub_editions': sub_editions, 'parent_id': int(edition_id)})


def add_new_edition(request):
    return render(request, 'edition/add_edition.html')


def rename_edition(request, edition_id):
    edition = get_object_or_404(Edition, pk=edition_id)
    return render(request, 'edition/rename_edition.html', {'edition': edition})


def add_new_sub_edition(request):
    main_editions = Edition.get_main_editions()
    return render(request, 'edition/add_sub_edition.html', {'main_editions': main_editions})
