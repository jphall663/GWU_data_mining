import logging
import os
import io
from datetime import datetime
import boto3
from boto3.s3.transfer import S3Transfer
import botocore
import platform

class MarkdownBuilder(object):
    """
    A class for logging code output and mathplotlib plots in aws s3. Only ONE
    object should be instantiated for a script for consolidated results.
    """
    def __init__(self, profile_name = 'default', s3_bucket = 'emr-related-files',s3_bucket_path='job_logs/',app_name='MyApp',path_to_save_logs_local=os.path.dirname(__file__)+'/logs'):
        self.s3_bucket = s3_bucket                                              # S3 Bucket to use for storage
        self.profile_name = profile_name                                        # Define IAM profile name (see: http://boto3.readthedocs.io/en/latest/guide/configuration.html)(config file located at user folder .aws directory)
        self.s3_bucket_path = s3_bucket_path                                    #The path to store the logs on your bucket (must end in a / b/c its a directory)
        self.app_name = app_name                                                #The name of your app
        self.path_to_save_logs_local = path_to_save_logs_local                  #A path to save all the built logs on your local machine.

    def get_datetime_str(self):
        """
        Gets a formated datetime string for naming purposes.
        """
        return datetime.now().strftime("%Y%m%d.%H:%M:%S.%f")

    def log_string(self,string):
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(self.s3_bucket)
        path = self.get_path_for_new_log()
        bucket.put_object(Body=string, ContentType='text/plain', Key=path)

    def build_markdowns(self):
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(self.s3_bucket)
        result = bucket.meta.client.list_objects_v2(Bucket=bucket.name,
                                         Delimiter='/', Prefix=self.s3_bucket_path+'unbuilt/')
        for o in result.get('CommonPrefixes'):
            prefix = o.get('Prefix') #example: job_logs/unbuilt/MyApp&&&20170607.00:54:28.355680/
            splits = prefix.split('/')
            folder_name = splits[-2]
            splits2 = folder_name.split('&&&')
            app_name = splits2[0]
            timestamp = splits2[1]
            result_inner = bucket.meta.client.list_objects_v2(Bucket=bucket.name,
                                             Prefix=prefix)
            objects_to_delete = []

            #Start making the first unbuilt markdown file
            markdown_str = 'Logs for ' + app_name + ' executed on ' +timestamp + ':\n'
            built_file_directory = self.s3_bucket_path + 'built/' + app_name + '/'+timestamp
            for o2 in result_inner.get('Contents'):
                key = o2.get('Key')
                key_split = key.split('/')
                filename, file_extension = os.path.splitext(key_split[-1])
                #Get ride of characters that are bad for windows files
                filename = filename.replace(':','').replace('.','')
                #This file will be deleted later
                objects_to_delete.append({'Key':key})
                #Download the file
                obj = s3.Object(bucket, key)

                if file_extension in ['.png','.jpg']:
                    #its a plot or image
                    if self.path_to_save_logs_local != False:
                        file_path = self.path_to_save_logs_local+'/'+app_name+'/'+timestamp.replace(':','').replace('.','')+'/data/'
                        if platform.system() == 'Windows':
                            file_path = file_path.replace('/','\\').replace(':','.')
                        #Make the directory if it doesnt exist
                        if not os.path.exists(file_path):
                            os.makedirs(file_path)
                        transfer = S3Transfer(boto3.client('s3'))
                        #download the file to a local location
                        transfer.download_file(self.s3_bucket,key,file_path+filename+file_extension)
                    markdown_str += '![{image_name}]({relative_path})'.format(image_name=filename,relative_path='data/'+filename+file_extension) + '\n'
                else:
                    file_content = boto3.client('s3').get_object(Bucket=self.s3_bucket,Key=key)['Body'].read().decode('UTF-8')
                    print(file_content)
                    markdown_str += "<p style='white-space: nowrap;'>`"+str(file_content)+'`</p>'+'\n'
                s3.Object(self.s3_bucket,built_file_directory+'/data/'+filename+file_extension).copy_from(CopySource=self.s3_bucket+'/'+key)

            bucket.put_object(Body=markdown_str, ContentType='text/plain', Key=built_file_directory+'/log.md')
            if self.path_to_save_logs_local != False:
                file_path = self.path_to_save_logs_local+'/'+app_name+'/'+timestamp.replace(':','').replace('.','')
                if platform.system() == 'Windows':
                    file_path = file_path.replace('/','\\').replace(':','.')
                #Make the directory if it doesnt exist
                if not os.path.exists(file_path):
                    os.makedirs(file_path)
                file = open(file_path+'/log.md','w')
                file.write(markdown_str)
                file.close()
            #delete the old files now that they have been moved to built
            bucket.delete_objects(Delete={'Objects':objects_to_delete})
