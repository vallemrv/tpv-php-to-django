# @Author: Manuel Rodriguez <valle>
# @Date:   10-Jun-2018
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 19-Jun-2018
# @License: Apache license vesion 2.0



from django.conf.urls import url
from . import consumers

url_reg = r'^ws/impresion/(?P<print_name>[^/]+)/$'
websocket_urlpatterns = [
    url(url_reg, consumers.ImpresionConsumer),
]
