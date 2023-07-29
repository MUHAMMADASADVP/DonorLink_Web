from django.urls import path

from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("signup", views.signup, name="signup"),
    path("hsignup", views.hsignup, name="hsignup"),
    path("bsignup", views.bsignup, name="bsignup"),
    path("update", views.update,name="update"),
    path("bstock",views.bstock,name="bstock"),
    path("addpatient",views.addpatient,name="addpatient"),
    path("get_attr_value/<str:attr>/",views.get_attr_value,name='get_attr_value'),
    path("patients",views.patients,name='patients'),
    path("patients/<str:argument>/",views.patients,name='patients'),
    path("completerequest/<int:id>/",views.completerequest,name='completerequest'),
]
