from django.shortcuts import render
from django.http import HttpResponse
def text(request):
    response = HttpResponse()
    response['Content-Disposition'] = 'attachment;filename=MP_verify_PuGkBdw2flZxu1Q4.txt'
    response.write('PuGkBdw2flZxu1Q4')
    return HttpResponse(response)
