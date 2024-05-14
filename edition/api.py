from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from edition.forms import EditionForm, SubEditionForm
from edition.models import Edition


def rename_edition(request):
    if request.method != 'POST':
        return JsonResponse({'result': False, 'message': 'Something went wrong please try again later'})
    name = request.POST.get('name')
    edition_id = request.POST.get('edition_id')
    edition = get_object_or_404(Edition, pk=edition_id)
    if Edition.objects.filter(name=name, is_main=edition.is_main).exclude(id=edition_id).exists():
        return JsonResponse({'result': False, 'message': 'Edition name already exist'})
    edition.name = name
    edition.save()
    return JsonResponse({'result': True, 'message': 'Edition status updated success fully'})


def add_new_sub_edition(request):
    if request.method == 'POST':
        form = SubEditionForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'result': True, 'message': 'Sub edition added successfully.'})
        else:
            error_message = list(form.errors.values())[0][0]
            return JsonResponse({'result': False, 'message': error_message})
    return JsonResponse({'result': False, 'message': 'Please enter new edition details.'})


def update_edition_status(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        print(f"got status id {status}")
        edition_id = request.POST.get('edition_id')
        if status is not None and edition_id is not None:
            edition = Edition.objects.get(id=edition_id)
            edition.is_active = str(status) == '1'
            edition.save()
            return JsonResponse({'result': True, 'message': 'Edition status updated success fully'})
    return JsonResponse({'result': False, 'message': 'Something went wrong please try again later'})


def add_new_edition(request):
    if request.method == 'POST':
        form = EditionForm(request.POST)
        if form.is_valid():
            new_edition = form.save(commit=False)
            new_edition.is_main = True
            new_edition.save()
            return JsonResponse({'result': True, 'message': 'Edition added successfully.'})
        else:
            error_message = list(form.errors.values())[0][0]
            return JsonResponse({'result': False, 'message': error_message})
    return JsonResponse({'result': False, 'message': 'Please enter new edition details.'})


def sub_editions(request):
    if request.method == 'POST':
        edition_id = request.POST.get('edition_id', 0)
        if editions := Edition.get_sub_editions(edition_id):
            output = [{'id': obj.id, 'name': obj.name} for obj in editions]
        else:
            output = []
        return JsonResponse({'result': True, 'message': 'OK', 'editions': output})
    return JsonResponse({'result': False, 'message': 'Something went please try again later'})
