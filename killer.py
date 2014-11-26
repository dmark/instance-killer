import sys
import datetime
import time
import boto.ec2
import smtplib
from email.mime.text import MIMEText

#GET COMMAND LINE ARGUMENTS
a = sys.argv

#MAIL
sender = 'aws.build@mttnow.com'
if a[-1] == "dry-run":
    receivers = [a[-2]]
else:
    receivers = [a[-1]]

message = "Subject: Auto-termination of AWS Build instances\n\n"

#VARIABLES
dry_run = False

#EXEMPTED SUBNETS
exempt = ["subnet-738e8e35","subnet-58f7aa1e","subnet-59f7aa1f","subnet-81c414e4","subnet-7037cf07","subnet-733de516","subnet-fa7fdf9f","subnet-c77cbbb0","subnet-d6ff5fb3","subnet-1720d460"]

if len(a) < 4:
    print"Usage: python killer.py <terminate interval> <warn interval> <region> <email> [dry-run]"
    sys.exit()

if a[-1] == "dry-run":
    message += "###DRY RUN###\n\n"
    dry_run = True

message += "https://mttnow.atlassian.net/wiki/display/DEV/Auto-termination+of+instances\n\n"
    
message += "Terminating older than %s hour(s) old; Warning older than %s hour(s) old\n\n" % (a[1],a[2])

now = int(time.time())

#CALCULATE SECONDS FOR INTERVALS
delta_kill = datetime.timedelta(hours=int(a[1])).total_seconds()

delta_warn = datetime.timedelta(hours=int(a[2])).total_seconds()

#CONNECT TO REGION AS ARGUMENT 3
ec2 = boto.ec2.connect_to_region(a[3])

#PROCESS
reservations = ec2.get_all_reservations()

kill = []
warn = []
ok = []

for r in reservations:
    for i in r.instances:
    	 
    	 if i.subnet_id in exempt:
             continue
    	    
         if 'Name' in i.tags:
	     name = i.tags['Name']
         else:
             name = i.public_dns_name

    	 t = time.mktime(datetime.datetime.strptime(i.launch_time, '%Y-%m-%dT%H:%M:%S.000Z').timetuple())

         if (now - t) > delta_kill:
             kill.append("%s %s\n" % (i.id, name))
             if dry_run == False:
                 #print "Terminating %s %s..." % (i.id,name)
                 status = ec2.get_instance_attribute(i.id,"disableApiTermination")
                 if status["disableApiTermination"] == False:
                     #ec2.terminate_instances(instance_ids=[i.id])

         elif (now - t) > delta_warn:
             warn.append("%s %s\n" % (i.id,name))
         else:
             ok.append("%s %s\n" % (i.id,name))


message += "These instances have been terminated:\n"

for i in kill:
    message += i

message += "\n"

message += "Eligible for termination in 24 hours:\n"

for i in warn:
    message += i

message += "\n"

message += "These instances are OK:\n"

for i in ok:
    message += i

#SEND EMAIL
smtpObj = smtplib.SMTP('localhost')
smtpObj.sendmail(sender, receivers, message)         
#print "Successfully sent email"
