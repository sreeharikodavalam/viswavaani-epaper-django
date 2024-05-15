import mimetypes
import os
import uuid

from django.http import HttpResponse, FileResponse, JsonResponse
from django.core.files.base import ContentFile
from PIL import Image
import requests
from io import BytesIO
from epaper.models import PaperPage
from epaper.utils.R2Boto import R2Boto
from viswavaani import settings


def proxy_file(request):
    image_url = request.GET.get('to')
    response = requests.get(image_url)
    if response.status_code == 200:
        content_type = response.headers['Content-Type']
        return HttpResponse(response.content, content_type=content_type)
    else:
        return HttpResponse('Failed to fetch image', status=response.status_code)


def generate_paper_share_image(request, page_id, x, y, w, h):
    try:
        page = PaperPage.objects.filter(pk=page_id).first()
        response = requests.get(page.gif_url)
        if response.status_code != 200:
            return None

        image = Image.open(BytesIO(response.content))
        cropped_image = image.crop((x, y, x + w, y + h))

        original_content_type = response.headers.get('content-type')
        file_extension = original_content_type.split('/')[-1]

        # Create a blank image with the same width as the cropped image and a height for the header
        header_height = 200  # Adjust the height as needed
        blank_image = Image.new('RGB', (cropped_image.width, cropped_image.height + header_height), color='white')

        # Paste the cropped image onto the blank image, leaving space for the header
        blank_image.paste(cropped_image, (0, header_height))

        # Load the logo image
        logo_path = os.path.join(settings.STATICFILES_DIRS[0], 'logo-white-bg.jpg')
        logo_image = Image.open(logo_path)

        # Resize the logo image if necessary
        max_logo_size = (180)  # Adjust the maximum logo size as needed
        logo_image.thumbnail(max_logo_size)

        # Calculate the position to place the logo at the center
        logo_position = ((blank_image.width - logo_image.width) // 2, (header_height - logo_image.height) // 2)

        # Paste the logo onto the blank image
        blank_image.paste(logo_image, logo_position)

        # Save the image to a temporary file
        temp_file = BytesIO()
        blank_image.save(temp_file, format=file_extension)
        return JsonResponse({'result': True, 'message': "OK", "data": upload_s3(temp_file, file_extension)}, safe=False)

    except:
        return JsonResponse({'result': False, 'message': "Something went wrong..."}, safe=False)


def upload_s3(temp_file, file_extension):
    bucket_path = f"share/{uuid.uuid4()}.{file_extension}"
    boto = R2Boto()
    temp_file.seek(0)
    boto.upload_file_obj(temp_file, bucket_path)
    return boto.get_url(bucket_path)
