# @Author: Manuel Rodriguez <valle>
# @Date:   10-Jun-2018
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 18-Jun-2018
# @License: Apache license vesion 2.0

# chat/urls.py
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
