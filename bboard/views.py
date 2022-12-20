import json
import requests
import lxml

from django.http import HttpResponse
from .predict import predict, get_forecast1
from bs4 import BeautifulSoup


def predict1(request, stockname):
    print(stockname)
    from1 = request.GET['from']
    to = request.GET['to']
    l = predict(from1, to, stockname)
    return HttpResponse(json.dumps(l), content_type="application/json")


def stock(request, stockname):
    from1 = request.GET['from']
    to = request.GET['to']
    stock = get_forecast1(from1, to, stockname)
    return HttpResponse(json.dumps(stock), content_type="application/json")


def allstock(request):
    url = 'https://finance.yahoo.com/lookup'
    contets = requests.get(url).text
    soup = BeautifulSoup(contets)
    l = []
    for row in soup.body.div.tbody.children:
        stock_name = row.td.a.text
        stock_price = list(row.children)[2].text
        if ':' not in stock_name:
            l.append({'stockName': stock_name, 'currentPrice': stock_price})
    return HttpResponse(json.dumps(l), content_type="application/json")
