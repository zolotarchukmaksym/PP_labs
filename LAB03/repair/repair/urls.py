from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('repair_app.url')),
    path('customers/', include('customers.url')),
    path('technicians/', include('technician.url')),
]

