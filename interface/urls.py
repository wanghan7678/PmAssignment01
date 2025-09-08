import interface.views as vs
from django.urls import path, re_path

urlpatterns = [
    path('test/', vs.generate_report)
]