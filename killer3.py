# killer3.py - boto3-based version of the killer.py script.

# Add the ability to specify which AWS CLI profile you want to use. You must
# specify the '-y' option to actually terminate instances.

import argparse

from boto3 import session, ec2
from datetime import tzinfo, timedelta, datetime
from pprint import PrettyPrinter

ZERO = timedelta(0)
HOUR = timedelta(hours=1)

# A UTC class.
class UTC(tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO

utc = UTC()

pp = PrettyPrinter(indent=4)

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--terminate", type=int, help="Terminate instances older than this many hours", default=72)
parser.add_argument("-w", "--warn", type=int, help="Warn about any instances older than this many hours", default=36)
parser.add_argument("-p", "--profile", help="The awscli profile name you wish to use", default="default")
parser.add_argument("-r", "--region", help="The AWS region you want to interact with", default="us-east-1")
parser.add_argument("-y", "--yes", help="Terminate all instances older than the specified termination time", action="store_true")
args = parser.parse_args()

now = datetime.now(utc)
delta_kill = now - timedelta(hours=args.terminate)
delta_warn = now - timedelta(hours=args.warn)

session = session.Session(region_name=args.region, profile_name=args.profile)
ec2 = session.client('ec2')
response = ec2.describe_instances()

warn_instances = []
for reservation in response[u'Reservations']:
    for instance in reservation[u'Instances']:
        launchtime = instance[u'LaunchTime']
        if launchtime < delta_kill and args.yes:
            print "Terminating instance", instance[u'InstanceId']
            #ec2.terminate_instances(InstanceIds=[instance[u'InstanceId']])
        elif launchtime < delta_kill and not args.yes:
            print "Skipping instance", instance[u'InstanceId']
        elif launchtime < delta_warn:
            warn_instances += instance

if warn_instances:
    print "The following instances are more than ", args.warn, "hrs old."
    pp.pprint(warn_instances)
