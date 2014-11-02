# Instance Killer

Bash and Python script to kill Amazon EC2 instances based on elapsed time since launch. Allows for warnings and dry runs. Use with care.

***TERMINATE EXECUTABLE NEEDS TO BE UNCOMMENTED IN THE SCRIPTS***

## Python

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

