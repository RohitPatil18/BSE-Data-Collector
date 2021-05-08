import csv
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from .models import BhavCopyRecord

# Create your views here.
def index(request):
    return render(request, 'bhavcopy/index.html')


def fetch_records(request):
    search = request.GET.get('search')
    page = request.GET.get('page')
    page = int(page) if page else 1
    size = request.GET.get('size')
    size = int(size) if size else 15
    if search and search != '':
        records = BhavCopyRecord.find_all(search)
    else:
        # Record 50 records at a time
        records = BhavCopyRecord.paginate(page, size)
    return JsonResponse(records, safe=False)


def download_file(request):
    response = HttpResponse(content_type='text/csv')  
    response['Content-Disposition'] = 'attachment; filename="bhavcopy.csv"'  
    search = request.GET.get('search')
    if search and search != '':
        records = BhavCopyRecord.find_all(search)
    else:
        records = BhavCopyRecord.all()
    writer = csv.writer(response)  
    writer.writerow(BhavCopyRecord.Meta.fields)
    for rec in records: 
        # Building columns list dyanamically
        cols = [rec[i] for i in BhavCopyRecord.Meta.fields] 
        writer.writerow(cols)  
    return response  