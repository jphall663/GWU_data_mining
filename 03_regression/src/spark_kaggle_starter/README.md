<h1>Spark Kaggle Starter</h1> 
<b>Summary:</b> This code takes much of Patrick's code and upgrades it with Spark and Pysparkling functionality. Also included is an EMR automation tool for launching clusters and running code as well as a logging tool for logging plots and code from your cluster's environment. 
 
[spark_main.py:](spark_main.py) This file will run the data prep and training. If you would like to run this with a local installation of spark and pysparkling please remove all the lines with logging or make sure the LoggingController can access an S3 bucket from your local env. 
 
[emr_controler.py:](spark_controler/emr_controler.py) This file helps with spinning up an EC2 cluster and zipping up code and submitting it to spark for execution. See README in directory. See README in spark_controler directory. 
 
[LoggingController.py:](logging_lib/LoggingController.py) This class will log files and plots. See README in logging_lib directory. 
 
[MarkdownBuilder.py:](logging_lib/MarkdownBuilder.py) This class will takes logs and make them into a nice clean markdown file. See README in logging_lib directory. 
 
<b>Using the EMR Automation tool and loggin tool:</b> When using these tools you will need to download the aws command line interface (aws cli) and run aws configure and give it access credentials that can access S3 and EMR. My suggestion is to just make a user with Administration permissions to avoid confustion of policies and roles (create a group with that permission then a user and download credentials of the user). 
 
To install aws cli. On Windows find the .msi file on AWS (easy takes like a whole 2 seconds). For macOS either go through the annoying terminal commands OR install homebrew and type brew install awscli.  
 
After the aws cli is installed in terminal: 
 
`aws configure` 
 
Type in your access key and secret key from IAM user role. 
 
For region type `us-east-1` (or another region if you want to use it and know what you're doing). 
 
Leave the last field blank (just hit enter past it). 
 
Done. You have set up the 'default' profile. 
