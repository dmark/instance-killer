#!/bin/sh

list=`aws ec2 describe-instances --region eu-west-1 | jsawk 'return this.Reservations' | jsawk 'return this.Instances[0]' | jsawk -n 'out(this.InstanceId + "+" + this.LaunchTime + "+" + this.SubnetId + "+" + this.PrivateIpAddress)'`

for i in $list
do
	IFS='+' read -a array <<< "$i"
        killlimit=`date -d "$1 hours ago" +%s`
        warnlimit=`date -d "$2 hours ago" +%s`
	launch=${array[1]/T/\ };
        launch=`date --utc --date "$launch" +%s`
	declare -A warn
	declare -A kill

       if [ "$launch" -lt "$warnlimit" ] && [ "$launch" -gt "$killlimit" ]
           then

                n=`aws ec2 describe-instances --region eu-west-1 --instance-ids ${array[0]} | jsawk 'return this.Reservations[0].Instances[0]' | jsawk 'return this.Tags[0].Value'`
		warn["${array[0]}"]='{"InstanceId":"'"${array[0]}"'","LaunchTime":"'"${array[1]}"'","SubnetId":"'"${array[2]}"'","PrivateIpAddress":"'"${array[3]}"'","Name":"'"$n"'"}'

        fi

        if [ "$launch" -lt "$killlimit" ]
	   then

        	n=`aws ec2 describe-instances --region eu-west-1 --instance-ids ${array[0]} | jsawk 'return this.Reservations[0].Instances[0]' | jsawk 'return this.Tags[0].Value'`
		kill["${array[0]}"]='{"InstanceId":"'"${array[0]}"'","LaunchTime":"'"${array[1]}"'","SubnetId":"'"${array[2]}"'","PrivateIpAddress":"'"${array[3]}"'","Name":"'"$n"'"}'
	fi
	
done

echo '####################'
echo "Instances on warning"
echo '####################'
for x in "${warn[@]}"
do
   :
   echo '~~~~~~~~~~~~~~~';
   echo $x | jsawk -n 'out(this.InstanceId+"\n"+this.LaunchTime+"\n"+this.SubnetId+"\n"+this.PrivateIpAddress+"\n"+this.Name)'
   echo '~~~~~~~~~~~~~~~';
done

echo '####################'
echo "Instances killed"
echo '####################'
for x in "${kill[@]}"
do
   :
   echo '~~~~~~~~~~~~~~~';
   echo $x | jsawk -n 'out(this.InstanceId+"\n"+this.LaunchTime+"\n"+this.SubnetId+"\n"+this.PrivateIpAddress+"\n"+this.Name)'
   echo '~~~~~~~~~~~~~~~';
done


