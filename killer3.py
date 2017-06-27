#!/usr/bin/env python2
# killer3.py - terminate long running EC2 instances

"""killer3.py

Terminates long running EC2 instances. The number of hours an instance must be
up before being terminated can be defined on the command line. The user must
explicitly pass the '-y' or '--yes' option before instances will be terminated.
Otherwise the script does not make any changes.
"""

from datetime import tzinfo, timedelta, datetime

ZERO = timedelta(0)
HOUR = timedelta(hours=1)

# A UTC class.
class UTC(tzinfo):
    """Creates a UTC instance of the tzinfo class"""

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO


def get_args():
    """Processes command line arguments"""
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--terminate", type=int,
                        help="Terminate instances older than this many hours (default 72)",
                        default=72)
    parser.add_argument("-w", "--warn", type=int,
                        help="Warn for any instances older than this many hours (default 36)",
                        default=36)
    parser.add_argument("-p", "--profile",
                        help="The awscli profile name you wish to use (default 'default')",
                        default="default")
    parser.add_argument("-r", "--region",
                        help="The AWS region you want to interact with (default us-east-1)",
                        default="us-east-1")
    parser.add_argument("-y", "--yes",
                        help="Terminate instances (default is 'do nothing')",
                        action="store_true")
    return(parser.parse_args())


def main():

    from boto3 import session, ec2
    from pprint import PrettyPrinter

    utc = UTC()
    pp = PrettyPrinter(indent=4)
    args = get_args()

    delta_kill = datetime.now(utc) - timedelta(hours=args.terminate)
    delta_warn = datetime.now(utc) - timedelta(hours=args.warn)

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


if __name__ == '__main__':
    main()
