#!/usr/bin/python2.7
from crontab import CronTab as cron

cronuser='pi'

def addJob(time,cmd,cmnt="default comment"):
    my_cron = cron(user=cronuser)
    job = my_cron.new(command=cmd, user=cronuser, comment=cmnt)
    print job.minute.every(10)
    
    dup = my_cron.find_time(job.minute.every(10))
    dupe = my_cron.find_time(job.minute.every(5))
    print dup[0]
    print dupe[0]
    #my_cron.write()
    

if __name__ == "__main__":
    addJob("0800", "testcmd", "testcomment")
