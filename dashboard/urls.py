from django.urls import include, path
from .views import GenerateTables


urlpatterns = [
    path('upload-csv/', GenerateTables.as_view(), name='upload_csv_file'),
]
