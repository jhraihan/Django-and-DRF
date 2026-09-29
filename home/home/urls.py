
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('aiven/', include('aiven.urls')),
    path('', include('dynamic.urls'))
]
