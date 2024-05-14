
from django.contrib import admin
from django.urls import include, path
from dashboard.views import home
from epaper.views import epaper_home
from core import views as core_views
urlpatterns = [
    #Paper Home
    path('', epaper_home, name='view_paper'),
    #Proxy
    path('direct', core_views.proxy_file, name='direct-file'),
    path('share/<int:page_id>/<int:x>/<int:y>/<int:w>/<int:h>', core_views.generate_paper_share_image, name='share-file'),
    #
    path('home', home, name='home'),
    path("dashboard/", include("dashboard.urls")),
    path("authentication/", include("authentication.urls")),
    path("epaper/", include("epaper.urls")),
    path("edition/", include("edition.urls")),
    
    #tools
    path('super-admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),

]
