from django.urls import path

from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("home", views.home_view, name="home"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("signup", views.signup, name="signup"),
    path("hsignup", views.hsignup, name="hsignup"),
    path("bsignup", views.bsignup, name="bsignup"),
    path("update", views.update,name="update"),
    path("bstock",views.bstock,name="bstock"),
    path("addpatient",views.addpatient,name="addpatient"),
    path("patients",views.patients,name='patients'),
    path("completerequest/<int:id>/",views.completerequest,name='completerequest'),
    path("history",views.history,name="history"),
    path("donorlist",views.donorlist,name="donorlist"),
    path("consentform",views.consentform,name="consentform"),
    path("consent",views.consent,name="consent"),
    path("notifications",views.notifications,name="notifications"),
    path("getdonor",views.getdonor,name="getdonor"),
    path("donationregister/<int:did>",views.donationregister,name="doationregister"),


    #API ROUTES
    path("patients/<str:argument>/",views.patients,name='patients'),
    path("get_attr_value/<str:attr>/",views.get_attr_value,name='get_attr_value'),
    path("getdonor/<int:did>/",views.getdonor,name="getdonor"),
]
