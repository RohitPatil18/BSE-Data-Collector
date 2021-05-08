from django.shortcuts import render
from django.http import JsonResponse

from .models import BhavCopyRecord

# Create your views here.
def index(request):
    return render(request, 'bhavcopy/index.html')


def fetch_records(request):
    search = request.GET.get('search')
    page = request.GET.get('page')
    page = int(page) if page else 1
    size = request.GET.get('size')
    size = int(size) if size else 50
    if search and search != '':
        records = BhavCopyRecord.find_all(search, paginate, page, size)
    else:
        # Record 50 records at a time
        records = BhavCopyRecord.paginate(page, size)
    return JsonResponse(records, safe=False)