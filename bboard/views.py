import json

from django.http import HttpResponse, JsonResponse

from .models import Bb, pred
from .predict import predict
from .serializers import RubricSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.response import Response


def index(request):
    s = 'Список объявлений:\r\n\r\n\r\n'
    for bb in Bb.objects.order_by('-published'):
        s += bb.title + '\r\n' + bb.content + '\r\n\r\n'
    return HttpResponse(s, content_type='text/plain; charset=utf-8')


# @api_view(['GET'])
def predict1(request,stockname):
    print(stockname)
    from1 = request.GET['from']
    to = request.GET['to']
    l = predict(from1, to, stockname)
    print(l)
    return HttpResponse(json.dumps(l), content_type="application/json")



def stock(request):
    from1 = request.GET['from']
    to = request.GET['to']
    stock = get_forecast1(from1, to).values
    k = 'Date       Open       High       Low        Close      AdjClose\r\n'
    for i in stock:
        k += i[0] + ' ' + str("%.6f" % i[1]) + ' ' + str("%.6f" % i[2]) + ' ' + str("%.6f" % i[3]) + ' ' + str(
            "%.6f" % i[4]) + ' ' + str("%.6f" % i[5]) + '\r\n'
    print(k)
    return HttpResponse(k, content_type='text/plain; charset=utf-8')
