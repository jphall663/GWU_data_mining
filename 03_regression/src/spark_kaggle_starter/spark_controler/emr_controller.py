import boto3
import botocore
import time
import logging
import os
from datetime import datetime
import tarfile
# https://medium.com/@datitran/quickstart-pyspark-with-anaconda-on-aws-660252b88c9a

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class EMRController(object):
    def __init__(self, profile_name = 'default', aws_access_key = False, aws_secret_access_key = False, region_name = 'us-east-1',
                 cluster_name = 'Spark-Cluster', instance_count = 3, master_instance_type = 'm3.xlarge', slave_instance_type = 'm3.xlarge',
                 key_name = 'EMR_Key', subnet_id = 'subnet-50c2a327', software_version = 'emr-5.5.0', s3_bucket = 'emr-related-files', path_script =os.path.dirname( __file__ ),
                 additional_job_args=['--packages', 'ai.h2o:sparkling-water-core_2.11:2.1.7', '--conf', 'spark.dynamicAllocation.enabled=false'] ):
        self.init_datetime_string = self.get_datetime_str()                     #Used to create a s3 directory so multiple scripts don't overwrite the same files

        self.aws_access_key = aws_access_key                                    #If you don't wan to use a credential from the AWS CLI on your machine set this
        self.aws_secret_access_key = aws_secret_access_key                      #If you don't wan to use a credential from the AWS CLI on your machine set this
        self.region_name = region_name                                          #AWS region to run the cluster in i.e. 'us-east-1'
        self.cluster_name = cluster_name+'_'+self.init_datetime_string          # Application Name on EMR
        self.instance_count = instance_count                                    #Total number of instances
        self.master_instance_type = master_instance_type                        # EC2 intance type for the master node(s)
        self.slave_instance_type = slave_instance_type                          # EC2 instance type for the worker nodes
        self.key_name = key_name                                                #Your ssh key used to ssh into the master node. i.e. 'My_KEY'
        self.subnet_id = subnet_id                                              #The Subnet on AWS for the cluster
        self.software_version = software_version                                #Elastic Map Reduce Version
        self.profile_name = profile_name                                        # Define IAM profile name (see: http://boto3.readthedocs.io/en/latest/guide/configuration.html)(config file located at user folder .aws directory)
        self.s3_bucket = s3_bucket                                              # S3 Bucket to use for storage
        self.path_script = path_script                                          #The path to your python script. If you are running /user/me/script.py set this to '/user/me'. If you are importing this from the same dir leave it default
        self.file_to_run = 'test.py'                                            # The file you want to run from the compressed files
        self.job_flow_id = None                                                 # AWS's unique ID for an EMR Cluster exameple: 'j-17LA5TIOEEEU3'
        self.additional_job_args = additional_job_args                          #Additional args for submitting an application to cluster


    def boto_client(self, service):
        """
        This will return a boto_client set the service i.e. 'emr' or 's3'.
        :return: boto3.client
        """
        if self.aws_access_key and self.aws_secret_access_key:
            client = boto3.client(service,
                                  aws_access_key_id=self.aws_access_key,
                                  aws_secret_access_key=self.aws_secret_access_key,
                                  region_name=self.region_name)
            return client
        else:
            session = boto3.Session(profile_name=self.profile_name)
            return session.client(service, region_name=self.region_name)

    def load_cluster(self):
        """
        Spins up a cluster on AWS EMR.

        :return: the response object from boto
        """
        response = self.boto_client("emr").run_job_flow(
            Name=self.cluster_name,
            LogUri='s3://'+self.s3_bucket+'/logs',
            ReleaseLabel=self.software_version,
            Instances={
                'MasterInstanceType': self.master_instance_type,
                'SlaveInstanceType': self.slave_instance_type,
                'InstanceCount': self.instance_count,
                'KeepJobFlowAliveWhenNoSteps': True,
                'TerminationProtected': False,
                'Ec2KeyName': self.key_name,
                'Ec2SubnetId': self.subnet_id
            },
            Applications=[
                {
                    'Name': 'Spark'
                },
                {
                    'Name': 'Hadoop'
                }
            ],
            BootstrapActions=[
                {
                    'Name': 'Install Conda',
                    'ScriptBootstrapAction': {
                        'Path': 's3://{s3_bucket}/temp/{init_datetime_string}/bootstrap_actions.sh'.format(
                            s3_bucket=self.s3_bucket,init_datetime_string=self.init_datetime_string),
                    }
                },
                # UNCOMMENT FOR AUTOTERMINATE BEHAVIOR
                # {
                #     'Name': 'idle timeout',
                #     'ScriptBootstrapAction': {
                #         'Path':'s3n://{}/{}/terminate_idle_cluster.sh'.format(self.s3_bucket + '/' + self.s3_path_temp_files, self.job_name),
                #         'Args': ['3600', '300']
                #     }
                # },
            ],
            Configurations=[
            #     {
            #         'Classification': 'spark-env',
            #         'Configurations': [
            #             {
            #                 "Classification": "export",
            #                 "Properties": {
            #                     "PYSPARK_PYTHON": "python34",
            #                     "PYSPARK_PYTHON": "/home/hadoop/conda/bin/python",
            #                     "PYSPARK_DRIVER_PYTHON":"/home/hadoop/conda/bin/python"
            #                 },
            #                 "Configurations": []
            #             }
            #         ],
            #         'Properties': {
            #         }
            #     },
            #     {
            #         "Classification": "hadoop-env",
            #         "Properties": {
            #
            #         },
            #         "Configurations": [
            #           {
            #             "Classification": "export",
            #             "Properties": {
            #               "HADOOP_DATANODE_HEAPSIZE": "2048",
            #               "HADOOP_NAMENODE_OPTS": "-XX:GCTimeRatio=19"
            #             },
            #             "Configurations": [
            #
            #             ]
            #           }
            #         ]
            #   },
              {
                  "Classification": "hadoop-env",
                  "Properties": {

                  },
                  "Configurations": [
                    {
                      "Classification": "export",
                      "Properties": {
                          "PYTHONHASHSEED": "123", #This is required for pyspark so all nodes have the same seed
                      },
                      "Configurations": [

                      ]
                    }
                  ]
            }
            ],
            VisibleToAllUsers=True,
            JobFlowRole='EMR_EC2_DefaultRole',
            ServiceRole='EMR_DefaultRole'
        )
        logger.info(response)
        return response

    def add_create_step(self, job_flow_id, master_dns):
        """
        This step has to be run directly after the bootstrapping to ensure that
        conda has been properly linked to the spark environment.

        :param string job_flow_id: The clusters id example: j-17LA5TIOEEEU3
        :param string master_dns: the dns address of the master node
        :return: the response object from boto3
        """
        response = self.boto_client("emr").add_job_flow_steps(
            JobFlowId=job_flow_id,
            Steps=[
                {
                    'Name': 'setup - copy files',
                    'ActionOnFailure': 'CANCEL_AND_WAIT',
                    'HadoopJarStep': {
                        'Jar': 'command-runner.jar',
                        'Args': ['aws', 's3', 'cp',
                                 's3://{s3_bucket}/temp/{init_datetime_string}/pyspark_quick_setup.sh'.format(
                                     s3_bucket=self.s3_bucket,init_datetime_string=self.init_datetime_string),
                                 '/home/hadoop/']
                    }
                },
                {
                    'Name': 'setup pyspark with conda',
                    'ActionOnFailure': 'CANCEL_AND_WAIT',
                    'HadoopJarStep': {
                        'Jar': 'command-runner.jar',
                        'Args': ['sudo', 'bash', '/home/hadoop/pyspark_quick_setup.sh', master_dns]
                    }
                }
            ]
        )
        logger.info(response)
        return response

    def add_spark_submit_step(self, job_flow_id,name_of_script_directory):
        """
        Steps for EMR to upload the python files and run them as a spark-submit
        on the cluster.
        First it uploads the .tar file, then decompresses it, then spark-submits
        it.

        :param string job_flow_id: The clusters id example: j-17LA5TIOEEEU3
        :param string name_of_script_directory: the name of the directory to hold scripts on s3 and master node. The file/directory holding the file should be a unique id to prevent overwritting
        :return: the response object from boto
        """

        args = []
        args.append('spark-submit')
        if self.additional_job_args:
            for arg in self.additional_job_args:
                args.append(arg)
        args.append("/home/hadoop/scripts/" + name_of_script_directory + '/' + self.file_to_run)

        response = self.boto_client("emr").add_job_flow_steps(
            JobFlowId=job_flow_id,
            Steps=[
                {
                    'Name': 'Copy_Tar',
                    'ActionOnFailure': 'CANCEL_AND_WAIT',
                    'HadoopJarStep': {
                        'Jar': 'command-runner.jar',
                        'Args': ['aws', 's3', 'cp',
                                 's3://{s3_bucket}/temp/{name_of_script_directory}/script.tar.gz'.format(
                                     s3_bucket=self.s3_bucket,name_of_script_directory=name_of_script_directory),
                                 '/home/hadoop/scripts/' + name_of_script_directory + '/']
                    }
                },
                {
                    'Name': 'Decompress script.tar.gz',
                    'ActionOnFailure': 'CANCEL_AND_WAIT',
                    'HadoopJarStep': {
                        'Jar': 'command-runner.jar',
                        'Args': ['tar', 'zxvf', '/home/hadoop/scripts/' + name_of_script_directory + '/script.tar.gz','-C','/home/hadoop/scripts/'+ name_of_script_directory]
                    }
                },
                {
                    'Name': 'Spark Application',
                    'ActionOnFailure': 'CONTINUE',
                    'HadoopJarStep': {
                        'Jar': 'command-runner.jar',
                        'Args': args
                    }
                }
            ]
        )
        logger.info(response)
        time.sleep(1)
        return response

    def create_bucket_on_s3(self, bucket_name):
        """
        Checks to see if the bucket exists if not it will create one by that
        name.

        :param string bucket_name: name of the s3 bucket to store all data from cluster
        """
        s3 = self.boto_client("s3")
        try:
            logger.info("Bucket already exists.")
            s3.head_bucket(Bucket=bucket_name)
        except botocore.exceptions.ClientError as e:
            logger.info("Bucket does not exist: {error}. I will create it!".format(error=e))
            s3.create_bucket(Bucket=bucket_name)

    def upload_to_s3(self, path_to_file, bucket_name, path_on_s3):
        """
        Uploads a file to s3.

        :param string path_to_file: The path of the file on local to upload.
        :param string bucket_name: The name of the s3 bucket
        :param string path_on_s3: The path and file it should be called on s3.
        """
        logger.info(
            "Upload file '{file_name}' to bucket '{bucket_name}'".format(file_name=path_on_s3, bucket_name=bucket_name))
        s3 = None
        if self.aws_access_key and self.aws_secret_access_key:
            s3 = self.boto_client("s3")
            s3.upload_file(path_to_file, bucket_name, path_on_s3)
        else:
            s3 = boto3.Session(profile_name=self.profile_name).resource('s3')
            s3.Object(bucket_name, path_on_s3)\
              .put(Body=open(path_to_file, 'rb'), ContentType='text/x-sh')





    def get_datetime_str(self):
        """
        Gets a formated datetime string for naming purposes.
        """
        return datetime.now().strftime("%Y%m%d.%H:%M:%S.%f")

    def generate_job_name(self):
        """
        Generates a Job name Key for referencing the EMR cluster on the AWS
        Console and through logs.
        """
        self.job_name = "{}.{}.{}".format(self.app_name,
                                          self.user,
                                          self.get_datetime_str())

    def tar_python_script(self):
        """
        Compresses a tar file and saves it.
        :return:
        """
        # Create tar.gz file
        t_file = tarfile.open(os.path.dirname( __file__ )+"/files/script.tar.gz", 'w:gz')
        # Add Spark script path to tar.gz file
        files = os.listdir(self.path_script)
        for f in files:
            t_file.add(self.path_script + '/' + f, arcname=f)
        # List all files in tar.gz
        for f in t_file.getnames():
            logger.info("Added %s to tar-file" % f)
        t_file.close()

    def remove_temp_files(self, s3):
        """
        Remove Spark files from temporary bucket. NOT FINISHED TODO

        :param s3:
        :return:
        """
        bucket = s3.Bucket(self.s3_bucket)
        for key in bucket.objects.all():
            if key.key.startswith(self.job_name) is True:
                key.delete()
                logger.info("Removed '{}' from bucket for temporary files".format(key.key))

    def run(self,execute_type='create'):
        """
        This will run the execution of the program. Call this after vars are set.

        :param string execute_type: Used to either create a cluster or submit a job. Accepted: 'create' or 'run_job'
        """
        if execute_type == 'create':
            logger.info(
                "*******************************************+**********************************************************")
            logger.info("Load config and set up client.")

            logger.info(
                "*******************************************+**********************************************************")
            logger.info("Check if bucket exists otherwise create it and upload files to S3.")
            self.create_bucket_on_s3(bucket_name=self.s3_bucket)
            self.upload_to_s3(os.path.dirname( __file__ )+"/scripts/bootstrap_actions.sh", bucket_name=self.s3_bucket,
                                    path_on_s3="temp/"+self.init_datetime_string+"/bootstrap_actions.sh")
            self.upload_to_s3(os.path.dirname( __file__ )+"/scripts/pyspark_quick_setup.sh", bucket_name=self.s3_bucket,
                                    path_on_s3="temp/"+self.init_datetime_string+"/pyspark_quick_setup.sh")
            self.upload_to_s3(os.path.dirname( __file__ )+"/scripts/terminate_idle_cluster.sh", bucket_name=self.s3_bucket,
                                    path_on_s3="temp/"+self.init_datetime_string+"/terminate_idle_cluster.sh")

            logger.info(
                "*******************************************+**********************************************************")
            logger.info("Create cluster and run boostrap.")
            emr_response = self.load_cluster()
            emr_client = self.boto_client("emr")
            self.job_flow_id = emr_response.get("JobFlowId")
            while True:
                job_response = emr_client.describe_cluster(
                    ClusterId=emr_response.get("JobFlowId")
                )
                time.sleep(10)
                if job_response.get("Cluster").get("MasterPublicDnsName") is not None:
                    master_dns = job_response.get("Cluster").get("MasterPublicDnsName")

                step = True

                job_state = job_response.get("Cluster").get("Status").get("State")
                job_state_reason = job_response.get("Cluster").get("Status").get("StateChangeReason").get("Message")

                if job_state in ["TERMINATING","TERMINATED","TERMINATED_WITH_ERRORS"]:
                    step = False
                    logger.info(
                        "Script stops with state: {job_state} "
                        "and reason: {job_state_reason}".format(job_state=job_state, job_state_reason=job_state_reason))
                    break
                elif job_state in ["WAITING","RUNNING"]:
                    step = True
                    break
                else: # BOOTSTRAPPING,STARTING
                    logger.info(job_response)

            if step:
                logger.info(
                    "*******************************************+**********************************************************")
                logger.info("Run steps.")
                add_step_response = self.add_create_step(emr_response.get("JobFlowId"), master_dns)

                while True:
                    list_steps_response = emr_client.list_steps(ClusterId=emr_response.get("JobFlowId"),
                                                                StepStates=["COMPLETED"])
                    time.sleep(10)
                    if len(list_steps_response.get("Steps")) == len(
                            add_step_response.get("StepIds")):  # make sure that all steps are completed
                        break
                    else:
                        logger.info(emr_client.list_steps(ClusterId=emr_response.get("JobFlowId")))
                return True
            else:
                logger.info("Cannot run steps.")
                return False
        elif execute_type == 'run_job':
            date_time_of_execute = 'test'#self.get_datetime_str()
            self.tar_python_script()
            self.upload_to_s3(os.path.dirname( __file__ )+'/files/script.tar.gz', bucket_name=self.s3_bucket,
                                    path_on_s3="temp/"+date_time_of_execute+"/script.tar.gz")
            self.add_spark_submit_step(self.job_flow_id,date_time_of_execute)
            return True
    def step_copy_data_between_s3_and_hdfs(self, c, src, dest):
        """
        Copy data between S3 and HDFS (not used for now)
        :param c: the boto_client
        :param src: source location of files
        :param dest: the destination on hdfs
        :return:
        """
        response = c.add_job_flow_steps(
            JobFlowId=self.job_flow_id,
            Steps=[{
                    'Name': 'Copy data from S3 to HDFS',
                    'ActionOnFailure': 'CANCEL_AND_WAIT',
                    'HadoopJarStep': {
                        'Jar': 'command-runner.jar',
                        'Args': [
                            "s3-dist-cp",
                            "--s3Endpoint=s3-eu-west-1.amazonaws.com",
                            "--src={}".format(src),
                            "--dest={}".format(dest)
                        ]
                    }
                }]
        )
        logger.info("Added step 'Copy data from {} to {}'".format(src, dest))
