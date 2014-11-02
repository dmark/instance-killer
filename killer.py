import sys
import datetime
import time
import boto.ec2

#VARIABLES
dry_run = False

#GET COMMAND LINE ARGUMENTS
a = sys.argv

if len(a) < 4:
    print"Usage: python killer.py <terminate interval> <warn interval> <region> [dry-run]"
    sys.exit()

if 4 < len(a):
    print "###DRY RUN####"
    dry_run = True
    
print "Searching for instances"
print "Killing older than %s hour(s) old; Warning older than %s hour(s) old" % (a[1],a[2])

now = int(time.time())

#CALCULATE SECONDS FOR INTERVALS
delta_kill = datetime.timedelta(hours=int(a[1])).total_seconds()

delta_warn = datetime.timedelta(hours=int(a[2])).total_seconds()

#CONNECT TO REGION AS ARGUMENT 3
ec2 = boto.ec2.connect_to_region(a[3])

#PROCESS
reservations = ec2.get_all_reservations()

for r in reservations:
    for i in r.instances:
    	 t = time.mktime(datetime.datetime.strptime(i.launch_time, '%Y-%m-%dT%H:%M:%S.000Z').timetuple())
         if (now - t) > delta_kill:
             print "Kill %s" % (i.id)
             if dry_run == False:
                 print "Killing now..."
                 #ec2.terminate_instances(instance_ids=[i.id])
         elif (now - t) > delta_warn:
             print "Warning %s" % (i.id)
         else:
             print "OK %s" % (i.id)
         	 
            	    
        
   

