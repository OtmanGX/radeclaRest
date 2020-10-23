from datetime import date

from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response

from core.models import Tournament, Membre
from radeclaRest.utils import StandardResultsSetPagination
from tournament.serializers import TournamentSerializer, TournamentLiteSerializer


class TournamentViewSet(viewsets.ModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    pagination_class = StandardResultsSetPagination
    filter_fields = '__all__'

    def list(self, request, *args, **kwargs):
        is_all = request.GET.get('all', None)
        if is_all:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = TournamentLiteSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return super().list(self, request, *args, **kwargs)


import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.lib import colors


def age_range(min_age, max_age):
    current = timezone.now()

    min_date = timezone.datetime(current.year - min_age, current.month, current.day)
    max_date = timezone.datetime(current.year - max_age, current.month, current.day)

    return max_date, min_date


def membre_data(sex='H', tournoi=None):
    ranges = ([7, 8], [9, 10], [11, 12], [13, 14], [15, 18], [12, 18], [40, 100], [1, 100])

    if tournoi:
        age_filter = lambda x: \
            Membre.objects.filter(date_naissance__range=age_range(x[0], x[1]), sexe=sex, tournaments__id=tournoi).values('nom')
    else:
        age_filter = lambda x: \
            Membre.objects.filter(date_naissance__range=age_range(x[0], x[1]), sexe=sex).values('nom')

    datas = [[i['nom'] for i in age_filter(e)] for e in ranges]
    print(datas)
    if sex == 'F':
        datas.append([i['nom'] for i in age_filter([1, 100])])
    max_length = len(max(datas, key=len))
    for data in datas:
        data.extend([''] * (max_length - len(data)))
    return datas


def some_view(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()
    sex = request.GET.get('sex', 'H')
    title = 'liste_initiale_' + sex
    # Create the PDF object, using the buffer as its "file."
    pdf = SimpleDocTemplate(
        buffer,
        pagesize=landscape(letter)
    )


    p = canvas.Canvas(buffer)
    lWidth, lHeight = letter

    p.setPageSize((lHeight, lWidth))

    tournoi = request.GET.get('tournoi', None)
    table_title = f'Inscription au tournoi ({sex})'
    if tournoi:
        table_title = f'{Tournament.objects.get(pk=int(tournoi)).name} ({sex})'
        data = membre_data(sex, int(tournoi))
    else:
        data = membre_data(sex)

    data = list(zip(*data))
    data.insert(0, [table_title])
    header = ['7-8 ans', '9-10 ans', '11-12 ans', '13-14 ans', '15-18 ans', 'double 12-18 ans','double vétérans +40 ans', 'double mixte']
    if sex == 'F':
        header.append('Simple Dames')
    data.insert(1, header)
    # data = [
    #     ['Dedicated Hosting', 'VPS Hosting', 'Sharing Hosting', 'Reseller Hosting'],
    #     ['€200/Month', '€100/Month', '€20/Month', '€50/Month'],
    #     ['Free Domain', 'Free Domain', 'Free Domain', 'Free Domain'],
    #     ['2GB DDR2', '20GB Disc Space', 'Unlimited Email', 'Unlimited Email'],
    #     ['2GB DDR2', '', '', '']
    # ]
    table = Table(data)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (len(data[1]), 0), colors.green),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),

        ('FONTNAME', (0, 0), (-1, 0), 'Courier-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),

        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),

        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),

        ('SPAN', (0, 0), (len(data[1])-1, 0)),
    ])
    table.setStyle(style)

    rowNumb = len(data)
    for i in range(1, rowNumb):
        if i % 2 == 0:
            bc = colors.burlywood
        else:
            bc = colors.beige

        ts = TableStyle(
            [('BACKGROUND', (0, i), (-1, i), bc),
             ('FONTSIZE', (0, i), (-1, i), 5),]
        )
        table.setStyle(ts)

    # 3) Add borders
    ts = TableStyle(
        [
            ('BOX', (0, 0), (-1, -1), 2, colors.black),

            ('LINEBEFORE', (2, 1), (2, -1), 2, colors.red),
            ('LINEABOVE', (0, 2), (-1, 2), 2, colors.green),

            ('GRID', (0, 1), (-1, -1), 2, colors.black),
        ]
    )

    table.setStyle(ts)

    elems = []
    elems.append(table)
    pdf.build(elems)
    # width = 600
    # height = 500
    # x = 10
    # y = lWidth - 100
    # table.wrapOn(p, width, height)
    # table.drawOn(p, x, y)

    # Close the PDF object cleanly, and we're done.
    # p.showPage()
    # p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=title + '.pdf')
