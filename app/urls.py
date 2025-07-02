from django.urls import path, include
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name="index"),
    path('create-patient', views.create_patient, name="create-patient"),
    path('search-patient', views.search_patient, name="search-patient"),
    path('search-patient-filter/', views.search_patient_filter, name="search-patient-filter"),
    path('update-patient/<str:patient_id>/', views.update_patient, name="update-patient"),
    path('list-patients', views.list_patients, name="list-patients"),
]
