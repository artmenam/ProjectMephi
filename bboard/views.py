from django.http import HttpResponse

from .models import Bb
from .predict import predict, get_forecast1


def index(request):
    s = 'Список объявлений:\r\n\r\n\r\n'
    for bb in Bb.objects.order_by('-published'):
        s += bb.title + '\r\n' + bb.content + '\r\n\r\n'
    return HttpResponse(s, content_type='text/plain; charset=utf-8')


def predict1(request):
    from1 = request.GET['from']
    to = request.GET['to']
    s, y = predict(from1, to)
    k = 'Предсказание:\r\n\r\n\r\n'
    k += s + ' ' + str(y)
    return HttpResponse(k, content_type='text/plain; charset=utf-8')


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
