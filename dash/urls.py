from django.urls import path, include
from . import views
urlpatterns = [

    path('', views.home_page, name="home_page_m"),
    path('login/', views.login_user, name="login_user_m"),
    path('logout/', views.logout_user, name="logout_user_m"),
    path('mfi/', views.mfi_applications, name="mfi_applications"),
    path('process/', views.processes, name="processes"),
    path('mfi/<str:loan_id>/', views.mfi_application_info, name="mfi_application_info"),
    path('process/<str:loan_id>/', views.process_info, name="process_info"),
    path('mfi/<str:loan_id>/upload/', views.mfi_doc, name="mfi_doc"),
    path('process/<str:loan_id>/upload/', views.process_doc, name="process_dsoc"),
]
