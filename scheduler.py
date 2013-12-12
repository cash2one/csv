# -*- encoding: utf-8 -*-

from datetime import datetime

from apscheduler.scheduler import Scheduler

import ConfigParser
config = ConfigParser.ConfigParser()
config.read('config.ini')
interval = config.get('info','INTERVAL')#读取配置文件时间值
INTERVAL = int(interval)

# import logging
# import logging.handlers
# import logging.config
# logging.config.fileConfig('logging.ini')
# log = logging.getLogger(__file__)

from globfile import glob_dir
class Controler:

    def __init__(self):
        '''

        '''
        # self.mailsend = MailSend()
    def loop(self):
        self.sched = Scheduler(daemonic = False)
        self.sched.add_interval_job(lambda:glob_dir(),seconds=INTERVAL)
        print('Tick! The time is: %s' % datetime.now())
        self.sched.start()
if __name__ == '__main__':
    contr = Controler()
    contr.loop()
