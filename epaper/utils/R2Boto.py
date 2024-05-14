import boto3
import environ
from botocore.exceptions import NoCredentialsError, ClientError


class R2Boto:
    def __init__(self):
        env = environ.Env()
        environ.Env.read_env()
        self.token = env('R2_TOKEN')
        self.access_key_id = env('R2_ACCESS_KEY')
        self.secret_key = env('R2_SECRET_KEY')
        self.bucket_name = env('R2_BUCKET_NAME')
        self.endpoint_url = env('R2_END_POINT')
        self.base_url = env('R2_BASE_URL')
        self.s3 = boto3.resource('s3', endpoint_url=self.endpoint_url, aws_access_key_id=self.access_key_id, aws_secret_access_key=self.secret_key)

    def get_url(self, bucket_path):
        return self.base_url + bucket_path

    def upload_file(self, local_file_path, s3_file_name):
        try:
            # Upload the file to R2
            self.s3.Bucket(self.bucket_name).upload_file(local_file_path, s3_file_name)
            print(f"Upload successful: {s3_file_name}")
            return True
        except FileNotFoundError:
            print("The file was not found")
            return False
        except (NoCredentialsError, ClientError) as e:
            print(f"Error uploading file to S3: {e}")
            return False

    def upload_file_obj(self, file_obj, s3_file_name):
        try:
            self.s3.Bucket(self.bucket_name).put_object(Key=s3_file_name, Body=file_obj)
            print(f"Upload successful: {s3_file_name}")
            return True
        except (NoCredentialsError, ClientError) as e:
            print(f"Error uploading file to S3: {e}")
            return False

    def batch_delete_objects(self, keys):
        try:
            objects_to_delete = [{'Key': key} for key in keys]
            response = self.s3.Bucket(self.bucket_name).delete_objects({'Objects': objects_to_delete})
            print(f"Deleted {len(response['Deleted'])} objects")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
