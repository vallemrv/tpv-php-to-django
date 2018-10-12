# @Author: Manuel Rodriguez <valle>
# @Date:   10-Jun-2018
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 19-Jun-2018
# @License: Apache license vesion 2.0

from django.
from django.utils.safestring import mark_safe
import json

def index(request):
    return render(request, 'chat/index.html', {})
