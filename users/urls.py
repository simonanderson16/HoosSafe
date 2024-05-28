from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("logout", views.logout_view, name="logout"),
    path('user_home/', views.user_home, name='user_home'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('report_form/', views.report_form, name="report_form"),
    path('report_confirmation/', views.report_confirmation, name="report_confirmation"),
    path('file_uploads/', views.file_uploads, name="file_uploads"),
    path('file_uploads/new', views.file_uploads_new, name="file_uploads_new"),
    path('file_uploads/in_progress', views.file_uploads_in_progress, name="file_uploads_in_progress"),
    path('file_uploads/resolved', views.file_uploads_resolved, name="file_uploads_resolved"),
    path('my_reports', views.my_reports, name="my_reports"),
    path('user_full_report/<int:report_id>', views.user_full_report, name='user_full_report'),
    path('delete_report/<int:report_id>', views.delete_report, name='delete_report'),
    path('admin_full_report/<int:report_id>', views.admin_full_report, name='admin_full_report'),
    path('my_reports/new', views.my_reports_new, name = "new"), 
    path('my_reports/in_progress', views.my_reports_in_progress, name = "in_progress"), 
    path('my_reports/resolved', views.my_reports_resolved, name = "resolved"),
]
