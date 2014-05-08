# -*- coding: utf-8 -*-
from django.http import HttpResponse

def main_page(request):
    return HttpResponse('hello. this is test. test.')
