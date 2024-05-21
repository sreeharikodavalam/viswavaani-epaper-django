import os
import uuid
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseNotFound
from PIL import Image
import requests
from io import BytesIO

from django.shortcuts import render
from django.utils.encoding import smart_str

from core.models import PaperCut
from epaper.models import PaperPage
from epaper.utils.R2Boto import R2Boto
from viswavaani import settings


def email(request):
    return render(request, 'email/email_subscription_verification.html')


def api_generate_paper_share_image(request, page_id, x, y, w, h):
    try:
        page = PaperPage.objects.filter(pk=page_id).first()
        response = requests.get(page.gif_url)
        if response.status_code != 200:
            return JsonResponse({'result': False, 'message': "Cant find paper page files"}, safe=False)

        image = Image.open(BytesIO(response.content))
        cropped_image = image.crop((x, y, x + w, y + h))

        original_content_type = 'image/jpeg'
        file_extension = 'jpeg'
        print(original_content_type)
        print(file_extension)
        # Create a blank image with the same width as the cropped image and a height for the header

        header_height = 200  # Adjust the height as needed
        blank_image = Image.new('RGB', (cropped_image.width, cropped_image.height + header_height), color='white')

        # Paste the cropped image onto the blank image, leaving space for the header
        blank_image.paste(cropped_image, (0, header_height))

        # Load the logo image
        logo_path = os.path.join(settings.STATICFILES_DIRS[0], 'logo-white-bg.jpg')
        logo_image = Image.open(logo_path)

        # Resize the logo image if necessary
        max_logo_size = (180, 180)  # Adjust the maximum logo size as needed
        logo_image.thumbnail(max_logo_size)

        # Calculate the position to place the logo at the center
        logo_position = ((blank_image.width - logo_image.width) // 2, (header_height - logo_image.height) // 2)

        # Paste the logo onto the blank image
        blank_image.paste(logo_image, logo_position)

        # Save the image to a temporary file
        temp_file = BytesIO()
        blank_image.save(temp_file, format=file_extension)
        image_url = upload_s3(temp_file, file_extension)
        paper_cut = PaperCut.objects.create(image_url=image_url, page_id=page_id)
        data = {
            'image_url': image_url,
            'share_url': paper_cut.share_url()
        }
        return JsonResponse({'result': True, 'message': "OK", "data": data}, safe=False)
    except PaperPage.DoesNotExist:
        print("Paper page does not exist.")
        return JsonResponse({'result': False, 'message': "Paper page does not exist."}, safe=False)

    except Exception as e:
        print("An error occurred while generating paper share image.")
        print(e)
        return JsonResponse({'result': False, 'message': "Something went wrong..."}, safe=False)


def upload_s3(temp_file, file_extension):
    try:
        bucket_path = f"share/{uuid.uuid4()}.{file_extension}"
        boto = R2Boto()
        temp_file.seek(0)
        boto.upload_file_obj(temp_file, bucket_path)
        return boto.get_url(bucket_path)
    except Exception as e:
        print("An error occurred while uploading to S3.")
        raise


def download_from_bucket(request, page_id, file):
    page = PaperPage.objects.filter(id=page_id).first()
    if not page:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    url = page.gif_url if file == 'gif' else page.pdf_url
    extension = ".gif" if file == 'gif' else ".pdf"
    file_name = f"vishwavani-epaper-{page.paper.date}{extension}"
    response = requests.get(url)
    if response.status_code == 200:
        response = HttpResponse(response.content, content_type=response.headers.get('Content-Type', 'application/octet-stream'))
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
        return response
    return HttpResponseNotFound('<h1>404 Page not found</h1>')


def proxy_file(request):
    if file_url := request.GET.get('to'):
        response = requests.get(file_url)
        if response.status_code == 200:
            content_type = response.headers['Content-Type']
            file_name = os.path.basename(file_url)
            response = HttpResponse(response.content, content_type=content_type)
            response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
            return response
    return HttpResponseNotFound('<h1>404 Page not found</h1>')
