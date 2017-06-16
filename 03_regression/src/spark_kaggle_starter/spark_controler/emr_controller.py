import boto3
import botocore
import time
import logging
import os
from datetime import datetime
import tarfile
# https://medium.com/@datitran/quickstart-pyspark-with-anaconda-on-aws-660252b88c9a

from spark_controler.ec2_instance_data_dict import ec2_data_dict


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class EMRController(object):
    def __init__(self, profile_name = 'default', aws_access_key = False, aws_secret_access_key = False, region_name = 'us-east-1',
                 cluster_name = 'Spark-Cluster', master_instance_count = 1,worker_instance_count = 3, master_instance_type = 'm3.xlarge', slave_instance_type = 'm3.xlarge',
                 key_name = 'EMR_Key', subnet_id = 'subnet-50c2a327', software_version = 'emr-5.5.0', s3_bucket = 'emr-related-files', path_script =os.path.dirname( __file__ ),
                 additional_job_args=['--packages', 'ai.h2o:sparkling-water-core_2.11:2.1.7', '--conf', 'spark.dynamicAllocation.enabled=false'], set_maxmimum_allocation=True, number_of_executors_per_node=1 ):
        self.init_datetime_string = self.get_datetime_str()                     # Used to create a s3 directory so multiple scripts don't overwrite the same files

        self.aws_access_key = aws_access_key                                    # If you don't wan to use a credential from the AWS CLI on your machine set this
        self.aws_secret_access_key = aws_secret_access_key                      # If you don't wan to use a credential from the AWS CLI on your machine set this
        self.region_name = region_name                                          # AWS region to run the cluster in i.e. 'us-east-1'
        self.cluster_name = cluster_name+'_'+self.init_datetime_string          # Application Name on EMR
        self.master_instance_count = master_instance_count                      # Number of master nodes to deploy
        self.worker_instance_count = worker_instance_count                      # Total number of worker instances
        self.master_instance_type = master_instance_type                        # EC2 intance type for the master node(s)
        self.slave_instance_type = slave_instance_type                          # EC2 instance type for the worker nodes
        self.key_name = key_name                                                # Your ssh key used to ssh into the master node. i.e. 'My_KEY'
        self.subnet_id = subnet_id                                              # The Subnet on AWS for the cluster
        self.software_version = software_version                                # Elastic Map Reduce Version
        self.profile_name = profile_name                                        # Define IAM profile name (see: http://boto3.readthedocs.io/en/latest/guide/configuration.html)(config file located at user folder .aws directory)
        self.s3_bucket = s3_bucket                                              # S3 Bucket to use for storage
        self.path_script = path_script                                          # The path to your python script. If you are running /user/me/script.py set this to '/user/me'. If you are importing this from the same dir leave it default
        self.file_to_run = 'test.py'                                            # The file you want to run from the compressed files
        self.job_flow_id = None                                                 # AWS's unique ID for an EMR Cluster exameple: 'j-17LA5TIOEEEU3'
        self.additional_job_args = additional_job_args                          # Additional args for submitting an application to cluster
        self.set_maxmimum_allocation = set_maxmimum_allocation                   # Calculates the maximum allocation in the cluster to use for the job then sets spark config properties boolean value: True or False
        self.number_of_executors_per_node = number_of_executors_per_node        # The number of executors per node (only used if set_maxmimum_alocation=True)

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

    def load_cluster(self, _spark_properties=False):
        """
        Spins up a cluster on AWS EMR.
        :param dict _spark_properties: A dict of any default spark properties to set on cluster
        :return: the response object from boto
        """
        spark_properties = {}
        if _spark_properties:
            spark_properties = _spark_properties

        response = self.boto_client("emr").run_job_flow(
            Name=self.cluster_name,
            LogUri='s3://'+self.s3_bucket+'/logs',
            ReleaseLabel=self.software_version,
            Instances={
                # 'MasterInstanceType': self.master_instance_type,
                # 'SlaveInstanceType': self.slave_instance_type,
                # 'InstanceCount': self.instance_count,
                'InstanceGroups': [
                    {
                        'Name': 'master(s)',
                        'Market': 'ON_DEMAND',#|'SPOT'
                        'InstanceRole': 'MASTER',#|'CORE'|'TASK'
                        # 'BidPrice': 'string',
                        'InstanceType': self.master_instance_type,
                        'InstanceCount': self.master_instance_count,
                        # 'Configurations': [
                        #     {
                        #         'Classification': 'string',
                        #         'Configurations': {'... recursive ...'},
                        #         'Properties': {
                        #             'string': 'string'
                        #         }
                        #     },
                        # ],
                        # 'EbsConfiguration': {
                        #     'EbsBlockDeviceConfigs': [
                        #         {
                        #             'VolumeSpecification': {
                        #                 'VolumeType': 'standard',#gp2, io1, standard
                        #                 # 'Iops': 123,
                        #                 'SizeInGB': 100
                        #             },
                        #             'VolumesPerInstance': 1
                        #         },
                        #     ],
                        #     'EbsOptimized': True#|False
                        # },
                        # 'AutoScalingPolicy': {
                        #     'Constraints': {
                        #         'MinCapacity': 123,
                        #         'MaxCapacity': 123
                        #     },
                        #     # 'Rules': [
                        #     #     {
                        #     #         'Name': 'string',
                        #     #         'Description': 'string',
                        #     #         'Action': {
                        #     #             'Market': 'ON_DEMAND'|'SPOT',
                        #     #             'SimpleScalingPolicyConfiguration': {
                        #     #                 'AdjustmentType': 'CHANGE_IN_CAPACITY'|'PERCENT_CHANGE_IN_CAPACITY'|'EXACT_CAPACITY',
                        #     #                 'ScalingAdjustment': 123,
                        #     #                 'CoolDown': 123
                        #     #             }
                        #     #         },
                        #     #
                        #     #         # 'Trigger': {
                        #     #         #     'CloudWatchAlarmDefinition': {
                        #     #         #         'ComparisonOperator': 'GREATER_THAN_OR_EQUAL'|'GREATER_THAN'|'LESS_THAN'|'LESS_THAN_OR_EQUAL',
                        #     #         #         'EvaluationPeriods': 123,
                        #     #         #         'MetricName': 'string',
                        #     #         #         'Namespace': 'string',
                        #     #         #         'Period': 123,
                        #     #         #         'Statistic': 'SAMPLE_COUNT'|'AVERAGE'|'SUM'|'MINIMUM'|'MAXIMUM',
                        #     #         #         'Threshold': 123.0,
                        #     #         #         'Unit': 'NONE'|'SECONDS'|'MICRO_SECONDS'|'MILLI_SECONDS'|'BYTES'|'KILO_BYTES'|'MEGA_BYTES'|'GIGA_BYTES'|'TERA_BYTES'|'BITS'|'KILO_BITS'|'MEGA_BITS'|'GIGA_BITS'|'TERA_BITS'|'PERCENT'|'COUNT'|'BYTES_PER_SECOND'|'KILO_BYTES_PER_SECOND'|'MEGA_BYTES_PER_SECOND'|'GIGA_BYTES_PER_SECOND'|'TERA_BYTES_PER_SECOND'|'BITS_PER_SECOND'|'KILO_BITS_PER_SECOND'|'MEGA_BITS_PER_SECOND'|'GIGA_BITS_PER_SECOND'|'TERA_BITS_PER_SECOND'|'COUNT_PER_SECOND',
                        #     #         #         'Dimensions': [
                        #     #         #             {
                        #     #         #                 'Key': 'string',
                        #     #         #                 'Value': 'string'
                        #     #         #             },
                        #     #         #         ]
                        #     #         #     }
                        #     #         # }
                        #     #
                        #     #     },
                        #     # ]
                        # }
                    },
                    {
                        'Name': 'slaves',
                        'Market': 'ON_DEMAND',#|'SPOT'
                        'InstanceRole': 'CORE',#|'MASTER'|'TASK'
                        # 'BidPrice': 'string',
                        'InstanceType': self.slave_instance_type,
                        'InstanceCount': self.worker_instance_count,
                        # 'Configurations': [
                        #     {
                        #         'Classification': 'string',
                        #         'Configurations': {'... recursive ...'},
                        #         'Properties': {
                        #             'string': 'string'
                        #         }
                        #     },
                        # ],
                        # 'EbsConfiguration': {
                        #     'EbsBlockDeviceConfigs': [
                        #         {
                        #             'VolumeSpecification': {
                        #                 'VolumeType': 'standard',#gp2, io1, standard
                        #                 # 'Iops': 123,
                        #                 'SizeInGB': 100
                        #             },
                        #             'VolumesPerInstance': 1
                        #         },
                        #     ],
                        #     'EbsOptimized': True#|False
                        # },
                        # 'AutoScalingPolicy': {
                        #     'Constraints': {
                        #         'MinCapacity': 123,
                        #         'MaxCapacity': 123
                        #     },
                        #     # 'Rules': [
                        #     #     {
                        #     #         'Name': 'string',
                        #     #         'Description': 'string',
                        #     #         'Action': {
                        #     #             'Market': 'ON_DEMAND'|'SPOT',
                        #     #             'SimpleScalingPolicyConfiguration': {
                        #     #                 'AdjustmentType': 'CHANGE_IN_CAPACITY'|'PERCENT_CHANGE_IN_CAPACITY'|'EXACT_CAPACITY',
                        #     #                 'ScalingAdjustment': 123,
                        #     #                 'CoolDown': 123
                        #     #             }
                        #     #         },
                        #     #
                        #     #         # 'Trigger': {
                        #     #         #     'CloudWatchAlarmDefinition': {
                        #     #         #         'ComparisonOperator': 'GREATER_THAN_OR_EQUAL'|'GREATER_THAN'|'LESS_THAN'|'LESS_THAN_OR_EQUAL',
                        #     #         #         'EvaluationPeriods': 123,
                        #     #         #         'MetricName': 'string',
                        #     #         #         'Namespace': 'string',
                        #     #         #         'Period': 123,
                        #     #         #         'Statistic': 'SAMPLE_COUNT'|'AVERAGE'|'SUM'|'MINIMUM'|'MAXIMUM',
                        #     #         #         'Threshold': 123.0,
                        #     #         #         'Unit': 'NONE'|'SECONDS'|'MICRO_SECONDS'|'MILLI_SECONDS'|'BYTES'|'KILO_BYTES'|'MEGA_BYTES'|'GIGA_BYTES'|'TERA_BYTES'|'BITS'|'KILO_BITS'|'MEGA_BITS'|'GIGA_BITS'|'TERA_BITS'|'PERCENT'|'COUNT'|'BYTES_PER_SECOND'|'KILO_BYTES_PER_SECOND'|'MEGA_BYTES_PER_SECOND'|'GIGA_BYTES_PER_SECOND'|'TERA_BYTES_PER_SECOND'|'BITS_PER_SECOND'|'KILO_BITS_PER_SECOND'|'MEGA_BITS_PER_SECOND'|'GIGA_BITS_PER_SECOND'|'TERA_BITS_PER_SECOND'|'COUNT_PER_SECOND',
                        #     #         #         'Dimensions': [
                        #     #         #             {
                        #     #         #                 'Key': 'string',
                        #     #         #                 'Value': 'string'
                        #     #         #             },
                        #     #         #         ]
                        #     #         #     }
                        #     #         # }
                        #     #
                        #     #     },
                        #     # ]
                        # }
                    },
                ],
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
                  "Classification": "hadoop-env", #set environment varaibles in here
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
            },
            # {
            #     "Classification": "spark",
            #     "Properties": {
            #       "maximizeResourceAllocation": "true", #AWS has problems with some instance types with this set (generates wrong spark settings, wtf AWS)
            #
            #     }
            # },
            {
              "Classification": "spark-defaults",
              "Properties": spark_properties,
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



    def get_maximum_resource_allocation_properties(self,_master_memory,_master_cores,_memory_per_workder_node_gb,_cores_per_worker_node,_number_of_worker_nodes,_executors_per_node = 1):
        """
        Will calculate spark configuration settings that maximize resource
        allocation within the cluster. Useful when you know you are only going
        to run one job at a time or are setting dynamicAllocation to false.

        :return: a dictonary of the properties to pass to boto3/AWS/spark
        """

        import math
        #Set by user
        master_memory = int(_master_memory)
        master_cores = int(_master_cores)
        number_of_worker_nodes = int(_number_of_worker_nodes)
        memory_per_workder_node_gb = int(_memory_per_workder_node_gb)
        cores_per_worker_node = int(_cores_per_worker_node)
        executors_per_node = int(_executors_per_node)

        #Change with caution
        memory_overhead_coefficient = 0.1
        executor_memory_upper_bound_gb = memory_per_workder_node_gb
        executor_core_upper_bound = 5
        os_reserved_cores = 1
        os_reserved_memory_gb = 1
        parallelism_per_core = 2

        #Calculations from previous variables
        availible_master_memory = master_memory - os_reserved_memory_gb
        availible_master_cores = master_cores - os_reserved_cores
        availible_workder_memory = memory_per_workder_node_gb - os_reserved_memory_gb
        availible_workder_cores = cores_per_worker_node - os_reserved_cores

        total_memory_per_executor = math.floor(availible_workder_memory/executors_per_node)
        overhead_memory_per_executor = math.ceil(total_memory_per_executor*memory_overhead_coefficient)
        memory_per_executor = total_memory_per_executor - overhead_memory_per_executor
        cores_per_executor = math.floor(availible_workder_cores/executors_per_node)
        unused_memory_per_node = availible_workder_memory -(executors_per_node*total_memory_per_executor)
        unused_cores_per_node = availible_workder_cores - (executors_per_node*cores_per_executor)

        spark_executor_instances = number_of_worker_nodes*executors_per_node
        spark_yarn_driver_memoryOverhead = math.ceil(availible_master_memory*memory_overhead_coefficient)*1024

        return {
            "spark.executor.instances": str(spark_executor_instances),
            "spark.yarn.executor.memoryOverhead":str(overhead_memory_per_executor*1024),
            "spark.executor.memory": str(memory_per_executor) +'G',
            "spark.yarn.driver.memoryOverhead":str(spark_yarn_driver_memoryOverhead),
            "spark.driver.memory":str(min(availible_master_memory-(spark_yarn_driver_memoryOverhead/1024),executor_memory_upper_bound_gb-(executor_memory_upper_bound_gb*memory_overhead_coefficient) ))+'G',
            "spark.executor.cores": str(cores_per_executor),
            "spark.driver.cores": str(min(availible_master_cores,executor_core_upper_bound)),
            "spark.default.parallelism":str(spark_executor_instances*cores_per_executor*parallelism_per_core)
        }

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

            spark_properties = {}
            if self.set_maxmimum_allocation:
                #Get the cores/RAM of worker/master
                master_memory = ec2_data_dict[self.master_instance_type]['memory']
                master_cores = ec2_data_dict[self.master_instance_type]['cores']
                worker_memory = ec2_data_dict[self.slave_instance_type]['memory']
                worker_cores = ec2_data_dict[self.slave_instance_type]['cores']

                spark_properties = self.get_maximum_resource_allocation_properties(_master_memory=master_memory,_master_cores=master_cores,_memory_per_workder_node_gb=worker_memory,_cores_per_worker_node=worker_cores,_number_of_worker_nodes=self.worker_instance_count,_executors_per_node=self.number_of_executors_per_node)
                print('spark_properties:')
                print(spark_properties)
            #Spin up the cluster
            emr_response = self.load_cluster(_spark_properties = spark_properties)
            emr_client = self.boto_client("emr")
            self.job_flow_id = emr_response.get("JobFlowId")
            #wait until cluster is in a ready state
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
