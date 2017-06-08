import logging
import os
import io
from datetime import datetime
import boto3
import botocore

class LoggingController(object):
    """
    A class for logging code output and mathplotlib plots in aws s3. Only ONE
    object should be instantiated for a script for consolidated results.
    """
    def __init__(self, profile_name = 'default', s3_bucket = 'emr-related-files',s3_bucket_path='job_logs/',app_name='MyApp'):
        self.init_datetime_string = self.get_datetime_str()                     #Used to create an s3 directory so multiple scripts don't overwrite the same files
        self.s3_bucket = s3_bucket                                              # S3 Bucket to use for storage
        self.profile_name = profile_name                                        # Define IAM profile name (see: http://boto3.readthedocs.io/en/latest/guide/configuration.html)(config file located at user folder .aws directory)
        self.s3_bucket_path = s3_bucket_path                                    #The path to store the logs on your bucket (must end in a / b/c its a directory)
        self.app_name = app_name                                                #The name of your app

    def get_datetime_str(self):
        """
        Gets a formated datetime string for naming purposes.
        """
        return datetime.now().strftime("%Y%m%d.%H:%M:%S.%f")
    def get_path_for_new_log(self):
        """
        Gets path to store new log message.
        """
        return str(self.s3_bucket_path + 'unbuilt/'+ self.app_name + '&&&' + self.init_datetime_string + '/' + self.get_datetime_str())
    def log_matplotlib_plot(self,plot, format = 'png'):
        """
        Uploads matplotlib plot to an s3 bucket.

        :param plot: The plot object to upload to s3.
        :param image_name: The image name (should be unique to prevent overwrite)
        :param format: The file type to plot.savefig as.
        :return:
        """
        img_data = io.BytesIO()
        try:
            plot.savefig(img_data, format='png')
        except:
            #Some plots throw an error which is fixed by this
            fig = plot.get_figure()
            fig.savefig(img_data)

        img_data.seek(0)

        s3 = boto3.resource('s3')
        bucket = s3.Bucket(self.s3_bucket)
        path = self.get_path_for_new_log() + '.png'
        bucket.put_object(Body=img_data, ContentType='image/png', Key=path)
    def log_string(self,string):
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(self.s3_bucket)
        path = self.get_path_for_new_log() + '.txt'
        bucket.put_object(Body=string, ContentType='text/plain', Key=path)
