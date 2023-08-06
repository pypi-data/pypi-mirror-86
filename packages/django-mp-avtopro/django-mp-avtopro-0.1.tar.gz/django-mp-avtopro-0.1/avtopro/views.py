# -*- encoding: utf-8 -*-

import xlwt

from django.apps import apps
from django.shortcuts import HttpResponse


def export_to_avtopro(request):

    response = HttpResponse(content_type='application/ms-excel')

    response['Content-Disposition'] = 'attachment; filename="products.xls"'

    wb = xlwt.Workbook(encoding='utf-8')

    ws = wb.add_sheet('Products')

    row_number = 0

    columns = [
        u'Производитель',
        u'Цена USD входящая',
        u'Наличие',
        u'Код',
        u'Описание',
        u'Фото',
        u'Б/У'
    ]

    for i, col in enumerate(columns):
        ws.write(row_number, i, col)

    qs = apps.get_model('products', 'Product')\
        .objects\
        .visible()\
        .available()\
        .select_related('manufacturer')\
        .prefetch_related('images')

    host = '{}://{}'.format(request.scheme, request.META['HTTP_HOST'])

    for product in qs:

        row_number += 1

        row = [
            product.manufacturer.name if product.manufacturer else '',
            product.price_usd,
            '1',
            product.code,
            product.description,
            ', '.join([host + i.file.url for i in product.images.all()]),
            u'Нет' if product.is_new else u'Да'
        ]

        for i, item in enumerate(row):
            ws.write(row_number, i, item)

    wb.save(response)

    return response
