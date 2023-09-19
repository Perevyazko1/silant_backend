from django.urls import path

from .views import get_machine_data, get_maintenance, get_complaints, get_machine_list, post_machine_data,\
    post_maintenance_data, post_complaints_data,get_maintenance_unit

urlpatterns = [
    path('api/machine/', get_machine_data),
    path('api/update_machine/', post_machine_data),
    path('api/update_maintenance/', post_maintenance_data),
    path('api/update_complaints/', post_complaints_data),
    path('api/maintenance/', get_maintenance),
    path('api/maintenance_unit/', get_maintenance_unit),
    path('api/complaints/', get_complaints),
    path('api/machine_list/', get_machine_list),
]
