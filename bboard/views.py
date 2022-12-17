from django.http import HttpResponse

from .models import Bb
from .predict import predict

def index(request):
    s = 'Список объявлений:\r\n\r\n\r\n'
    for bb in Bb.objects.order_by('-published'):
        s += bb.title + '\r\n' + bb.content + '\r\n\r\n'
    return HttpResponse(s, content_type='text/plain; charset=utf-8')

def predict1(request):
    from1 = request.GET['from']
    to = request.GET['to']
    OUT_DIR = '../../data'
    s, y = predict(from1,to)
    return HttpResponse(s,y, content_type='text/plain; charset=utf-8')
