import boto3

class AWSS3:
    def __init__(self, bucket_name, key, access_key_id, secret_access_key):
        self.bucket_name = bucket_name
        self.key = key
        self.s3_session = boto3.Session(
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key)
        self.s3 = self.s3_session.client('s3')

    
    def upload_csv_file(self, filename, object_name):
        try:
            response = self.s3.upload_file(filename, self.bucket_name, object_name)
        except ClientError as e:
            raise Exception('Upload Error', 'error savings a file in s3')
        return response

    
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
