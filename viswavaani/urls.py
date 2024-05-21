from django.contrib import admin
from django.urls import include, path
from dashboard.views import home
from epaper.views import epaper_home, share_paper_cut

urlpatterns = [
    # Core
    path("", include("core.urls")),

    # Paper Home
    path('', epaper_home, name='view_paper'),
    path('share/<uuid:share_id>', share_paper_cut, name='share-paper-cut'),

    # # #
    path('home', home, name='home'),
    path("dashboard/", include("dashboard.urls")),
    path("authentication/", include("authentication.urls")),
    path("epaper/", include("epaper.urls")),
    path("edition/", include("edition.urls")),

    # tools
    path('super-admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),

]
