# Instance Killer

Bash and Python script to kill Amazon EC2 instances based on elapsed time since launch. Allows for warnings and dry runs. Use with care.

***TERMINATE EXECUTABLE NEEDS TO BE UNCOMMENTED IN THE SCRIPTS***

## Python + boto3

The script `killer3.py` is a boto3-based version of the killer.py script. The boto3 version adds the ability to specify an AWS CLI profile to use for authentication. Also the script requires that you specify the `-y` or `--yes` argument to terminate instances. Otherwise it does not make any changes. Like the previous script, the actual line to terminate the instance is commented out. This is a dangerous script! Use wisely and at your own risk.

## Python + boto2

Requirements:

You need Amazon CLI boto module

`pip install boto`

https://github.com/boto/boto

Usage:

`python killer.py <terminate interval> <warn interval> <region> [dry-run]`

eg

`python killer.py 72 48 eu-west-1`

or

`python killer.py 72 48 eu-west-1 dry-run` to test before running

Amazon CLI environment set in ~/.boto



## Bash

Requirements:

jsawk
https://github.com/micha/jsawk

Spidermonkey js interpreter
https://developer.mozilla.org/en-US/docs/Mozilla/Projects/SpiderMonkey

Usage:

`./killer.sh <terminate interval> <warn interval>`

eg

`./killer.sh 72 48`

Amazon CLI environment variables must be set as normal for use with Amazon CLI
