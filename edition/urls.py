# myapp/urls.py
from django.urls import path
from edition import views, api

urlpatterns = [
    path('', views.home, name='editions'),
    path('sub', views.sub_editions_list, name='sub-editions'),
    path('add/sub', views.add_new_sub_edition, name='sub-editions-add-new'),
    path('add', views.add_new_edition, name='editions-add-new'),
    path('rename/<int:edition_id>', views.rename_edition, name='editions-rename'),

    # Api
    path('api/add', api.add_new_edition, name='editions-add-new-api'),
    path('api/sub/add', api.add_new_sub_edition, name='sub-editions-add-new-api'),
    path('api/status', api.update_edition_status, name='api-update-edition-status'),
    path('api/renames', api.rename_edition, name='editions-rename-api'),
    path('api/sub-editions/', api.sub_editions, name='api-sub-editions'),
]
