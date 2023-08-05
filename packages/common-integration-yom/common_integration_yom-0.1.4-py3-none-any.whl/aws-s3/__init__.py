import boto3

class AWSS3:
    def __init__(self, bucket_name, key, access_key_id, secret_access_key):
        self.bucket_name = bucket_name
        self.key = key
        self.s3_session = boto3.Session(
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key)
        self.s3 = self.s3_session.client('s3')
        self.resource = self.s3_session.resource('s3')

    
    def upload_file(self, filename, object_name):
        try:
            response = self.s3.upload_file(filename, self.bucket_name, object_name)
        except ClientError as e:
            raise Exception('Upload Error', f'error saving a file {filename} in s3')
        return response


    def download_file(self, filename, object_name):
        try:
            response = self.s3.download_file(self.bucket_name, object_name, filename)
        except ClientError as e:
            raise Exception('Download Error', f'error downloading a file {filename} in s3')
        return response


    def list_files(self, prefix):
        try:
            my_bucket = self.resource.Bucket(self.bucket_name)
            files = my_bucket.objects.filter(Prefix=prefix)
            files = list(map(lambda f: f.key, files))
            return files
        except ClientError as e:
            raise Exception('List Files Error', f'error downloading files in bucket {self.bucket_name}')

    
    def set_bucket_name(self, bucket_name):
        self.bucket_name = bucket_name


    def set_key(self, key):
        """
        key is the path where the file is saved.
        Example:
        self.key="customer/soprole/integrations/intelligence/errors/integration-soprole-error-2020-11-19.csv"
        """
        self.key = key


    def set_session(self, access_key_id, secret_access_key):
        self.s3_session = boto3.Session(
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key
        )
        self.s3 = self.s3_session.client('s3')
        self.resource = self.s3_session.resource('s3')
