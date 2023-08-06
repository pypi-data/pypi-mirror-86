# -*- coding: utf-8 -*-

import logging
import os
from datetime import datetime

from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.blocking import BlockingScheduler

from notejob.tasks.ba import watch_product

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='log1.txt',
                    filemode='a')


def my_job(id='my_job'):
    print(id, '-->', datetime.now())


job_stores = {
    # 'default': MemoryJobStore(),
    'default': SQLAlchemyJobStore(url='sqlite:///jobs-sqlite.db')
}

executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(10)
}

job_defaults = {
    'coalesce': False,
    'max_instances': 3
}


def my_listener(event):
    if event.exception:
        print('任务出错了！！！！！！')
    else:
        print('任务照常运行...')


scheduler = BlockingScheduler(
    jobstores=job_stores, executors=executors, job_defaults=job_defaults)
scheduler.add_job(watch_product,  'interval', seconds=120, args=['44434'])
scheduler.add_job(watch_product,  'interval', seconds=120, args=['44435'])

scheduler.add_job()

print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C    '))

try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    pass
