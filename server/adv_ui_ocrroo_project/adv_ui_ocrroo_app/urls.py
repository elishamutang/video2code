from django.urls import path
from . import views

urlpatterns = [
    path('video/', views.serve_video, name='serve_video'),
    path('video/frame/<str:timestamp>/', views.get_vid_frame, name='get_vid_frame'),
    path('video/duration/', views.get_vid_duration, name='get_vid_duration')
]