from django.urls import path
from .views import run_diagnosis, sms_diagnosis, diagnosis_page, diagnosis_history, get_history

urlpatterns = [
    path('crop-diagnosis', diagnosis_page, name='crop_diagnosis'),
    path('run-diagnosis', run_diagnosis, name='run_diagnosis'),
    path('sms-diagnosis', sms_diagnosis, name='sms_diagnosis'),
    path('history/<int:user_id>', diagnosis_history, name='diagnosis_history'),
    path('get_history/<int:diagnosis_id>', get_history, name='get_history')
]