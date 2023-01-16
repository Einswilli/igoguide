from django.contrib.auth import *
from django.views.decorators.csrf import csrf_exempt
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os