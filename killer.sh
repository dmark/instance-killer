#!/bin/sh

list=`aws ec2 describe-instances | jsawk 'return this.Reservations' | jsawk 'return this.Instances[0]' | jsawk -n 'out(this.InstanceId + "+" + this.LaunchTime + "+" + this.SubnetId + "+" + this.PrivateIpAddress)'`

for i in $list
do
	IFS='+' read -a array <<< "$i"
        limit=`date -d "3 days ago" +%s`
        launch=`date --utc --date "${array[1]/T/\ }" +%s`
	echo $now
	echo $launch
	echo ${array[0]};
	echo ${array[1]/T/\ };
	echo ${array[2]};
	echo ${array[3]};
        n=`aws ec2 describe-instances --instance-ids ${array[0]} | jsawk 'return this.Reservations[0].Instances[0]' | jsawk 'return this.Tags[0].Value'`
	echo $n
done
