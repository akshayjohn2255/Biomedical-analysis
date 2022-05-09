"""bioproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from bioproject.bioapp import views
from bioproject import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/',views.about),
    path('',views.home),
    path('home/',views.home),
    path('loginPage/',views.login),
    path('logincheck/',views.logincheck),
    path('logout/',views.logout),

    path('about-us/',views.about),
    path('Adminabout/',views.ADabout),
    path('userabout/',views.userabout),
    path('docabout/',views.docabout),

    path('contact/',views.contact),


    # admin
    path('adminHome/',views.adminHome),
    path('diseaseList/', views.adviewNewDislist),
    path('viewDoctorlist/', views.viewDoctorlist),
    path('viewNewDoc/',views.viewNewDoc),
    path('delDoc/',views.delDoc),

    path('docManage/',views.manageDoc),
    path('newdiseasedb/',views.newDiseasedb),
    path('disManage/',views.disManage),
    path('activeDiseases/',views.activeDiseases),


    path('viewUsers/',views.viewUsers),

    #
    path('reRank/',views.reRank),
    #

    #user

    path('uregistration/',views.uregistration),
    path('uregistdb/',views.uregistdb),
    path('userHome1/',views.userHome1),

    path('uProfile/',views.uProfile),
    path('uUpdatedb/',views.uUpdatedb),
    path('searchDisease/',views.searchDisease),
    path('getUrlContent/',views.getUrlContent),
    path('userViewDoc/',views.userViewDoc),

    path('userViewDoctors/',views.userViewDoctors),

    #Doctor
    path('docHome/',views.docHome),
    path('doctorRegpage/',views.docReg),
    path('docRegDB/',views.docRegDB),
    path('dProfile/',views.viewDprofile),
    path('docUpdate/',views.docUpdate),

    path('dAddDisease/',views.dAddDisease),
    path('docViewAddedDiseases/',views.docViewAddedDiseases),
    path('disupdate/',views.disupdate),
    path('ranking/',views.getRank),




]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)