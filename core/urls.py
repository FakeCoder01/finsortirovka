from django.urls import path, include
from . import views
urlpatterns = [

    path('', views.home_page, name="home_page"),
    path('login/', views.login_user, name="login_user"),
    path('signup/', views.signup_user, name="signup_user"),
    path('logout/', views.logout_user, name="logout_user"),
    path('profile/', views.manage_profile, name="manage_profile"),
    path('mfi/', views.mfi_form, name="mfi_form"),
    path('dash/', views.dashboard, name="dashboard"),
    path('dash/<str:loan_id>/', views.loan_details, name="loan_details"),
    path('dash/<str:loan_id>/upload/', views.upload_doc, name="upload_doc"),
]
