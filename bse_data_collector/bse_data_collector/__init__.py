from __future__ import absolute_import
from bse_data_collector.celery import app as celery_worker

__all__ = ['celery_worker']