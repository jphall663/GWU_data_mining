import os
import sys

from spark_controler.emr_controller import EMRController



deployer = EMRController()
deployer.profile_name = 'default'
deployer.subnet_id = 'subnet-50c2a327'
deployer.key_name = 'EMR_Key'
deployer.s3_bucket = 'emr-related-files'
deployer.master_instance_type = 'm4.xlarge'
deployer.slave_instance_type = 'm4.xlarge'
deployer.worker_instance_count = 2
deployer.set_maxmimum_allocation = True
deployer.number_of_executors_per_node = 1
# deployer.run('create')

deployer.job_flow_id = 'j-7F2D0E3L1W1W'
deployer.path_script = os.path.dirname( __file__ )
deployer.file_to_run = 'spark_main.py'
# Use this if you want to spark submit on the server manually in an ssh shell
# spark-submit --packages ai.h2o:sparkling-water-core_2.11:2.1.9 --conf spark.dynamicAllocation.enabled=false yourfile.py
deployer.additional_job_args = ['--packages', 'ai.h2o:sparkling-water-core_2.11:2.1.7', '--conf', 'spark.dynamicAllocation.enabled=false']
deployer.run('run_job')
