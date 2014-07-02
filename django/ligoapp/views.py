# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response

def main_page(request):
<<<<<<< HEAD
    return render_to_response('index.html', {})
=======
    return HttpResponse('hello. this is test. exclude sparse-checkout test v2')
>>>>>>> 1bbd1a1df891eb4fff649433d76a597ba76ed335
