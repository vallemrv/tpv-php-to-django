# @Author: Manuel Rodriguez <valle>
# @Date:   01-Jan-2018
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 27-Jun-2018
# @License: Apache license vesion 2.0


"""service_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include

urlpatterns = [
    url(r'^almacen/', include("almacen.urls"), name="almacen"),
    url(r'^contabilidad/', include("contabilidad.urls"), name="conta"),
    url(r'^gestion/', include("gestion.urls"), name="gestion"),
    url(r'^ventas/', include("ventas.urls"), name="ventas"),
    url(r'', include("inicio.urls")),
]
