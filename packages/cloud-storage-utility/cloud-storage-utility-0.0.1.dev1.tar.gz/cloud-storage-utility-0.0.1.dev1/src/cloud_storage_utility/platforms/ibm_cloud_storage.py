from concurrent.futures.thread import ThreadPoolExecutor
import ibm_boto3
from ibm_botocore.config import Config

from ..common.base_cloud_storage import BaseCloudStorage
from ..config import config


class IbmCloudStorage(BaseCloudStorage):
    def __init__(self, use_threads=True):
        super().__init__()
        self.use_threads = use_threads
        self.api_key = config.IBM_CONFIG['api_key']
        self.cos_crn = config.IBM_CONFIG['crn']
        self.auth_endpoint = config.IBM_CONFIG['auth_endpoint']
        self.cos_endpoint = config.IBM_CONFIG['cos_endpoint']

        self.cos = self.__get_resource(self.api_key,
                                       self.cos_crn,
                                       self.auth_endpoint,
                                       self.cos_endpoint)

    def upload_file(self, bucket_name, cloud_key, file_path):
        try:
            # the upload_fileobj method will automatically execute a multi-part upload
            # in 5 MB chunks for all files over 15 MB
            with open(file_path, "rb") as file_data:
                self.cos.Object(bucket_name, cloud_key).upload_fileobj(Fileobj=file_data)
                return True
        except Exception as error:  # pylint: disable=broad-except
            print(error)
            return False

    def upload_files(self, bucket_name, cloud_files):
        if self.use_threads and len(cloud_files) > 1:
            self.__upload_files_parallel(bucket_name, cloud_files)
        else:
            self.__upload_files_serial(bucket_name, cloud_files)

    def clear_bucket(self, bucket):
        delete_list_array = self.get_bucket_keys(bucket)
        return self.remove_items(bucket, delete_list_array)

    def remove_items(self, bucket_name, item_names):
        # do nothing
        if len(item_names) == 0:
            return []
        # the cloud function only allows up to 1000 keys per request, so we may need many requests
        delete_requests = []
        try:
            request = []
            for i, name in enumerate(item_names):
                request.append({"Key": name})
                # every time the index is a mod of 1000, we know that's a complete request
                if (i + 1) % 1000 == 0:
                    delete_requests.append({"Objects": request})
                    # reset request list for the next iteration
                    request = []
            # append whatever is left over
            if len(request) > 0:
                delete_requests.append({"Objects": request})

            # submit the requests in parallel
            with ThreadPoolExecutor(self.max_threads) as executor:
                for delete_request in delete_requests:
                    executor.submit(self.cos.Bucket(bucket_name).delete_objects, Delete=delete_request)
        except Exception as error:  # pylint: disable=broad-except
            print(error)

        return delete_requests

    def download_file(self, bucket_name, cloud_key, destination_filepath):
        try:
            self.cos\
                .Object(bucket_name, cloud_key)\
                .download_file(destination_filepath, Config=self._get_transfer_config(False))
            return True
        except Exception as error:  # pylint: disable=broad-except
            print(error)
            return False

    def get_bucket_keys(self, bucket_name):
        try:
            files = self.cos.Bucket(bucket_name).objects.all()
            # I only want to return the keys
            return_array = list(map(lambda x: x.key, files))
        except Exception as error:  # pylint: disable=broad-except
            print(error)
            return []

        return return_array

    def get_buckets(self):
        pass

    def __upload_files_serial(self, bucket_name, cloud_map):
        for file in cloud_map:
            self.upload_file(bucket_name, file.cloud_key, file.local_filepath)

    def __upload_files_parallel(self, bucket_name, cloud_map):
        with ThreadPoolExecutor(self.max_threads) as executor:
            for file in cloud_map:
                executor.submit(self.upload_file, bucket_name, file.cloud_key, file.local_filepath)

    def _get_transfer_config(self, use_threads=True):
        # set the transfer threshold and chunk size
        return ibm_boto3.s3.transfer.TransferConfig(
            use_threads=use_threads,
            multipart_threshold=self.default_file_threshold,
            multipart_chunksize=self.default_part_size
        )

    @staticmethod
    def __get_resource(api_key, cos_crn, auth_endpoint, cos_endpoint):
        return ibm_boto3.resource("s3",
                                  ibm_api_key_id=api_key,
                                  ibm_service_instance_id=cos_crn,
                                  ibm_auth_endpoint=auth_endpoint,
                                  config=Config(signature_version="oauth"),
                                  endpoint_url=cos_endpoint)
