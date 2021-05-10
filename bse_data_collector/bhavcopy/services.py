import os
import logging
import pandas as pd

from datetime import datetime, timedelta
from urllib import request
from urllib.error import HTTPError
from zipfile import ZipFile

from bse_data_collector.settings import BASE_DIR
from bhavcopy.models import BhavCopyRecord

logger = logging.getLogger(__name__)

class BhavCopyScraper:
    '''
    Scraper Service which collects the data from BSE India site and store it in Redis DB
    '''

    def __init__(self):
        print("Initializing scraper...")
        # Equity code is used to build url and identify and open datafile in zip
        self.equity_code = self._get_equity_code()

    def _get_equity_code(self):
        _date = datetime.today().strftime("%d%m%y")
        return f'EQ{_date}'

    def _download_file(self, zip_file_path):
        url = f'https://www.bseindia.com/download/BhavCopy/Equity/{self.equity_code}_CSV.ZIP'
        opener = request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        request.install_opener(opener)
        data = request.urlretrieve(url, zip_file_path)

    def save(self, df):
        '''
        Stores data in database 
        '''
        rec_date = datetime.today().strftime("%d-%m-%Y")
        for _, row in df.iterrows():
            rec = BhavCopyRecord(
                code=row['SC_CODE'], 
                name=row['SC_NAME'], 
                group=row['SC_GROUP'],
                sc_type=row['SC_TYPE'],
                open=row['OPEN'],
                high=row['HIGH'],
                low=row['LOW'],
                close=row['CLOSE'],
                last=row['LAST'],
                prevclose=row['PREVCLOSE'],
                no_trades=row['NO_TRADES'],
                no_of_shares=row['NO_OF_SHRS'], 
                net_turnover=row['NET_TURNOV'],
                record_date=rec_date
            )
            rec.create()

    def scrape(self):
        zip_file_path = os.path.join(BASE_DIR, 'tmp', 'bhavcopy.zip')
        try:
            self._download_file(zip_file_path)
            with ZipFile(zip_file_path, 'r') as _zip:
                filename = f'{self.equity_code}.CSV'
                f = _zip.open(filename)
                df = pd.read_csv(f)
                self.save(df)
                f.close()
        except HTTPError:
            logger.info('BSE did not publish any entries.')
        except Exception as e:
            logger.error(e)
