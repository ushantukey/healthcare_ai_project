from django.contrib import admin
from django.urls import path
from api.views import analyze_patient

urlpatterns = [
    path('admin/', admin.site.urls),
    path('analyze/', analyze_patient),
]