import os
import uuid
from pdf2image import convert_from_path
from PyPDF2 import PdfWriter, PdfReader
from django.conf import settings
from epaper.utils.R2Boto import R2Boto


def _delete_local_file(file_path):
    """Delete a file from the local file system if it exists."""
    if os.path.exists(file_path):
        os.remove(file_path)


def _cleanup_files(processed_files):
    """Clean up local files after processing and uploading."""
    try:
        for page in processed_files:
            _delete_local_file(page['pdf_path'])
            _delete_local_file(page['gif_path'])
            _delete_local_file(page['thumbnail_path'])
    except Exception as e:
        print(f"Error deleting  file: {e}")


class PDFProcessor:
    def __init__(self, uploaded_files, upload_date):
        self.uploaded_files = uploaded_files
        self.upload_date = upload_date
        self.boto = R2Boto()

    def process_files(self, only_first=False):
        processed_files = self._process_uploaded_files(only_first)
        file_urls = self._generate_file_urls(processed_files)
        _cleanup_files(processed_files)
        return file_urls

    def _process_uploaded_files(self, only_first):
        processed_files = []
        folder_name = self.upload_date.strftime('%m-%Y')

        for uploaded_file in self.uploaded_files:
            file_uuid = str(uuid.uuid4())
            if uploaded_file.name.endswith('.pdf'):
                directory = os.path.join(settings.MEDIA_ROOT, 'epaper', folder_name)
                os.makedirs(directory, exist_ok=True)

                pdf_filename = f'pdf-{file_uuid}.pdf'
                pdf_path = os.path.join(directory, pdf_filename)
                with open(pdf_path, 'wb') as f:
                    f.write(uploaded_file.read())

                # Split the PDF into individual pages
                individual_pdf_paths = split_pdf_to_pages(pdf_path, file_uuid, only_first)

                for i, individual_pdf_path in enumerate(individual_pdf_paths, start=1):
                    # Convert each page to GIF and generate thumbnail
                    gif_path, thumbnail_path = convert_to_gif_and_thumbnail(individual_pdf_path, directory, file_uuid, i)
                    print(individual_pdf_path)
                    processed_files.append({
                        'pdf_path': individual_pdf_path,
                        'gif_path': gif_path,
                        'thumbnail_path': thumbnail_path
                    })

        return processed_files

    def _generate_file_urls(self, processed_files):
        file_urls = []
        for page in processed_files:
            bucket_file = {
                'pdf_url': get_relative_path(page['pdf_path']),
                'gif_url': get_relative_path(page['gif_path']),
                'thumbnail_url': get_relative_path(page['thumbnail_path']),
            }
            self.upload_files_to_bucket(page['gif_path'], bucket_file['gif_url'])
            self.upload_files_to_bucket(page['thumbnail_path'], bucket_file['thumbnail_url'])
            self.upload_files_to_bucket(page['pdf_path'], bucket_file['pdf_url'])

            bucket_file['pdf_url'] = self.boto.base_url + bucket_file['pdf_url']
            bucket_file['gif_url'] = self.boto.base_url + bucket_file['gif_url']
            bucket_file['thumbnail_url'] = self.boto.base_url + bucket_file['thumbnail_url']

            file_urls.append(bucket_file)

        return file_urls

    def upload_files_to_bucket(self, source_path, destination_path):
        if source_path and destination_path:
            self.boto.upload_file(source_path, destination_path)


# PDF and other utility methods

def split_pdf_to_pages(pdf_path, file_uuid, only_first=False):
    individual_pdf_paths = []
    with open(pdf_path, 'rb') as f:
        pdf_reader = PdfReader(f)
        print(f"PDF Page Length : {len(pdf_reader.pages)}")
        for i in range(len(pdf_reader.pages)):
            individual_pdf_filename = f'pdf-{file_uuid}-{i + 1}.pdf'
            individual_pdf_path = os.path.join(os.path.dirname(pdf_path), individual_pdf_filename)
            writer = PdfWriter()
            writer.add_page(pdf_reader.pages[i])
            with open(individual_pdf_path, 'wb') as output_pdf:
                writer.write(output_pdf)
            individual_pdf_paths.append(individual_pdf_path)
            # return first page only
            if only_first:
                break
    _delete_local_file(pdf_path)
    return individual_pdf_paths


def convert_to_gif_and_thumbnail(pdf_path, directory, file_uuid, page_number):
    # Convert PDF page to image
    image = convert_from_path(pdf_path)[0]

    # Save as GIF
    gif_filename = f'gif-{file_uuid}-{page_number}.gif'
    gif_path = os.path.join(directory, gif_filename)
    image.save(gif_path, format='GIF')

    # Generate thumbnail
    thumbnail_filename = f'gif-thumb-{file_uuid}-{page_number}.png'
    thumbnail_path = os.path.join(directory, thumbnail_filename)
    image.thumbnail((420, 420))
    image.save(thumbnail_path)

    return gif_path, thumbnail_path


def get_relative_path(full_path):
    if full_path.startswith(str(settings.MEDIA_ROOT)):
        return os.path.relpath(full_path, settings.MEDIA_ROOT).replace("\\", "/")
    return full_path
