<h1> EMR Automation Controller </h1>

<b>Summary</b>: This package uses boto3 to interact with AWS's EMR service. It has two main functionalities. First, it will auto launch and bootstrap new EMR clusters. Second, it will auto run code on a cluster by compressing all python files in a directory and submitting them as a step on the cluster.

<h1>Code example</h1>

| Required parameters for creating a cluster: |
|---|
| profile_name: Define IAM profile name ('aws configure' cli command uses 'default')(see: http://boto3.readthedocs.io/en/latest/guide/configuration.html)  |
| subnet_id: The Subnet on AWS for the cluster (try launching a random new cluster and copying from the console page.) |
| key_name: Your ssh key used to ssh into the master node. i.e. 'My_KEY' |
| s3_bucket: An s3 staging bucket to store logs and temporary files. |
| master_instance_type: EC2 intance type for the master node(s) |
| slave_instance_type: EC2 instance type for the worker nodes |
| instance_count: Total number of instances (one will be master rest workers) |


| Required parameters for running a spark_submit step: |
|---|
| job_flow_id: AWS's unique ID for an EMR Cluster exameple: 'j-17LA5TIOEEEU3'. You can find this on the EMR console  |
| path_script: The path to your python script on local machine. If you are running /user/me/script.py set this to '/user/me'. If you are importing this from the same dir leave it default |
| file_to_run: The file you want to run from the compressed files. Or path to file if not in top directory. |
| additional_job_args: Set to false if you don't want any parameters |

<b>Code:</b>
```
import os
from emr_controller import EMRController
deployer = EMRController()
deployer.profile_name = 'default'
deployer.subnet_id = 'subnet-50c2a327'
deployer.key_name = 'EMR_Key'
deployer.s3_bucket = 'emr-related-files'
deployer.master_instance_type = 'm4.xlarge'
deployer.slave_instance_type = 'm4.xlarge'
deployer.instance_count = 2
deployer.run('create')
deployer.job_flow_id = 'j-7F2D0E3L1W1W'
deployer.path_script = os.path.dirname( __file__ )
deployer.file_to_run = 'test.py'
deployer.additional_job_args = ['--packages', 'ai.h2o:sparkling-water-core_2.11:2.1.7', '--conf', 'spark.dynamicAllocation.enabled=false']
deployer.run('run_job')
```


<b>Suggestion:</b> The bootstrapping action usually takes ~7-15minutes. Comment out the create step and go your console and copy your cluster id. Only run the run job function on the same cluster. This will also save costs as instance hours are rounded up so you always have to pay for one hour.

<b>Alternative Authentication</b> If you don't have access to aws cli configurations you can set the aws_access_key and aws_secret_access_key variables, which will override the profile_name variable.
