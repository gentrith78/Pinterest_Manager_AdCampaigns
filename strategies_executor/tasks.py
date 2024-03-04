from __future__ import absolute_import, unicode_literals

from celery import shared_task

try:
    from .strategies_processor import process_strategies
except:
    from strategies_processor import process_strategies


@shared_task
def executor(interval):
   return process_strategies(interval)

if __name__ == '__main__':
    try:
        from .strategies_processor import process_strategies
    except:
        from strategies_processor import process_strategies
    process_strategies('EH')