from django.urls import path
from . import views, api

urlpatterns = [
    path('', views.home, name='epaper-home'),
    path('add', views.add_new_paper, name='epaper-add-new'),
    path('manage/<int:paper_id>', views.manage, name='epaper-manage'),
    path('variants', views.variants, name='epaper-variants'),

    # api
    path('api/add/additional', api.add_additional_paper, name='epaper-api-add-additional-paper'),
    path('api/add', api.add_new_paper, name='epaper-api-add-new'),
    path('api/update/status', api.update_paper_status, name='api-update-paper-status'),
    path('api/pages/reorder', api.reorder_pages, name='api-reorder-epaper'),
    path('api/page/delete', api.delete_epaper_page, name='api-delete-epaper-page'),
    path('api/find/release', api.find_main_editions_paper, name='api-find-main-edition-paper-release'),
    path('api/upload/variant', api.upload_sub_edition_variant, name='api-upload-paper-variant'),
    path('api/home', api.epaper_home_data, name='api-epaper-home-data'),

]
