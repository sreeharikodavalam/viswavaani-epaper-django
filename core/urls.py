from django.urls import path
from . import views, api

urlpatterns = [
    path('direct', views.proxy_file, name='direct-file'),
    path('download/<int:page_id>/<slug:file>', views.download_from_bucket, name='download-from-bucket'),
    path('share/api/<int:page_id>/<int:x>/<int:y>/<int:w>/<int:h>', views.api_generate_paper_share_image, name='api-share-file'),
    path('email', views.email, name='email-template'),
    path('subscribe', api.subscribe_epaper, name='subscribe-epaper'),
]
