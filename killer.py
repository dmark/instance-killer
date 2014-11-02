import sys
import datetime
import time
import boto.ec2

a = sys.argv

print "Searching for instances greater than %s hour(s) old" % (a[1])

now = int(time.time())

delta = datetime.timedelta(hours=int(a[1])).total_seconds()

ec2 = boto.ec2.connect_to_region("eu-west-1")

reservations = ec2.get_all_reservations()

reservations = ec2.get_all_reservations()

for r in reservations:
    for i in r.instances:
    	 t = time.mktime(datetime.datetime.strptime(i.launch_time, '%Y-%m-%dT%H:%M:%S.000Z').timetuple())
         if (now - t) > delta:
             print "Killing %s" % (i.id)
        
   

