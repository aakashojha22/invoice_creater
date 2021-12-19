import datetime
from io import BytesIO
from django.shortcuts import render

# Create your views here.

from io import StringIO

from django.views.decorators.csrf import csrf_exempt
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def invoice_pdf(request):
    if request.method == "POST":
        seller_name = request.POST.get('seller_name')
        seller_phone = request.POST.get('seller_phone')
        seller_address = request.POST.get('seller_address')
        buyer_name = request.POST.get('buyer_name')
        buyer_phone = request.POST.get('buyer_phone')
        buyer_address = request.POST.get('buyer_address')
        count = int(request.POST.get('count'))

        template = get_template('sample_template_pdf.html')
        dic = {}
        total_amt = 0
        for a in range(0, count + 1):

            a1 = {}
            try:

                if request.POST.get('item{}'.format(a)):
                    a1['item'] = request.POST.get('item{}'.format(a))

                if request.POST.get('price{}'.format(a)):
                    a1['price'] = int(request.POST.get('price{}'.format(a)))

                if request.POST.get('tax{}'.format(a)):
                    a1['tax'] = int(request.POST.get('tax{}'.format(a)))

                if request.POST.get('quantity{}'.format(a)):
                    a1['quantity'] = int(request.POST.get('quantity{}'.format(a)))
                tax_value = (float(a1['price'] / 100)) * a1['tax']
                a1['total'] = int((a1['price'] + tax_value) * a1['quantity'])
                total_amt = total_amt + a1['total']
                dic[a] = a1
            except:
                pass

        context = {
            'seller_name': seller_name,
            'seller_phone': seller_phone,
            'seller_address': seller_address,
            'buyer_name': buyer_name,
            'buyer_phone': buyer_phone,
            'buyer_address': buyer_address,
            'dic': dic,
            'date': datetime.datetime.now(),
            'count': count + 1,
            'total_amt': total_amt
        }
        print(dic)
        html = template.render(context)
        pdf = render_to_pdf('sample_template_pdf.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "invoice.pdf"
            content = "'%cs'"
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % filename
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Error")

    else:
        return render(request, 'index_form.html')


@csrf_exempt
def api_invoice_pdf(request):
    if request.method == "POST":
        seller_name = request.POST.get('seller_name')
        seller_phone = request.POST.get('seller_phone')
        seller_address = request.POST.get('seller_address')
        buyer_name = request.POST.get('buyer_name')
        buyer_phone = request.POST.get('buyer_phone')
        buyer_address = request.POST.get('buyer_address')
        count = int(request.POST.get('count'))

        template = get_template('sample_template_pdf.html')
        dic = {}
        total_amt = 0
        for a in range(0, count + 1):

            a1 = {}
            try:

                if request.POST.get('item{}'.format(a)):
                    a1['item'] = request.POST.get('item{}'.format(a))

                if request.POST.get('price{}'.format(a)):
                    a1['price'] = int(request.POST.get('price{}'.format(a)))

                if request.POST.get('tax{}'.format(a)):
                    a1['tax'] = int(request.POST.get('tax{}'.format(a)))

                if request.POST.get('quantity{}'.format(a)):
                    a1['quantity'] = int(request.POST.get('quantity{}'.format(a)))
                tax_value = (float(a1['price'] / 100)) * a1['tax']
                a1['total'] = int((a1['price'] + tax_value) * a1['quantity'])
                total_amt = total_amt + a1['total']
                dic[a] = a1
            except:
                pass

        context = {
            'seller_name': seller_name,
            'seller_phone': seller_phone,
            'seller_address': seller_address,
            'buyer_name': buyer_name,
            'buyer_phone': buyer_phone,
            'buyer_address': buyer_address,
            'dic': dic,
            'date': datetime.datetime.now(),
            'count': count + 1,
            'total_amt': total_amt
        }
        print(dic)
        html = template.render(context)
        pdf = render_to_pdf('sample_template_pdf.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "invoice.pdf"
            content = "'%cs'"
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % filename
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Error")

    else:
        return render(request, 'index_form.html')


