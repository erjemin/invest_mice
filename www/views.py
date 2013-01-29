# -*- coding: utf-8 -*-
# Включили поддержку UTF-8 в Python. Без этого даже комментарии на русском языке нельзя писать.

from django.http import HttpResponse, Http404
import random
import datetime
import time


def hello ( request ) :
    return HttpResponse ( "Hello world! Привет питон!")
