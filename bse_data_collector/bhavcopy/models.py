from django.db import models
from core.models import RedisModel

class BhavCopyRecord(RedisModel):
    class Meta:
        name = 'bhavcopy'
        fields = [
            'code', 
            'name', 
            'group',
            'sc_type',
            'open',
            'high',
            'low',
            'close',
            'last',
            'prevclose',
            'no_trades',
            'no_of_shares', 
            'net_turnover',
            'record_date'
        ]
        key_field = 'name'