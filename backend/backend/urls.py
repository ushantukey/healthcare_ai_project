from django.contrib import admin
from django.urls import path
from api.views import analyze_patient, get_history, delete_history,delete_all_history

urlpatterns = [
    path('admin/', admin.site.urls),
    path('analyze/', analyze_patient),
    path('history/', get_history),
    path('history/delete/<int:id>/', delete_history),
    path('history/delete-all/', delete_all_history),
]