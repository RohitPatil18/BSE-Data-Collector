from celery import shared_task

from bhavcopy.services import BhavCopyScraper

@shared_task()
def download_bhavcopy_zip():
    ''' 
    Runs at scheduled time every day. Downloads and saves data in redis database
    '''
    BhavCopyScraper().scrape()
